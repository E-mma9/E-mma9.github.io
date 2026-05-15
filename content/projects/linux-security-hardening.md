---
title: "Linux Security Hardening"
date: 2026-03-20
summary: "Two Bash scripts that harden a fresh Ubuntu/Debian box and audit it afterwards."
tags: ["linux", "bash", "ssh", "ufw", "auditd", "security", "ubuntu", "debian"]
externalUrl: "https://github.com/E-mma9/Linux-Security-Hardening"
showHero: false
---

Two Bash scripts that take a freshly-installed Ubuntu or Debian server and harden it to a sensible baseline, then audit the result.

## What it does

**`harden.sh`**

- SSH hardening — no root login, no password auth, non-default port
- UFW firewall — default-deny, only SSH/HTTP/HTTPS open
- `auditd` installed and configured for security logging
- `unattended-upgrades` enabled for security patches
- Fail2ban for brute-force protection

**`security-audit.sh`**

- Verifies SSH config matches hardened baseline
- Checks firewall rules
- Reports failed login attempts from `journalctl`
- Lists pending updates
- Exit code reflects pass/fail for CI integration

## Why

Wrote this to practice basic Linux admin and server-side security hands-on. The scripts are short and readable on purpose — every line is something I'd be able to defend in an interview.

## Repo

[github.com/E-mma9/Linux-Security-Hardening](https://github.com/E-mma9/Linux-Security-Hardening)
