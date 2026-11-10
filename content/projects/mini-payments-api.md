---
title: "Mini Payments API"
date: 2026-10-24
period: "Oct 2026 – present"
status: wip
weight: 20
icon: payments
summary: "Spring Boot payments API with PostgreSQL 17. Multistage image, Compose, then local Kubernetes with a ConfigMap, a Secret and a Postgres volume."
tech: ["Java", "Spring Boot", "PostgreSQL", "Docker", "Kubernetes"]
repo: "https://github.com/E-mma9/mini-payments-api/tree/feature/mini-payments-api-skeleton"
---

A small payments API for practising the path from code to a container to a cluster. The Java backend and the small frontend were scaffolded with Claude. The database, the containers and the Kubernetes setup are my own work. It runs on Minikube on my machine. The homelab deploy and AKS are still plans.

The steps, with the dates from the commits, are in the [Mini Payments build log]({{< relref "posts/mini-payments.md" >}}).

## What exists today

- Accounts and transfers, with business-rule errors when a transfer is not allowed. Flyway applies `V1__create_accounts_and_transfers.sql` on PostgreSQL 17.
- A unit test for the transfer rules and an integration test for the transfer flow, run with the Maven wrapper.
- Multistage Docker image. Disk usage went from 825 MB to 402 MB, content size from 265 MB to 128 MB. The process runs as a non-root user.
- Docker Compose for the app and PostgreSQL, without a volume on the database.
- Local Kubernetes, first on Docker Desktop, then Minikube. The app Deployment has 3 replicas. Postgres is one replica and is still a Deployment, not a StatefulSet.
- Database URL and username in a ConfigMap. The password is in a Secret. The app reads both with `envFrom`. Postgres reads the password with `secretKeyRef`. The secret manifest is listed in `.gitignore`.
- A 5Gi ReadWriteOnce PersistentVolumeClaim mounted at `/var/lib/postgresql/data`.

## Planned, not built

- StatefulSet for Postgres
- Liveness and readiness probes
- Resource requests and limits
- Ingress
- CI/CD to the homelab cluster, then AKS
- Prometheus and Grafana
