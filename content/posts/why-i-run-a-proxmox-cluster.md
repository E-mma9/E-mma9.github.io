---
title: "Why I run a 3-node Proxmox cluster at home"
date: 2026-01-18
summary: "Three machines, consumer hardware, no enterprise budget — and what I get out of it that a single VPS can't give me."
tags: ["proxmox", "homelab", "linux", "virtualization"]
showTableOfContents: true
---

## The pitch most homelabbers skip

People ask me why I run three machines instead of one beefy server. The honest answer: I wanted to fail.

Not the dramatic kind. Just the everyday kind — pull a power cable, watch what happens. Reboot a node mid-deploy, see which workloads survive. You can't simulate any of that on a single server. You can't write a runbook for HA failover if you've never failed over.

## The hardware

Three identical second-hand mini PCs, ~€180 each. Each one is:

- Intel N100, 16 GB RAM, 512 GB NVMe
- 2.5 GbE — important for cluster traffic
- Headless, runs Proxmox VE 8

Total cluster cost: under €600. About the same as one decent NAS.

## What I actually get from three nodes

**Real high-availability.** I run Pi-hole as an HA pair across two nodes. When I take node 1 down for kernel updates, my whole house still resolves DNS. Before this setup, every kernel update was a downtime event because I had services I cared about on the box.

**Storage HA via Ceph.** This is the spicy one. Ceph on three N100s is *not* fast, but it's resilient. If I pull a disk, my VMs don't notice. The cluster heals. It's also taught me more about distributed storage than any AWS whitepaper.

**Live migration.** `qm migrate <vmid> <target>` and a VM moves between hosts with seconds of network blip. Useful operationally; even more useful for testing — I can move a workload onto an isolated node and intentionally degrade it without affecting anything else.

## What it doesn't give me

Cost savings. The N100 nodes use about 8 W each idle, ~15 W loaded. Three of them, 24/7, is roughly €60–80/year in electricity. A single beefier box would run cheaper. I'm paying for the topology, not the compute.

Quiet operation either — even fanless N100s, you can hear three of them gently humming in a closet.

## How it's organized

Networks:

- **MGMT (VLAN 10)** — Proxmox web UI, SSH, cluster heartbeat
- **STORAGE (VLAN 20)** — Ceph backend traffic, jumbo frames
- **PROD (VLAN 30)** — actual VM traffic
- **TRUST (VLAN 100)** — my laptop, phone, daily-driver hosts

Segmentation matters. Cluster traffic on its own VLAN means if I saturate the lab playing with a workload, my management plane doesn't suffer. Storage traffic on its own VLAN with MTU 9000 means Ceph isn't fighting normal network traffic for bandwidth.

## What I'd change

I'd start with three nodes again. I would *not* try to run Ceph on them again — at this scale, ZFS replication is enough and an order of magnitude less complicated. Ceph was educational, but for actual lab workloads it's overkill.

## The honest summary

A homelab cluster isn't cheaper, quieter, or simpler than a single server. It's just *more like production.* If your goal is to learn how real systems behave under failure, that's worth a lot.
