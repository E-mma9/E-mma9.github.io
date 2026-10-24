---
title: "Linux Security Hardening"
date: 2026-04-20
period: "Nov 2025 – Apr 2026"
status: done
weight: 40
icon: shield
summary: "Two Bash scripts that bring a fresh Ubuntu/Debian server to a sensible baseline and audit the result."
tech: ["Bash", "Ubuntu", "SSH", "UFW", "auditd"]
repo: "https://github.com/E-mma9/Linux-Security-Hardening"
---

Two short Bash scripts: one hardens a freshly installed Ubuntu or Debian server, the other reports on the result. Tested on Ubuntu LTS.

## What `harden-server.sh` does

1. Updates the system and enables `unattended-upgrades` for automatic security patches.
2. Hardens SSH: no root login, no password authentication, port moved to 2222.
3. Configures UFW: default deny incoming, allow outgoing, open only 2222, 80 and 443.
4. Installs and enables `auditd` for security event logging.

## What `Security-audit.sh` reports

- The active SSH settings for `Port`, `PermitRootLogin` and `PasswordAuthentication`.
- UFW status and rules.
- Failed SSH login attempts from `auth.log`.
- Packages with pending updates.

## Audit output

{{< terminal title="sudo ./Security-audit.sh" >}}
Linux Security Audit

 SSH configuration:
✓ Port 2222
✓ PermitRootLogin no
✓ PasswordAuthentication no

UFW firewall status:
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)

To                         Action      From
--                         ------      ----
2222/tcp                   ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere

 Failed SSH login attempts (last 24h):
sshd[2376]: Failed password for project from 192.168.159.1 port 30414 ssh2
sshd[4581]: Failed password for project from 192.168.159.1 port 30543 ssh2

 Audit Complete
{{< /terminal >}}

## Why

I wrote these to practice Linux administration and server-side security hands-on. The scripts are short and readable on purpose: every line is something I can explain and defend.

## What I'd do next

For one server, Bash is fine. For ten, this becomes an Ansible playbook with an inventory, and the audit becomes a set of `[OK]`/`[FAIL]` checks with an exit code so it can run from cron or CI.
