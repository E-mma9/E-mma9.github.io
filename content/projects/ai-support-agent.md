---
title: "AI support agent in production"
slug: ai-support-agent
date: 2026-10-16
period: "Live since 16 Oct 2026"
status: live
weight: 10
icon: bot
summary: "Solo-built AI support agent, live since 16 Oct 2026, used for ~200 client organisations of a managed service provider. Azure-hosted, with a person reviewing every note."
tech: ["Azure"]
thumb: "/img/projects/ai-support-agent/architecture.svg"
thumb_width: 1200
thumb_height: 760
---

Solo-built AI support agent for a managed service provider. It has been live since 16 Oct 2026 and is used for ~200 client organisations.

A new support ticket is picked up on Azure. The agent reads the ticket and related context from the PSA, the documentation platform and RMM, then writes a diagnosis note. An engineer reads the note and decides what happens next. Nothing goes to a client without that person.

{{< figure src="/img/projects/ai-support-agent/architecture.svg" alt="High-level flow: a new PSA ticket reaches an Azure-hosted agent, which reads the PSA, a documentation platform and RMM, then writes a diagnosis note for an engineer" caption="High-level flow. Vendor names, network detail and client information are left out." width=1200 height=760 dark=true >}}

## What it does

The agent is hosted on Azure. It works one ticket at a time and stops at a note for a person. The context it can read is read-only. The only write is that note.
