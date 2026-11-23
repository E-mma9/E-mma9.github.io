---
title: "Mini Payments: images, Compose, and the database manifests"
date: 2026-10-25T18:15:44Z
series:
  - Mini Payments
series_order: 4
tags: ["mini-payments", "docker", "kubernetes"]
summary: "25 October: a single-stage image, then a multistage image at half the size, Compose without a volume, and the first database manifests."
---

25 October was four commits: a single-stage image, a multistage Dockerfile, Compose, and the first Kubernetes manifests, which were only for the database.

## Single-stage image

The first image wrapped a JAR I had built by hand.

1. `./mvnw package -DskipTests`
2. `docker build -t mini-payments-api:dev .` — `-t` is the name and tag, and the `.` is the build context.
3. Run it, with the database settings as environment variables. `-e` sets a variable, `--rm` removes the container when it stops, and `-p 8080:8080` publishes the port. The app reaches Postgres on the host through `host.docker.internal`. The password is one of those variables. I'm not printing it.

Anyone who wanted to run that image had to compile first, and the image was large.

## Multistage Dockerfile

`docker build` now compiles and packages. The final stage is the image. This is the Dockerfile:

```dockerfile
# stage 1: Building image containing both Maven and Java 21
FROM maven:3.9.9-eclipse-temurin-21 as BUILD

WORKDIR /app

COPY . .

RUN mvn package -DskipTests

# stage 2: runtime
FROM eclipse-temurin:21-jre-alpine as RUNTIME

WORKDIR /app

RUN adduser -S appuser

COPY --from=BUILD /app/target/*-SNAPSHOT.jar app.jar

USER appuser

EXPOSE 8080

ENTRYPOINT [ "java", "-jar", "app.jar" ]
```

Stage 1 is the Maven image with a JDK 21, and `as BUILD` is the name the next stage copies from. `COPY . .` copies the whole project. That is a weak layer: a source change and a dependency change bust the same cache. Copying `pom.xml` first and resolving dependencies in their own layer is the next improvement. For now it is fine.

Stage 2 is a JRE on Alpine, so the runtime image stays small. `adduser -S appuser` is Alpine's command, not the one from the Maven image. `USER appuser` is who the process runs as. `EXPOSE 8080` is documentation. The entrypoint is `java -jar app.jar`.

| Image | Disk usage | Content size |
|---|---|---|
| Single-stage (`test:tag1`) | 825 MB | 265 MB |
| Multistage (`mini-payments-api:dev`) | 402 MB | 128 MB |

A smaller image means faster pulls on a cluster, faster scale-up and a lighter pipeline.

## Compose

`docker-compose.yml` starts PostgreSQL 17 next to the app. The app service uses `build: .`, so Compose builds the Dockerfile and starts the container. `depends_on` waits for the database service. There is no volume on the database: a restart drops the data. The environment variables for both services have to be in the file. I'm not pasting it here, because it contains the database password.

## Database manifests

The same evening I added `k8s/database-deployment.yaml` and `k8s/database-service.yaml`. The Deployment runs `postgres:17`. The Service is named `database`, port 5432, and that name is what the app will connect to.

That first Deployment set `replicas: 3`, and it put the database name, user and password in the pod environment. The password value stays out of this post. The next day I changed the replica count. A Service in front of three Postgres pods that do not share a disk is the problem the next post is about.
