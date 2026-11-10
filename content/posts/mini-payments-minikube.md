---
title: "Mini Payments: Minikube can't see the image"
date: 2026-11-03
series:
  - Mini Payments
series_order: 6
tags: ["mini-payments", "kubernetes", "minikube"]
summary: "3 November: moved to Minikube. The app pods stayed down until minikube image load, then port-forward again."
---

On 3 November I moved the same manifests from Docker Desktop's cluster to Minikube. The app containers would not start. Minikube does not see an image I built on the host until that image is loaded into the cluster.

Build on the host, then load the tag the Deployment already uses:

```bash
docker build -t mini-payments-api:dev .
minikube image load mini-payments-api:dev
```

The Service is still only inside the cluster, so the port-forward is the way onto it:

```bash
kubectl port-forward svc/app 8080:8080
```
