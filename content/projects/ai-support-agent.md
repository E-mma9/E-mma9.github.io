---
title: "AI support agent in production"
slug: ai-support-agent
date: 2026-10-16
period: "Live since 16 Oct 2026"
status: live
weight: 10
icon: bot
summary: "Solo-built Azure platform for an AI support agent, live since 16 Oct 2026, for ~200 client organisations. A person reviews every note. Write actions require approval."
tech: ["Azure Container Apps", "Bicep", "PostgreSQL", "Azure DevOps", "Key Vault", "Python"]
thumb: "/img/projects/ai-support-agent/architecture.svg"
thumb_width: 1200
thumb_height: 760
---

This is a solo-built, Azure-hosted support agent that has been live since 16 October 2026 and is used across around 200 client organisations. When a new ticket arrives, the agent reads from the PSA, the documentation platform, the RMM, the EDR and the Microsoft 365 management tools, then writes an internal note with a diagnosis and a proposed next step; a person reviews that note, and anything that would change a customer environment runs only after approval. On the platform side the work is a read service and a separate execute service, each with its own identity and database role, secrets taken at runtime from Key Vault, PostgreSQL with Entra authentication, and a pipeline that tests every change, builds container images and deploys through Bicep.

{{< figure src="/img/projects/ai-support-agent/architecture.svg" alt="High-level flow: a new PSA ticket reaches an Azure-hosted agent, which reads the PSA, a documentation platform, RMM, EDR and an M365 management tool, then writes an internal note. Changes in a customer environment require approval." caption="High-level flow of a new ticket. The agent reads those systems and writes an internal note for a person. Write actions require approval. Vendor names, network detail and client information are left out." width=1200 height=760 dark=true >}}

## Platform

The platform is the work. The agent is the workload on top of it.

It is split into a read service and a separate execute service. Each has its own managed identity, its own Key Vault access and its own PostgreSQL role. The model has no credentials for customer systems. Write actions in a customer environment require approval. The approval path — mail, a confirmation page, a queue and a scheduled execute job — binds a decision to one unchanged proposal with a server-side token.

The services run on Azure Container Apps, with Azure Container Apps Jobs for scheduled work. Images are non-root and the build contains no secrets. Eighteen additive PostgreSQL migrations are applied by a migration tool that checks checksums, takes an advisory lock and uses a role per service. PostgreSQL uses Entra authentication over TLS.

Infrastructure is Bicep. The Azure DevOps pipeline has four stages: required pull-request tests with no Azure access, incremental image builds in Azure Container Registry, Container Apps deploys gated on a health check, then Bicep deployments that cannot roll an image backwards. An exclusive lock stops two releases from overlapping. Secrets are read from Key Vault at runtime through managed identity. Secret scanning runs in pre-commit and in CI, with a pinned tool version and a checksum, and dependency auditing runs on each build.
