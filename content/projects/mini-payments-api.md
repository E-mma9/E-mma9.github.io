---
title: "Mini Payments API"
date: 2026-10-24
period: "Oct 2026 – present"
status: wip
weight: 20
icon: payments
summary: "Spring Boot payments service with PostgreSQL and Flyway, on its way to Kubernetes with a scanned CI/CD pipeline."
tech: ["Java", "Spring Boot", "PostgreSQL", "Flyway", "Maven", "Kubernetes"]
repo: "https://github.com/E-mma9/mini-payments-api"
---

A small payments service built to practice platform work at a payments-grade standard: strict business rules, migrations, tests, and a delivery pipeline that scans before it ships.

## What exists today

- Spring Boot service with an accounts and transfers API, including balance checks and business-rule exceptions.
- PostgreSQL schema managed by Flyway migrations.
- A unit test for the transfer rules and an integration test for the full transfer flow, run through the Maven wrapper.

## Next

- Docker multi-stage build.
- Kubernetes manifests, first on the homelab cluster.
- GitHub Actions pipeline with Trivy image scanning.
- AKS via Terraform.
- Prometheus metrics and a Grafana dashboard.
