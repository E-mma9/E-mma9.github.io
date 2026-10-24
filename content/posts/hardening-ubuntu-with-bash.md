---
title: "Hardening Ubuntu with Bash"
date: 2026-03-25
summary: "Two scripts for taking a fresh Ubuntu/Debian box to a defensible baseline."
tags: ["linux", "bash", "security", "ssh", "ufw", "auditd"]
showTableOfContents: true
---

I wrote two Bash scripts to harden a fresh Ubuntu/Debian server and audit it afterwards. Posting the structure and a few notes here.

## What gets configured

`harden-server.sh`:

- System updates, with `unattended-upgrades` enabled for security patches
- SSH — disable root login, disable password auth, move to port 2222
- UFW — default-deny incoming, allow 2222/80/443
- `auditd` installed and enabled for security logging

`Security-audit.sh`:

- Prints the active SSH settings for `Port`, `PermitRootLogin` and `PasswordAuthentication`
- Shows UFW status and rules
- Lists failed SSH logins from `auth.log`
- Lists packages with pending updates

## Keeping it simple

The SSH changes are three `sed` one-liners:

```bash
sed -i 's/^#\?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?Port .*/Port 2222/' /etc/ssh/sshd_config
```

The `^#\?` matches both the commented default and an existing value, so the line gets replaced either way. `ufw` skips rules that already exist. Together that makes the script safe to re-run.

## The audit script

The audit is deliberately plain: show the state, let a human read it.

```bash
grep -E '^(Port|PermitRootLogin|PasswordAuthentication)' /etc/ssh/sshd_config
ufw status verbose
grep "Failed password" /var/log/auth.log | tail -20
apt list --upgradable
```

The next step is turning each line into an `[OK]`/`[FAIL]` check with an exit code, so it can run from cron or CI and fail loudly on drift.

## When this stops being the right tool

For one server, Bash is fine. For ten, I'd move to Ansible — the inventory and playbook structure pay for themselves. The scripts were a way to get familiar with the actual files and directives. After that, config management makes more sense.

## Repo

[github.com/E-mma9/Linux-Security-Hardening](https://github.com/E-mma9/Linux-Security-Hardening)
