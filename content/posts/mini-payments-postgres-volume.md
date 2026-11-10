---
title: "Mini Payments: a volume for Postgres"
date: 2026-11-10T13:14:04Z
series:
  - Mini Payments
series_order: 8
tags: ["mini-payments", "kubernetes", "postgresql"]
summary: "10 November: a 5Gi ReadWriteOnce PersistentVolumeClaim at /var/lib/postgresql/data. The database is still a Deployment, not a StatefulSet."
---

The same day as the ConfigMap, after that fight, I gave Postgres a disk. The commit is "PVC/PV fixed for database".

`k8s/database-pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-pvc
spec:
  resources:
    requests:
      storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
```

The database Deployment mounts that claim at `/var/lib/postgresql/data`:

```yaml
volumeMounts:
  - name: database-storage
    mountPath: /var/lib/postgresql/data
volumes:
  - name: database-storage
    persistentVolumeClaim:
      claimName: database-pvc
```

The object is still a Deployment, `replicas: 1`. A PersistentVolumeClaim is a request for storage. It is not a StatefulSet. A StatefulSet is the controller that gives a stateful app a stable pod name and its own volume per pod. I do not have one.

On this commit I also added `k8s/app-secret.yaml` to `.gitignore`.

## What I'm learning next

Planned, not built.

**StatefulSet.** Stable pod name, own volume per pod. The claim above does not turn this Deployment into one, and raising the replica count still would not.

**Liveness and readiness probes.** Periodic checks. Readiness decides whether the pod receives traffic. Liveness decides whether it is restarted.

**Resource requests and limits.** A request is what the scheduler reserves. A limit is the cap. Without a limit, one pod can use up the node. Without a request, the scheduler cannot place it properly.

**Ingress.** An HTTP router for the cluster, instead of `kubectl port-forward`. A LoadBalancer or NodePort service per app does not scale.

**CI/CD.** Build the image and deploy it, first to the homelab cluster, then to AKS.

**Prometheus and Grafana.** Actuator with Micrometer collects HTTP requests, memory, threads and database connections. A dependency in `pom.xml` turns that into Prometheus text format, and the metrics endpoint has to be exposed. Grafana would be the dashboards. I test each step with `kubectl describe`, `kubectl logs` and `kubectl get events`.
