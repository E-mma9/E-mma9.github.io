---
title: "Mini Payments: the API on Docker Desktop Kubernetes"
date: 2026-10-26T22:24:56Z
series:
  - Mini Payments
series_order: 5
tags: ["mini-payments", "kubernetes", "postgresql"]
summary: "26 October: the app Deployment at 3 replicas and a Service, on Docker Desktop. Postgres cut from 3 replicas to 1."
---

On 26 October I added the app manifests and ran them on the Kubernetes cluster built into Docker Desktop.

`k8s/app-deployment.yaml` runs 3 replicas of `mini-payments-api:dev`. The container listens on 8080. The datasource URL, username and password are environment variables on the pod. The URL is `jdbc:postgresql://database:5432/payments` and the username is `payments`. The password is set the same way. I'm not printing the value.

`k8s/app-service.yaml` is named `app`. It selects those pods and exposes port 8080. Traffic to the Service is spread across the three replicas.

## One database replica

The database Deployment from 25 October asked for 3 replicas. I set it to 1.

Postgres here has no shared disk. Each pod has its own data directory. The Service spreads requests across the pods: the app creates an account through one pod, reads it through another, and gets "not found". A database is stateful. Adding replicas does not make it reliable. That takes a stable identity per pod and a volume per pod, which is a StatefulSet and a PersistentVolumeClaim. On 26 October I have neither, so the database stays at one replica.

## Reaching it

The Services are only inside the cluster. From the laptop:

```bash
kubectl port-forward svc/app 8080:8080
```

To look at the tables, exec into the Postgres pod. The pod I used that day:

```bash
kubectl exec -it database-79d5d77c8b-d8lv9 -- psql -U payments -d payments
```
