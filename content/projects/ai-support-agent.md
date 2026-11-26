---
title: "AI support agent in production"
slug: ai-support-agent
date: 2026-10-16
period: "Live since 16 Oct 2026"
status: live
weight: 10
icon: bot
tagline: "Carries out standard changes, takes support calls and answers questions in Teams, live for 200+ organisations."
summary: "Solo-built Azure platform for an AI support agent, live since 16 Oct 2026, for 200+ client organisations. It carries out standard changes without engineer approval, handles inbound support calls and answers documentation questions in Teams."
tech: ["Azure Container Apps", "Bicep", "PostgreSQL", "Azure DevOps", "Key Vault", "Python"]
thumb: "/img/projects/ai-support-agent/architecture.svg"
thumb_width: 1200
thumb_height: 760
---

This is a solo-built, Azure-hosted support agent that has been live since 16 October 2026 and is used across more than 200 client organisations. It started as an agent that wrote a diagnosis note for an engineer to review, and it now does three things. When a new ticket arrives, the agent reads from the PSA, the documentation platform, the RMM, the EDR and the Microsoft 365 management tools, diagnoses the problem and carries out standard changes itself, without an engineer approving them. It answers inbound customer calls, creates the ticket and resolves some issues during the call. And it works as a documentation source that colleagues query from a Teams chat. On the platform side the work is a read service and a separate execute service, each with its own identity and database role, secrets taken at runtime from Key Vault, PostgreSQL with Entra authentication, and a pipeline that tests every change, builds container images and deploys through Bicep.

{{< figure src="/img/projects/ai-support-agent/architecture.svg" alt="High-level flow: a new PSA ticket, an inbound call and a Teams question reach an Azure-hosted agent, which works in the PSA, a documentation platform, RMM, EDR and an M365 management tool. It carries out standard changes without engineer approval, handles the call and creates the ticket, and answers the question from the documentation." caption="High-level flow. Tickets, calls and Teams questions come in; the agent carries out standard changes itself, handles calls and answers from the documentation. Vendor names, network detail and client information are left out." width=1200 height=760 dark=true >}}

## Platform

The platform is the work. The agent is the workload on top of it.

It is split into a read service and a separate execute service. Each has its own managed identity, its own Key Vault access and its own PostgreSQL role. The model has no credentials for customer systems. Standard changes run without waiting for an engineer's approval. Every other write action in a customer environment requires approval. The approval path — mail, a confirmation page, a queue and a scheduled execute job — binds a decision to one unchanged proposal with a server-side token.

The services run on Azure Container Apps, with Azure Container Apps Jobs for scheduled work. Images are non-root and the build contains no secrets. Eighteen additive PostgreSQL migrations are applied by a migration tool that checks checksums, takes an advisory lock and uses a role per service. PostgreSQL uses Entra authentication over TLS.

Infrastructure is Bicep. The Azure DevOps pipeline has four stages: required pull-request tests with no Azure access, incremental image builds in Azure Container Registry, Container Apps deploys gated on a health check, then Bicep deployments that cannot roll an image backwards. An exclusive lock stops two releases from overlapping. Secrets are read from Key Vault at runtime through managed identity. Secret scanning runs in pre-commit and in CI, with a pinned tool version and a checksum, and dependency auditing runs on each build.
