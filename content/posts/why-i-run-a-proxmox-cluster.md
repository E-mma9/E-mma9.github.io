---
title: "Notes on my 3-node Proxmox cluster"
date: 2026-01-18
summary: "Hardware, networks, and what I've learned running three nodes at home."
tags: ["proxmox", "homelab", "linux", "virtualization"]
showTableOfContents: true
---

A short write-up on my home Proxmox cluster — why three nodes, how it's wired, and what I've learned. I get asked about this a lot, so this is the canonical answer.

## Hardware

Three identical second-hand Intel N100 mini-PCs, ~€180 each. Each one has:

- N100 CPU, 16 GB RAM, 512 GB NVMe
- 2.5 GbE — matters for cluster + storage traffic
- Headless, Proxmox VE 8

Total around €600. Power draw is roughly 8 W idle, 15 W loaded per node.

## Why three instead of one

A single bigger server would be cheaper to run and quieter. Three nodes give me things a single host can't:

- **HA pairs** — Pi-hole and a few other services run as an HA pair across two nodes. I can take a node down for kernel updates without breaking DNS for the house.
- **Live migration** — `qm migrate <vmid> <target>` moves a VM between hosts with a few seconds of network blip. Useful operationally, and useful for testing.
- **Real failure modes** — pulling a power cable on one node behaves differently from rebooting a single host. The behaviour during recovery is the actual reason I have three.

## Networks

Four VLANs, segmented on an OPNsense box:

- **MGMT (VLAN 10)** — Proxmox UI, SSH, cluster heartbeat
- **STORAGE (VLAN 20)** — Ceph backend, jumbo frames (MTU 9000)
- **PROD (VLAN 30)** — VM traffic
- **TRUST (VLAN 100)** — daily-driver hosts

Splitting storage from production traffic means a heavy workload doesn't starve the management plane.

## Storage

I tried Ceph for a while because I wanted to learn it. On three N100s it's not fast, but it does heal correctly when I pull a disk. After about three months I moved most things back to ZFS replication — simpler to reason about, and at this scale the resilience of Ceph wasn't worth its operational weight for me.

## What it's not

- Not cheaper than a single server, on hardware or electricity
- Not quieter — three fans humming
- Not simpler

It's just closer to a production setup, which is the only reason I run it.

## What I'd do differently

Start with three nodes again, but skip Ceph and go straight to ZFS + scheduled replication. The time I spent on Ceph was educational but not directly useful for the workloads I actually run at home.
