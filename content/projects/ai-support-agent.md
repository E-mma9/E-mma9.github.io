---
title: "AI support agent in production"
slug: ai-support-agent
date: 2026-10-01
period: "Live since Oct 2026"
status: live
weight: 10
icon: bot
summary: "Solo-built agent that researches every new support ticket for 200+ client organisations and delivers a diagnosis note in 1–2 minutes."
tech: ["Azure Container Apps", "Service Bus", "PostgreSQL", "Key Vault", "Bicep", "Azure DevOps", "MCP", "Claude"]
thumb: "/img/projects/ai-support-agent/architecture.svg"
thumb_width: 1200
thumb_height: 760
---

Built end-to-end at a managed service provider, from the first design document to the production rollout. The agent sits in the support flow: every new ticket is picked up automatically, researched across the company's tooling, and handed back to the engineer with a diagnosis note before they have opened it.

From idea to production took seven weeks. The agent now runs about 45 times per workday for 200+ client organisations. The first week saw 200+ runs and zero data incidents.

{{< figure src="/img/projects/ai-support-agent/architecture.svg" alt="Simplified production architecture: a ticket triggers a job in a private Azure virtual network, the Hermes agent calls a read-only MCP server that reads Autotask, IT Glue and Datto RMM and writes one internal note; Key Vault, PostgreSQL, Container Registry and Log Analytics sit behind private endpoints" caption="Simplified architecture. Internal names, addressing and client details are left out on purpose." width=1200 height=760 dark=true >}}

## How a run works

1. **A new ticket arrives** in the PSA. A small trigger job picks it up through a Service Bus queue and starts exactly one run for exactly one ticket. The request to the agent is signed, so nothing else can start a run.
2. **The agent researches.** It uses 17 read-only tools over Autotask (tickets and history), IT Glue (documentation) and Datto RMM (endpoints), exposed through an MCP server. The server fixes the ticket and the client scope for the run before the model starts; the model cannot widen it.
3. **The model reasons** over what the tools return. Model calls leave the network through a NAT gateway with a fixed outbound address.
4. **One write, nothing else.** The result is a diagnosis note with a proposed next step, written as an internal note on the ticket. That is the only write path the agent has. The engineer reads it and decides.

Every run is stored in PostgreSQL with its inputs, tool calls and output, so each note can be traced back.

## Platform as code

The whole platform is defined in Bicep and deployed from the pipeline, nothing by hand:

- **Azure Container Apps** for the agent, the MCP server and the trigger job, each with its own managed identity and scale-to-zero when idle.
- **Service Bus** queue between ticket intake and the agent.
- **PostgreSQL Flexible Server** with Entra authentication only, no passwords.
- **Key Vault** for every token and signing key, read at runtime through managed identity with access granted per secret.
- **Container Registry** with the admin user disabled; images are pulled by digest.
- **Private virtual network**: data services are reachable through private endpoints only, public access is switched off, and all outbound traffic leaves through the NAT gateway.
- **Log Analytics** collects application logs, Key Vault audit events and database metrics, with alert rules on top.

## Delivery pipeline

Azure DevOps runs the whole chain on every pull request: unit tests, `pip-audit` for vulnerable dependencies, `gitleaks` for leaked secrets, an image build pushed through workload identity federation (no stored registry credentials), and a health-checked rollout. A branch policy on `main` requires green tests, so nothing reaches production untested or unscanned.

## Security by design

The rule throughout: the boundary lives in code, never in a prompt.

- **One ticket per run.** The scope is set by the server before the model starts and cannot be changed by the model.
- **Zero credentials inside the agent.** The agent process has no tokens for client systems; only the MCP server talks to the APIs, and it reads its tokens from Key Vault at runtime.
- **Secret fields filtered.** Password-type fields from documentation never reach the model; the agent gets the item name and a link, not the value.
- **Prompt injection detected and refused.** Ticket text is untrusted input. Instructions hidden in a ticket or an attachment are recognised and the run refuses to act on them.
- **Read-only by construction.** The tools are read-only and the single write is the internal note. Execution of proposals is a separate, later component with its own identity and its own vault.

## What's next

A second agent for sales is in design. It gets an MCP server as its only write path and a human approval step before any message is sent. The execution side of the support agent follows the same pattern: fixed building blocks, approved by an engineer in the ticket, carried out by a separate service that checks the approval itself.
