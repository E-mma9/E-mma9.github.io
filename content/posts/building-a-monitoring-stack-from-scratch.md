---
title: "Building a monitoring stack from scratch"
date: 2026-04-02
summary: "Why I rejected the all-in-one homelab installers and wrote my own Prometheus + Alertmanager + PagerDuty pipeline."
tags: ["prometheus", "alertmanager", "pagerduty", "homelab", "monitoring"]
showTableOfContents: true
---

## The shortcut I didn't take

There's a whole genre of homelab YouTube videos that goes: *"set up monitoring in 10 minutes with this docker-compose."* Pull the repo, run the script, you get Prometheus, Grafana, Loki, Alertmanager — all wired up, all running, all working. Neat.

I almost did that. Then I remembered why I built the cluster in the first place: to learn. So I deleted the compose file and started over with a blank Debian VM.

## What I actually wanted to know

Three questions I couldn't answer just from running a demo:

1. **How does Prometheus discover what to scrape?** I'd seen `scrape_configs` in tutorials, but never traced a metric end-to-end.
2. **What does Alertmanager actually route on?** Labels? Routes? Receivers? The diagrams made sense; the YAML didn't.
3. **How do you test an alert without breaking production?** Production in my case is one VM running my Nextcloud, so this matters.

## The setup

Three Proxmox nodes, each running:

- `node_exporter` on the host
- A Debian VM for Prometheus + Alertmanager (only on node 1)
- `blackbox_exporter` for synthetic HTTP checks

Prometheus config has three scrape jobs:

```yaml
scrape_configs:
  - job_name: 'nodes'
    static_configs:
      - targets: ['10.0.0.10:9100', '10.0.0.11:9100', '10.0.0.12:9100']
  - job_name: 'blackbox-http'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://cloud.emmanueltekle.nl
          - https://emmanueltekle.nl
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9115
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

The blackbox relabel dance is the bit nobody explains in tutorials. The `__param_target` rewrite is what lets Prometheus tell blackbox_exporter *which URL to probe* on each scrape.

## Alertmanager: routing actually clicked

The mental model that finally worked for me: **labels are inputs, routes are filters, receivers are destinations.** Once I saw it that way, this config wrote itself:

```yaml
route:
  receiver: 'default-pagerduty'
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers:
        - severity = "info"
      receiver: 'null'

receivers:
  - name: 'default-pagerduty'
    pagerduty_configs:
      - service_key: '...'
  - name: 'null'
```

Info-level alerts get dropped. Everything else pages. Simple.

## Testing without breaking things

I needed to verify the full chain — alert fires → Alertmanager routes → PagerDuty pages my phone — without actually breaking a service. Solution: a `TestAlert` rule with a fixed-true expression I toggle on for 60 seconds.

```yaml
- alert: TestAlert
  expr: vector(1) > 0
  for: 0m
  labels:
    severity: critical
  annotations:
    summary: "Manual test alert"
```

I `kill -HUP` Prometheus to reload, watch my phone buzz, then revert. The pager voice call arrived 5 minutes later when I deliberately didn't ack. Cool.

## What I learned

Not the tools themselves — I'd read the docs already. The thing I actually learned was how the components *fail.* When the blackbox relabel was wrong, the probes ran but every metric had an empty `instance` label and Alertmanager couldn't deduplicate. When `group_interval` was set too aggressively, I got 12 pages in a row from one outage. When PagerDuty's integration key was for the wrong service, alerts vanished silently.

You don't get any of that from a docker-compose.
