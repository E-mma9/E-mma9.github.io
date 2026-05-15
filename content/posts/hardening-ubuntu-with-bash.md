---
title: "Hardening Ubuntu with Bash, not Ansible"
date: 2026-03-25
summary: "Why I wrote a 200-line Bash hardening script before reaching for a config management tool."
tags: ["linux", "bash", "security", "ssh", "ufw", "auditd"]
showTableOfContents: true
---

## The temptation to over-engineer

When I started thinking about hardening fresh Ubuntu servers, the obvious answer was Ansible. I already use Ansible for other things. There are battle-tested roles like `dev-sec/ansible-collection-hardening`. Done in an afternoon.

I wrote Bash instead. Here's why.

## The skill gap I was actually closing

Ansible abstracts away *what's happening on the box.* When the role finishes and SSH is hardened, you know the outcome, but you don't always know which file got edited and which line changed. For my own learning, I needed to actually touch:

- `/etc/ssh/sshd_config` — change `PermitRootLogin`, `PasswordAuthentication`, `Port`
- `/etc/default/ufw` — set default-deny
- `/etc/audit/rules.d/audit.rules` — define what to audit
- `/etc/apt/apt.conf.d/50unattended-upgrades` — security-only auto-updates

I needed to know the file, the directive, and why it matters. Ansible would have hidden all three.

## The script structure

Two scripts, both idempotent:

```
harden.sh         # apply baseline
security-audit.sh # verify baseline
```

Idempotency in Bash isn't free. Every change is wrapped in a check:

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

Two patterns to notice: matching the key with `^${key}[[:space:]]` avoids matching commented-out duplicates, and the function handles both update and insert. Running the script twice produces the same file.

## The audit script earns its keep

`security-audit.sh` reads the same baseline and reports drift. Exit code 0 = compliant, 1 = drift. That makes it CI-friendly.

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

The `[OK]/[FAIL]` columnar output is intentional — I can pipe it into a Slack notification when I run it on a schedule.

## When to switch to Ansible

For *one* server, Bash is faster and clearer. For ten, I'd switch — the inventory and the playbook structure are worth the abstraction tax. The script taught me the *what.* Ansible would have only taught me the *how.*

## Repo

[github.com/E-mma9/Linux-Security-Hardening](https://github.com/E-mma9/Linux-Security-Hardening)
