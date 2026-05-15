---
title: "Monitoring Homelab"
date: 2026-02-10
summary: "Production-style Prometheus + Grafana + Alertmanager stack on a 3-node Proxmox cluster. PagerDuty for paging."
tags: ["proxmox", "prometheus", "grafana", "alertmanager", "pagerduty", "linux", "homelab"]
externalUrl: "https://github.com/E-mma9/Monitoring-Homelab"
showHero: false
---

A full monitoring stack on a 3-node Proxmox VE cluster running on consumer hardware. Every config file written by hand so I actually understand what each setting does.

## What's running

- **Prometheus** scraping 15s metrics from all nodes and services
- **Grafana** dashboards (node health, networking, container)
- **Alertmanager** routing to PagerDuty
- **node_exporter** on every host
- **blackbox_exporter** for HTTP/TCP endpoint checks
- **Tailscale** mesh for remote access

## Alert rules

Seven alert rules in production:

- `NodeDown` — any host unreachable for > 2 min
- `DiskSpaceLow` — < 15% free
- `HighCPU` — > 90% sustained 10 min
- `HighRAM` — > 90% sustained 5 min
- `EndpointDown` — any blackbox target failing
- `ServiceCrashed` — systemd unit in failed state
- `ProxmoxStorageWarn` — storage pool > 85%

## Paging

Alertmanager → PagerDuty. SMS on alert, voice escalation if not acknowledged within 5 minutes. Tested by triggering each rule deliberately.

## Repo

[github.com/E-mma9/Monitoring-Homelab](https://github.com/E-mma9/Monitoring-Homelab)
