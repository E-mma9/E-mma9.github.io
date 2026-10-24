#!/usr/bin/env bash
# Build the site and check the output.
#   bash scripts/verify-site.sh            build + checks
#   bash scripts/verify-site.sh --deploy   build + checks, then copy public/ to the repo root
set -euo pipefail
cd "$(dirname "$0")/.."

hugo --minify --cleanDestinationDir --destination public --quiet

fail=0

# 1. Forbidden strings (old terminal theme, outdated homelab facts). HTML and RSS/XML output.
forbidden=$(cat <<'EOF'
whoami
~/projects
~/.contact
~/writing
learn out loud
N100
Ceph
VLAN
OPNsense
fail2ban
Fail2ban
ServiceCrashed
ProxmoxStorageWarn
DiskSpaceLow
harden.sh
EOF
)
while IFS= read -r needle; do
  [ -z "$needle" ] && continue
  hits=$(grep -rlF --include='*.html' --include='*.xml' -- "$needle" public || true)
  if [ -n "$hits" ]; then
    echo "FORBIDDEN '$needle' in:"; echo "$hits" | sed 's/^/  /'; fail=1
  fi
done <<< "$forbidden"

# 2. Internal links/sources must resolve to a file under public/.
python3 -I - <<'EOF' || fail=1
import os, re, sys
root = "public"
bad = []
pat = re.compile(r'(?:href|src)="(/[^"#?]*)')
for d, _, files in os.walk(root):
    for f in files:
        if not f.endswith(".html"):
            continue
        p = os.path.join(d, f)
        for m in pat.finditer(open(p, encoding="utf-8", errors="replace").read()):
            target = m.group(1)
            fs = os.path.join(root, target.lstrip("/"))
            if os.path.isdir(fs):
                fs = os.path.join(fs, "index.html")
            if not os.path.isfile(fs):
                bad.append((p, target))
for p, t in bad:
    print(f"DEAD LINK {t} in {p}")
sys.exit(1 if bad else 0)
EOF

# 3. CV present and not a stub.
if [ ! -f public/Emmanuel_Tekle_CV.pdf ] || [ "$(stat -f%z public/Emmanuel_Tekle_CV.pdf)" -lt 4000 ]; then
  echo "CV missing or too small at public/Emmanuel_Tekle_CV.pdf"; fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "FAILED"; exit 1
fi
echo "OK"

# --deploy: GitHub Pages serves the repo root of main, so copy the build there.
# Only generated paths are removed; source dirs (content, layouts, assets, static,
# config, data, docs, scripts) and .nojekyll/.gitignore are never touched.
if [ "${1:-}" = "--deploy" ]; then
  rm -rf about css tags categories posts projects img index.html index.xml sitemap.xml robots.txt
  cp -R public/. .
  echo "DEPLOYED to repo root"
fi
