---
title: "Monitoring Homelab"
date: 2026-04-18
period: "Feb – Apr 2026"
status: done
weight: 30
summary: "Production-style Prometheus, Grafana and Alertmanager stack on a 3-node Proxmox cluster, paging through PagerDuty."
tech: ["Prometheus", "Grafana", "Alertmanager", "blackbox_exporter", "PagerDuty", "Proxmox VE"]
repo: "https://github.com/E-mma9/Monitoring-Homelab"
thumb: "/img/projects/monitoring/pipeline.jpg"
thumb_width: 1376
thumb_height: 768
---

A full monitoring and alerting pipeline on my 3-node Proxmox VE cluster. Every config file was written by hand, no helper scripts or one-click installers, so that I understand what each line does.

{{< figure src="/img/projects/monitoring/pipeline.jpg" alt="Monitoring data flow: node_exporter and blackbox_exporter feed Prometheus, which feeds Grafana and Alertmanager; Alertmanager pages through PagerDuty" caption="Data flow from exporters to my phone." width=1376 height=768 dark=true >}}

## What's running

- **node_exporter** on each Proxmox host, exposing CPU, memory, disk and network metrics.
- **Prometheus** scraping every target every 15 seconds and evaluating the alert rules.
- **Grafana** with a custom cluster-overview dashboard.
- **Alertmanager** grouping alerts and routing them to PagerDuty.
- **blackbox_exporter** probing the HTTP endpoints of the services I run.

Everything except node_exporter runs together in one LXC container; node_exporter runs directly on each host because it needs the host's kernel data.

## Alert rules

Seven rules, each with a `for` duration chosen so a short spike does not page me.

| Alert | Fires when | For | Severity |
|-------|-----------|-----|----------|
| `NodeDown` | node_exporter unreachable | 1 min | critical |
| `DiskSpaceWarning` | root partition above 85% | 5 min | warning |
| `DiskSpaceCritical` | root partition above 95% | 2 min | critical |
| `HighMemoryUsage` | RAM above 90% | 5 min | warning |
| `HighCPUUsage` | CPU above 95% | 10 min | warning |
| `EndpointDown` | HTTP probe fails | 2 min | critical |
| `SlowResponse` | response slower than 5 s | 5 min | warning |

{{< figure src="/img/projects/monitoring/prometheus-alert-rules.png" alt="Prometheus rules page showing the blackbox_alerts and node_alerts groups, all inactive" caption="All seven rules loaded and quiet." width=943 height=907 >}}

## Dashboards

{{< figure src="/img/projects/monitoring/grafana-cluster-overview.png" alt="Grafana cluster overview dashboard with CPU, memory, disk and uptime panels for node2" caption="Custom cluster-overview dashboard in Grafana." width=1400 height=663 >}}

## Paging

Alertmanager sends firing alerts to PagerDuty through the Events API. PagerDuty opens an incident and sends a text message; if I do not acknowledge it, it calls. From crash to phone buzz is about three minutes for most alerts: the `for` duration plus Alertmanager's grouping window.

I chose PagerDuty over Telegram or Discord because it is what companies use, and I wanted to set up real incident management: escalation policies, acknowledgements, on-call.

{{< figure src="/img/projects/monitoring/pagerduty-incident.png" alt="PagerDuty service page for Homelab-Alerts showing a resolved incident for an unreachable endpoint" caption="A resolved test incident in PagerDuty." width=1300 height=936 >}}

## The cluster underneath

Three second-hand small-form-factor PCs (Dell OptiPlex, HP ProDesk) running Proxmox VE 9 as a cluster with high availability enabled. Storage is local on each node, with a 931 GB ZFS pool on `pve` for backups. Without shared storage an HA failover copies the container disk to another node, which takes minutes rather than seconds; fine for a homelab. All nodes are connected over Tailscale, with no ports exposed to the internet.

{{< figure src="/img/projects/monitoring/proxmox-cluster.jpg" alt="Diagram of the three Proxmox nodes pve, node2 and node3 with the services running on each, connected through Tailscale" caption="The three nodes and what runs where." width=1376 height=768 dark=true >}}

## What I learned

- How Prometheus works under the hood: the pull model, scrape jobs, relabelling and PromQL.
- Why Alertmanager is a separate component: grouping, routing and silencing are their own problem.
- How companies handle incidents with PagerDuty: on-call, escalation and acknowledgement.

The install was the easy part. Understanding what each metric means, choosing thresholds that do not cry wolf, and building dashboards that actually help took most of the time.
