---
title: "Mini Payments: ConfigMap and Secret"
date: 2026-11-10T09:46:38Z
series:
  - Mini Payments
series_order: 7
tags: ["mini-payments", "kubernetes"]
summary: "9–10 November: database URL and username in a ConfigMap, the password in a Secret. One Secret with two expected key names, about two hours, then a 20-minute Flyway startup order."
---

9 and 10 November were the ConfigMap and the Secret. A ConfigMap holds the non-secret settings, the database URL and the username, outside the Deployment and outside the image. The same image can then start with different values. The password goes in a Secret.

The app reads both with `envFrom`:

```yaml
envFrom:
  - configMapRef:
      name: mini-payments-config
  - secretRef:
      name: mini-payments-secrets
```

`k8s/app-configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mini-payments-config
data:
  SPRING_DATASOURCE_URL: "jdbc:postgresql://database:5432/payments"
  SPRING_DATASOURCE_USERNAME: "payments"
```

The database Deployment no longer carries the password as a plain value. It reads one key from the same Secret:

```yaml
- name: POSTGRES_PASSWORD
  valueFrom:
    secretKeyRef:
      name: mini-payments-secrets
      key: SPRING_DATASOURCE_PASSWORD
```

The Secret manifest itself is not in this post.

## What broke

This took about an hour and a half to two hours.

- The YAML indentation was wrong. A field was a sibling when it needed to be a child, or the other way around.
- `kubectl describe` on the pod shows where each environment variable comes from.
- `kubectl logs`, and the output of a rollout, is where the error shows up. Mine was `unknown field "envFrom[0].name"`. `name` was sitting directly on the `envFrom` entry. It belongs under `configMapRef` or `secretRef`.

Those were symptoms. The design mistake under them was one Secret whose keys did not match what the two containers expected. The database wanted a different key name from the app, so the references did not line up. The wiring above is the fix: the app consumes the Secret as environment variables, and the database maps `POSTGRES_PASSWORD` to the key `SPRING_DATASOURCE_PASSWORD`.

A note I wrote next to that, about how this usually works once it leaves a laptop: in production the database is typically outside the cluster, a managed service, with managed identity. Mini Payments is not that. The database pod is still in the cluster.

## Flyway, 20 minutes

Starting the database while the app was already running left the app holding a connection to the old database, so the Flyway migration did not run. The database has to be up before the app, or come up with it.
