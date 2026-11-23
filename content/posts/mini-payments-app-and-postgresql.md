---
title: "Mini Payments: app and PostgreSQL"
date: 2026-10-24
series:
  - Mini Payments
series_order: 3
tags: ["mini-payments", "postgresql", "spring-boot"]
summary: "24 October: Claude scaffolded the Java and the frontend. PostgreSQL 17 is my work, including the missing payments role."
---

The commit on 24 October is the base build. The message on it is blunt: the backend and the frontend were built by Claude, and I made the PostgreSQL database myself. That split is the point. I am practising the platform side.

The API is Java 21 and Spring Boot. It has accounts, transfers between them, and business-rule errors when a transfer is not allowed. Flyway applies `V1__create_accounts_and_transfers.sql`, so the schema is built the same way every time. The database is PostgreSQL 17.

`./mvnw test` runs the tests. `./mvnw spring-boot:run` starts the app, and it will not stay up without the database.

## The payments role

The first database container did not create the `payments` role, so Postgres never became usable and Spring Boot, which waits on it, did not start either. I had passed `POSTGRES_USERS` instead of `POSTGRES_USER`. The image does not invent that role. It creates the role from `POSTGRES_USER`.

I removed the container and created it again with `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB` set, plus a named volume (`payments-data` mounted at `/var/lib/postgresql/data`) so the data survives a restart. I'm not putting the password in this post. The database name and the role are both `payments`.

From the host, with the app in a second terminal:

```bash
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/payments \
SPRING_DATASOURCE_USERNAME=payments \
./mvnw spring-boot:run
```

And into the database:

```bash
psql -h localhost -U payments -d payments
```

The commands I actually use in `psql`:

| Command | What it does |
|---|---|
| `\conninfo` | Which database and user am I connected as? |
| `\dt` | List the tables |
| `\d accounts` | Columns, constraints and indexes of a table |
| `\di` | List the indexes |
| `\x` | Toggle expanded rows |
| `\q` | Quit |

When the app fails to start, check the dependency it is waiting on before debugging the app.
