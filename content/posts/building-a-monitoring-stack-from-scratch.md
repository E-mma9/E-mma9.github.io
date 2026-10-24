---
title: "Building a monitoring stack from scratch"
date: 2026-04-02
summary: "Notes on setting up Prometheus + Alertmanager + PagerDuty by hand on my home cluster."
tags: ["prometheus", "alertmanager", "pagerduty", "homelab", "monitoring"]
showTableOfContents: true
---

I wanted monitoring on my home cluster, so I set up Prometheus, Alertmanager and PagerDuty step by step. Writing the configs myself instead of using a pre-made stack helped me understand what each part actually does. These are my notes.

## The setup

Three Proxmox nodes. Each host runs `node_exporter` directly, because it needs the host's kernel data. Prometheus, Alertmanager, Grafana and `blackbox_exporter` run together in one LXC container.

Prometheus scrapes every 15 seconds. The two jobs that matter:

```yaml
scrape_configs:
  - job_name: 'proxmox-nodes'
    static_configs:
      - targets:
          - '192.168.1.249:9100'   # pve
          - '192.168.1.211:9100'   # node2
          - '192.168.1.74:9100'    # node3

  - job_name: 'blackbox-http'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - 'http://192.168.1.30:81'       # Nginx Proxy Manager
          - 'http://192.168.1.223/admin'   # Pi-hole
          - 'http://localhost:3000'        # Grafana
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: localhost:9115
```

The `blackbox-http` relabel block took me a while to get right. The `__param_target` rewrite is what tells `blackbox_exporter` which URL to probe on each scrape — without it, you get metrics but the target is empty.

## Alert rules

Seven rules, each with a `for` duration so a short spike doesn't page me:

- `NodeDown` — node_exporter unreachable for 1 minute
- `DiskSpaceWarning` — root partition above 85% for 5 minutes
- `DiskSpaceCritical` — above 95% for 2 minutes
- `HighMemoryUsage` — RAM above 90% for 5 minutes
- `HighCPUUsage` — CPU above 95% for 10 minutes
- `EndpointDown` — HTTP probe failing for 2 minutes
- `SlowResponse` — response slower than 5 seconds for 5 minutes

## Alertmanager

The mental model that helped me: labels are inputs, routes are filters, receivers are destinations.

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
      - routing_key: '...'
  - name: 'null'
```

Info-level alerts go to a null receiver. Everything else pages.

## Testing the chain

I needed to verify alerts actually reach PagerDuty without breaking a real service. I added a `TestAlert` rule with a constant true expression:

```yaml
- alert: TestAlert
  expr: vector(1) > 0
  for: 0m
  labels:
    severity: critical
  annotations:
    summary: "Manual test alert"
```

Reload Prometheus, wait for the alert to fire, get the text message. A few minutes later the phone call came in because I didn't acknowledge it. Then I disabled the rule again.

## Things that tripped me up

- A wrong `__param_target` rewrite meant every blackbox metric had an empty `instance` label, so Alertmanager couldn't deduplicate alerts.
- `group_interval: 30s` (which I had early on) flooded my phone with 12 pages from one outage. `5m` is much saner.
- I had the wrong PagerDuty integration key for a few days. Alerts fired in Alertmanager but PagerDuty showed nothing. The Alertmanager logs surfaced it eventually.

## Repo

[github.com/E-mma9/Monitoring-Homelab](https://github.com/E-mma9/Monitoring-Homelab) — full config and Grafana dashboard JSON.
