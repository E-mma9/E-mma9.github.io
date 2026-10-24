---
title: "Notes on my 3-node Proxmox cluster"
date: 2026-01-18
summary: "Hardware, networking, and what I've learned running three nodes at home."
tags: ["proxmox", "homelab", "linux", "virtualization"]
showTableOfContents: true
---

A short write-up on my home Proxmox cluster — why three nodes, how it's wired, and what I've learned. I get asked about this a lot, so this is the canonical answer.

## Hardware

Three second-hand small-form-factor PCs, a Dell OptiPlex and two HP ProDesks, all on Intel i5 CPUs:

- **pve** — 16 GB RAM, 238 GB NVMe for the OS, plus a 931 GB HDD as a ZFS pool for backups
- **node2** — 8 GB RAM, 119 GB NVMe
- **node3** — 8 GB RAM, 119 GB SSD

All three run Proxmox VE 9, headless, joined in one cluster with high availability enabled.

## Why three instead of one

A single bigger server would be cheaper to run and quieter. Three nodes give me things a single host can't:

- **Quorum** — three is the minimum for the cluster to keep making decisions when one node drops out. With two, losing one locks the cluster up.
- **HA** — Proxmox restarts a failed service up to three times on the same node, then migrates it to another one. I can take a node down for kernel updates without losing the services on it.
- **Live migration** — `pct migrate` and `qm migrate` move a workload between hosts with a few seconds of network blip. Useful operationally, and useful for testing.
- **Real failure modes** — pulling a power cable on one node behaves differently from rebooting a single host. The behaviour during recovery is the actual reason I have three.

## Networking

Everything sits on one bridged LAN via `vmbr0`, not segmented yet. Remote access goes over Tailscale, so nothing is exposed to the internet: no port forwards, no public IPs on the nodes.

## Storage

Storage is local on each node. There is no shared storage: a distributed storage layer would need an extra disk per node, and I did not want to spend on that yet. The ZFS pool on `pve` holds the backups for the whole cluster.

The trade-off shows up on failover. Without shared storage, HA has to copy the container disk to the target node before it can start there, so a failover takes minutes rather than seconds. For a homelab that's fine.

## What it's not

- Not cheaper than a single server, on hardware or electricity
- Not quieter — three fans humming
- Not simpler

It's just closer to a production setup, which is the only reason I run it.

## What I'd do differently

Shared storage first. An extra disk per node for distributed storage, or an NFS share, would turn failover from minutes into seconds. Network segmentation is next on the list.
