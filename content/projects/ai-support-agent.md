---
title: "AI support agent in production"
slug: ai-support-agent
date: 2026-10-01
period: "Live since Oct 2026"
status: live
weight: 10
icon: bot
summary: "Solo-built agent that researches every new support ticket for ~50 client organisations and delivers a diagnosis note in 1–2 minutes."
tech: ["Azure Container Apps", "Service Bus", "PostgreSQL", "Key Vault", "Bicep", "Azure DevOps", "Claude"]
---

Built end-to-end during my internship at JUICT, a managed service provider. The agent sits in the support flow: every new ticket is picked up, researched across the company's tooling, and returned to the engineer with a diagnosis note before they open it.

## What it does

From idea to production in seven weeks. The agent researches every new support ticket for ~50 client organisations and delivers a diagnosis note in 1–2 minutes. It runs about 45 times per workday; the first week saw 200+ runs and zero data incidents.

Research happens through 17 read-only tools over Autotask (tickets), IT Glue (documentation) and Datto RMM (endpoints). The agent can look, not touch.

## Platform as code

The whole platform is defined in Bicep: Azure Container Apps, a Service Bus queue feeding a job, PostgreSQL, Key Vault accessed through managed identities, a container registry, and a scale-to-zero schedule so nothing runs idle.

The pipeline in Azure DevOps runs unit tests, `pip-audit` and `gitleaks`, deploys with health-checked rollouts, and validates every pull request with a build. Nothing reaches production untested or unscanned.

## Security by design

The limits are enforced in code rather than in prompts: one ticket per run, zero credentials inside the agent, secret fields filtered before anything reaches the model, and prompt-injection attempts detected and refused.

A second agent for sales is in design. It gets an MCP server as its only write path, with human approval before any message is sent.
