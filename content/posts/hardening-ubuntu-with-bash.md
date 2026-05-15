---
title: "Hardening Ubuntu with Bash"
date: 2026-03-25
summary: "Two scripts for taking a fresh Ubuntu/Debian box to a defensible baseline."
tags: ["linux", "bash", "security", "ssh", "ufw", "auditd"]
showTableOfContents: true
---

I wrote two Bash scripts to harden a fresh Ubuntu/Debian server and audit it afterwards. Posting the structure and a few notes here.

## What gets configured

`harden.sh`:

- SSH — disable root login, disable password auth, change to a non-default port
- UFW — default-deny, allow SSH/HTTP/HTTPS
- `auditd` for security logging
- `unattended-upgrades` for security patches
- `fail2ban` for brute-force protection

`security-audit.sh`:

- Verifies SSH config against the hardened baseline
- Checks UFW status and rules
- Reports failed logins from `journalctl`
- Lists pending updates
- Exits non-zero on drift (useful for CI / cron)

## Idempotency

Bash idempotency takes a bit of care. Each change is wrapped in a check so the script can be re-run safely:

```bash
ssh_set() {
  local key="$1" val="$2"
  if grep -qE "^${key}[[:space:]]" /etc/ssh/sshd_config; then
    sed -i "s|^${key}.*|${key} ${val}|" /etc/ssh/sshd_config
  else
    echo "${key} ${val}" >> /etc/ssh/sshd_config
  fi
}

ssh_set "PermitRootLogin" "no"
ssh_set "PasswordAuthentication" "no"
ssh_set "Port" "2222"
```

Matching `^${key}[[:space:]]` avoids picking up commented-out lines. The function handles both update and insert in one place.

## The audit script

```bash
check() {
  local desc="$1" cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    echo "  [OK]   $desc"
  else
    echo "  [FAIL] $desc"
    EXIT=1
  fi
}

check "SSH root login disabled" \
  "grep -qE '^PermitRootLogin no' /etc/ssh/sshd_config"
check "SSH password auth disabled" \
  "grep -qE '^PasswordAuthentication no' /etc/ssh/sshd_config"
check "UFW active" "ufw status | grep -q 'Status: active'"
check "auditd running" "systemctl is-active --quiet auditd"
```

`[OK]/[FAIL]` columnar output is easy to pipe into a Slack notification or store in a log.

## When this stops being the right tool

For one server, Bash is fine. For ten, I'd move to Ansible — the inventory and playbook structure pay for themselves. The scripts were a way to get familiar with the actual files and directives. After that, config management makes more sense.

## Repo

[github.com/E-mma9/Linux-Security-Hardening](https://github.com/E-mma9/Linux-Security-Hardening)
