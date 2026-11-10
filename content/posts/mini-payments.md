---
title: "Mini Payments: build log"
date: 2026-11-10
series:
  - Mini Payments
series_order: 1
tags: ["mini-payments", "kubernetes", "docker", "postgresql"]
summary: "Index of the Mini Payments build log, from the 15 October plan to a Postgres volume on Minikube."
---

I'm building [Mini Payments](https://github.com/E-mma9/mini-payments-api/tree/feature/mini-payments-api-skeleton) to practise the path a service takes: code, container, cluster. It's a small payments API in Java 21 with Spring Boot and PostgreSQL. It has accounts, transfers between them, and business-rule errors when a transfer isn't allowed.

I scaffolded the Java backend and the small frontend with Claude. My own work is the database, the containers and the Kubernetes setup. The commits below are on `feature/mini-payments-api-skeleton`. It runs on Minikube on my machine. A homelab deploy and AKS are still plans.

## The posts

1. [15 Oct — Kickoff]({{< relref "mini-payments-kickoff.md" >}}). The README states the plan.
2. [24 Oct — App and PostgreSQL]({{< relref "mini-payments-app-and-postgresql.md" >}}). The payments role was missing.
3. [25 Oct — Images, Compose, database manifests]({{< relref "mini-payments-images-and-database-manifests.md" >}}). 825 MB disk down to 402 MB.
4. [26 Oct — Docker Desktop Kubernetes]({{< relref "mini-payments-docker-desktop.md" >}}). Three app replicas, one database replica.
5. [3 Nov — Minikube]({{< relref "mini-payments-minikube.md" >}}). The cluster could not see the host image.
6. [9–10 Nov — ConfigMap and Secret]({{< relref "mini-payments-configmap-and-secret.md" >}}). One Secret, two expected key names.
7. [10 Nov — A volume for Postgres]({{< relref "mini-payments-postgres-volume.md" >}}). A PersistentVolumeClaim on a Deployment.

## Where it stands

The app Deployment has 3 replicas of `mini-payments-api:dev`. Postgres 17 is one replica, still a Deployment, with a 5Gi ReadWriteOnce claim mounted at `/var/lib/postgresql/data`. The database URL and username come from a ConfigMap. The password comes from a Secret. I reach the API with `kubectl port-forward`.

## What I'm learning next

Planned, not built. These are the notes I wrote for the steps after the volume.

**StatefulSet.** A StatefulSet is the controller for a stateful app: a stable pod name, and its own volume per pod. The volume I have does not make the database Deployment a StatefulSet. Raising `replicas` is not how you make Postgres reliable.

**Liveness and readiness probes.** Kubernetes checks the container on a schedule. Readiness decides whether traffic may go to the pod. Liveness decides whether the pod should be restarted.

**Resource requests and limits.** A request is what the scheduler reserves. A limit is the cap on the machine. Without a limit, one pod can use up the node. Without a request, the scheduler cannot place the pod properly.

**Ingress.** An HTTP router into the cluster, in place of port-forward. A LoadBalancer or NodePort service per app does not scale. Ingress is the one front door.

**CI/CD.** A pipeline that builds the image and deploys it, first to my homelab cluster, then to AKS.

**Prometheus and Grafana.** Spring Boot Actuator, with the Micrometer that is already there, collects HTTP requests, memory, threads and database connections. A dependency in `pom.xml` turns those metrics into the text format Prometheus reads. The endpoint still has to be opened: Spring Boot only exposes health over HTTP until then. Grafana is the dashboard in front of that. I check each of these steps with `kubectl describe`, `kubectl logs` and `kubectl get events`.
