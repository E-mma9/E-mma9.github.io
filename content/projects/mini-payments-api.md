---
title: "Mini Payments API"
date: 2026-10-24
period: "Oct 2026 – present"
status: wip
weight: 20
icon: payments
summary: "Spring Boot payments service with PostgreSQL and Flyway, containerized with a multi-stage image and local Kubernetes manifests."
tech: ["Java", "Spring Boot", "PostgreSQL", "Flyway", "Maven", "Docker", "Kubernetes"]
repo: "https://github.com/E-mma9/mini-payments-api"
---

A small payments service built to practice platform work: accounts and transfers with strict business rules, migrations, tests, then Docker and Kubernetes locally.

## What exists today

- Spring Boot service with an accounts and transfers API, including balance checks and business-rule exceptions.
- PostgreSQL schema managed by Flyway migrations.
- A unit test for the transfer rules and an integration test for the full transfer flow, run through the Maven wrapper.
- Multi-stage Dockerfile: Maven build stage, runtime on a JRE Alpine image as a non-root user. Image went from 825 MB on disk (single-stage) to 402 MB.
- docker-compose for the app and PostgreSQL together.
- Kubernetes manifests for the app (3 replicas) and the database (1 replica, because a database is stateful and there is no StatefulSet or PersistentVolumeClaim yet). Ran on Docker Desktop's built-in Kubernetes, not yet on the homelab cluster.

## Next

- GitHub Actions pipeline with Trivy image scanning.
- Deploy the manifests to the homelab cluster.
- AKS via Terraform.
- Prometheus metrics and a Grafana dashboard.
