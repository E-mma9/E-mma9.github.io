# Portfolio redesign: "clean corporate" — design

Date: 2026-10-24
Site: https://emmanueltekle.nl (Hugo, GitHub Pages, repo `E-mma9/E-mma9.github.io`)
Owner: Emmanuel Tekle

## Intent

Emmanuel's site must convince recruiters and hiring managers at large
companies and fintechs, within thirty seconds, that he is a young, ambitious
engineer with drive who actually ships things. He is available full-time
February–July 2027 and positions himself as a DevOps / Platform Engineer
heading for DevSecOps.

The current site is out of date (still lists Livio as current job, no JUICT
internship, no AZ-104) and its terminal/homelab aesthetic reads as "hobbyist",
not "engineer a bank would hire". This redesign updates both content and
look.

## Source of truth for facts

The new CV at `Emmanuel_Tekle_CV_DevOps_Platform.pdf` (repo root, untracked
at time of writing) is **leading** over LinkedIn wherever they disagree:

- Livio: Systems Administrator, Apr 2025 – Aug 2026.
- JUICT: Automation & Infrastructure Intern, Sep 2026 – Jan 2027.
- Saxion average 7.1, year 3, graduating Jul 2028 (expected).
- Availability: Feb – Jul 2027, full-time.

Copy on the site is drawn from the CV wording. Do not invent facts, numbers
or client names that are not in the CV or in the public GitHub repos.

For the homelab hardware and the monitoring stack, the **Monitoring-Homelab
repo README and `docs/architecture.md` are leading** over the CV, the
existing site and the blog posts (Emmanuel confirmed this). For each
project page, the linked repo at HEAD is leading over the CV: the page must
never claim something a reviewer cannot see in the repo.

## Goals

1. A recruiter lands on the homepage and immediately sees: who he is, that
   he is Azure-certified, that he is available Feb–Jul 2027, and one
   headline achievement (the AI support agent in production).
2. Experience, projects, certifications and a CV download are reachable
   without scrolling hunts; CV download is one click from every page.
3. Projects show real evidence: screenshots and diagrams from the public
   repos, not just prose.
4. Site looks professional, light and calm; works on phone and desktop.

## Non-goals

- No CMS, no JavaScript framework, no new hosting. Stay on Hugo + GitHub
  Pages with the current deploy model (build output committed to repo root).
- No Dutch translation; the site stays English (the CV is English and the
  target companies recruit in English).
- No rewriting of the three existing blog posts for tone or structure.
  Factual corrections (see "Blog posts") are in scope.
- No dark mode toggle. A single light theme is enough; honour
  `prefers-color-scheme` only if it costs nothing.

## Anti-goals (what would make this a failure)

- Reads like a student hobby page: terminal prompts, blinking cursors,
  grid backgrounds, "learning out loud" copy.
- Leaks anything about JUICT clients beyond what the CV already says.
- Stale again in a month because facts are scattered: all biographical
  facts live in one place (`config/_default/hugo.toml` params or a single
  data file), templates read from there.
- Broken on mobile, or a Lighthouse score that embarrasses a platform
  engineer (target: 95+ on performance, accessibility, best practices, SEO).

## Visual direction (chosen: option A, "clean corporate")

Emmanuel chose this over a dark-professional variant and over keeping the
terminal style.

- Background white `#ffffff`, text slate `#0f172a`, secondary text
  `#475569`, borders `#e2e8f0`, soft panels `#f8fafc`.
- One accent colour: navy/blue `#1d4ed8` (hover `#1e40af`). Used for the
  primary button, links, the availability badge and small highlights only.
- Typeface: Inter for everything. Monospace (JetBrains Mono) only inside
  code blocks and the terminal-output block on the hardening project page.
- No gradients, no glow, no background grid, no `$ prompt` decorations, no
  blinking cursor.
- Max content width about 760px for text pages; the homepage may use a
  wider container (about 960px) for the stats row and project grid.
- Cards: 1px border, 10–12px radius, subtle hover (border darkens, slight
  lift). Nothing heavier.
- Mobile: single column, 16px side gutter, no horizontal scroll.

The mockup Emmanuel approved is in
`.superpowers/brainstorm/70950-1792847683/content/visual-style.html`, card A
(gitignored; copy of the relevant markup is reproduced in spirit below).

## Site map

| Path | Purpose |
|------|---------|
| `/` | Homepage: pitch, stats, experience, projects, certifications, education, contact |
| `/projects/` | Project list |
| `/projects/<slug>/` | One page per project (five, see below) |
| `/posts/` | Writing list (unchanged content, new style) |
| `/posts/<slug>/` | Blog posts (unchanged content, new style) |
| `/Emmanuel_Tekle_CV.pdf` | CV download (the new CV, replacing the old file under the same filename so existing links keep working) |

The separate `/about/` page is removed; its content merges into the
homepage. Add a redirect-style stub if easy (`<meta refresh>` to `/`), else
just delete it and remove it from nav.

Navigation on every page: name/logo left; right: **Work** (anchor to the
experience section on the homepage), **Projects**, **Writing**, and a
visually distinct **CV ↓** button (opens the PDF in a new tab).

Footer: © year, Enschede NL, links email · GitHub · LinkedIn · CV · RSS.

## Homepage, top to bottom

1. **Hero**
   - Badge: `● Available Feb – Jul 2027 · full-time` (green dot, navy pill).
   - H1: "DevOps & Platform Engineer in the making."
   - Lead (2 sentences, from CV profile): "Azure-certified (AZ-104) student
     at Saxion who ships production systems while studying. Designed and
     built, solo, an AI support agent that now handles every new ticket for
     ~50 client organisations of a managed service provider."
   - Buttons: primary **Download CV**, secondary **Get in touch** (anchor to
     contact form). Small inline links: GitHub · LinkedIn.
2. **Three stats** (equal cards):
   - `AZ-104` / Microsoft Certified, Oct 2026
   - `2 yrs` / hands-on production experience
   - `7 weeks` / AI agent from idea to production
3. **Experience** (section id `work`), timeline list, newest first. Each
   entry: role, company, location, dates, two bullets taken from the CV.
   - Automation & Infrastructure Intern · JUICT B.V. (managed service
     provider) · Haaksbergen · Sep 2026 – Jan 2027
   - Systems Administrator · Livio (healthcare) · Enschede · Apr 2025 – Aug 2026
   - Studentaanhuis and TotalEnergies are deliberately omitted.
4. **Selected projects**: four cards in a 2×2 grid (1 column on mobile),
   each with a thumbnail, title, one-line summary, tech tags, link to its
   project page. Order: AI support agent, Mini Payments API, Monitoring
   Homelab, Linux Security Hardening. Link "All projects →".
5. **Certifications**: AZ-104 as the hero entry with the certificate image
   (cropped/scaled from the screenshot now at repo root, renamed to
   `static/img/az-104-certificate.png`), credential ID `4C620F71E4B4DAAC`,
   earned 22 Oct 2026, expires 23 Oct 2027, and a "Verify on Microsoft
   Learn" link to
   `https://learn.microsoft.com/api/credentials/share/en-us/EmmanuelTekle/4C620F71E4B4DAAC`
   (builder: if that URL pattern does not resolve, fall back to a plain text
   credential ID without a link; do not guess another URL).
   Below it, two "planned" rows in muted style: HashiCorp Terraform
   Associate (exam Nov 2026), Certified Kubernetes Administrator (exam Jan
   2027).
6. **Education & beyond work**: Saxion, Bachelor Cybersecurity & Cloud
   Engineering, Sep 2024 – Jul 2028 (expected), year 3, with the three
   named grades (Virtualisation 10, Public & Hybrid Cloud 9, Automated
   Infrastructures 9). One sentence: "Outside work: competitive kickboxing
   (B-class, 9–1) and speedcubing (Dutch top 20, 2019)."
7. **Latest writing**: three most recent posts, compact list.
8. **Contact**: short heading "Get in touch", the existing Formspree form
   (action URL unchanged), plus email link. Keep "replies within 24h".

## Project pages

Each project page: title, one-line summary, meta (date range, status),
tech tags, GitHub link button when a public repo exists, body, images.

### 1. AI support agent in production (JUICT)
- No public repo; no GitHub button. No images (nothing public). Builder may
  draw a simple inline SVG architecture sketch from the components named in
  the CV (portal/ticket → Service Bus → Container Apps job → read-only tools
  → diagnosis note); keep it generic, no client names.
- Body = the three CV bullets, lightly expanded into short paragraphs:
  what it does and the numbers; platform as code and the pipeline; security
  by design. Mention the second (sales) agent as "in design".
- Status: Live since Oct 2026.

### 2. Mini Payments API — Spring Boot on Kubernetes
- Repo: https://github.com/E-mma9/mini-payments-api (public).
- Body, matching the repo at HEAD: Spring Boot service with accounts and
  transfers, PostgreSQL via Flyway migrations, unit and integration tests
  (Maven). "Next" list: Docker multi-stage build, Kubernetes manifests,
  GitHub Actions with Trivy, AKS via Terraform, Prometheus metrics. The CV
  lists the Docker build as done but the repo has no Dockerfile yet, so the
  site puts it under "next" (my call; move it to "done" once the Dockerfile
  is pushed). Mark the project clearly "in progress, Oct 2026".
- No images yet.

### 3. Monitoring Homelab — production-style observability
- Repo: https://github.com/E-mma9/Monitoring-Homelab (public, complete).
- Images, copied from the repo into `static/img/projects/monitoring/`
  (all PNG, optimise to ≤300KB each; use `<img loading="lazy">` with
  width/height attributes):
  - `pipeline.png` (repo `docs/image.png`, 1376×768): monitoring data-flow
    diagram. Hero image for this page and thumbnail on the homepage card.
  - `grafana-cluster-overview.png` (1541×730).
  - `prometheus-alert-rules.png` (repo `Screenshots/prometheus-targets.png`,
    943×907, actually shows the seven alert rules).
  - `pagerduty-incident.png` (1918×1382).
  - `proxmox-cluster.png` (repo `Schematics/ProxmoxCluster.png`, 1376×768).
  - The Alertmanager, Blackbox and PagerDuty service-directory screenshots
    are optional; include only if they fit cleanly.
- Body: keep the existing page content (what runs, the seven alert rules,
  PagerDuty escalation) and add a short "The cluster underneath" section
  with the Proxmox diagram: three nodes, Proxmox VE with HA, Tailscale
  mesh, no ports exposed. Correct the existing page where it contradicts
  the repo README (the README is right: no Ceph, no VLANs; alert list is
  NodeDown, DiskSpaceWarning, DiskSpaceCritical, HighMemoryUsage,
  HighCPUUsage, EndpointDown, SlowResponse).

### 4. Linux Security Hardening
- Repo: https://github.com/E-mma9/Linux-Security-Hardening (public).
- No images in the repo. Instead render the example output from
  `tests/output-example.txt` as a styled terminal block (dark panel,
  monospace, green check marks) showing the audit result: SSH config
  (port 2222, no root login, no password auth), UFW status, failed login
  listing. Shorten to the interesting ~20 lines.
- Body: rewrite to match what the scripts actually do (repo is leading).
  `harden-server.sh`: system updates + unattended-upgrades, SSH hardening
  (no root login, no password auth, port 2222), UFW default-deny with
  SSH/HTTP/HTTPS, auditd, then runs the audit. `Security-audit.sh`: prints
  SSH config, UFW status, failed SSH logins, pending updates. Remove the
  existing claims about Fail2ban and CI exit codes; they are not in the
  scripts. Fix script names to match the repo.

### 5. Homelab platform (optional, builder's call)
The CV lists "Homelab — 3-node Proxmox VE cluster" separately from the
monitoring project. The site folds it into the Monitoring Homelab page
("The cluster underneath"). Do not create a fifth page unless it has
content that is not already on page 3.

## Blog posts (factual corrections only)

The three posts under `content/posts/` keep their titles, URLs, tone and
structure, but every fact that contradicts the Monitoring-Homelab repo or
the hardening repo is corrected:

- `why-i-run-a-proxmox-cluster.md`: hardware is Dell OptiPlex / HP ProDesk
  (Intel i5; 16 GB on `pve`, 8 GB on `node2` and `node3`; NVMe/SSD OS
  disks, 931 GB HDD ZFS pool on `pve`), Proxmox VE 9 with HA, local
  storage only (no Ceph; HA failover copies the disk), bridged networking
  on one LAN (no VLANs, no OPNsense), Tailscale for remote access, no
  ports exposed. Remove the N100 / price / jumbo-frame claims.
- `building-a-monitoring-stack-from-scratch.md`: alert names and
  thresholds as in the README (NodeDown, DiskSpaceWarning,
  DiskSpaceCritical, HighMemoryUsage, HighCPUUsage, EndpointDown,
  SlowResponse); scrape interval 15s; PagerDuty text then phone call.
- `hardening-ubuntu-with-bash.md`: script names `harden-server.sh` and
  `Security-audit.sh`; drop Fail2ban and exit-code claims.

If a sentence cannot be corrected without inventing something, delete the
sentence rather than guess.

## Content facts to centralise

Put in `config/_default/hugo.toml` `[params]` (or `data/profile.toml`):
name, headline, availability text, email, GitHub, LinkedIn, CV path,
location, stats, certifications (name, issuer, date, status, credential
ID, verify URL, image), experience entries, education. The homepage
template renders from these; project pages stay as Markdown content.

## Deploy model (unchanged, must keep working)

GitHub Pages serves the **repo root of `main`**. Build procedure:

```
hugo --minify
cp -R public/* .
```

then commit source and output together. `public/` and `resources/_gen/`
stay gitignored; `.nojekyll` and `CNAME` stay at root. Hugo is not
installed on this machine at the time of writing (last build used Hugo
0.140.0-DEV); install via Homebrew (`brew install hugo`) before building.

Stale generated files from the old site (`about/index.html`, old
fingerprinted CSS under `css/`, tag pages for removed tags) must be removed
from the repo root when the new build is copied in, so the deployed site
has no orphan pages.

## Files to add / replace

- `static/Emmanuel_Tekle_CV.pdf` ← `Emmanuel_Tekle_CV_DevOps_Platform.pdf`
  (then delete the untracked copy at repo root and the old root-level
  `Emmanuel_Tekle_CV.pdf`, which is a stale build artefact).
- `static/img/az-104-certificate.png` ← the screenshot now at repo root
  (`Scherm­afbeelding 2026-10-22 om 14.53.53.png`); crop to the dark
  certificate card, drop the blue border, scale to ≤1200px wide. Delete the
  original from the repo root.
- `static/img/projects/monitoring/*.png` as listed above.
- `assets/img/avatar.jpg` is unused; remove it and its placeholder note.

## Constraints

- Work on branch `feature/portfolio-redesign`, open a PR to `main`; never
  push to `main` directly.
- Keep the GoatCounter snippet (production only) and both RSS feeds.
- Keep the Formspree form action and the hidden `_subject` field.
- No external JS libraries. Google Fonts for Inter is acceptable (already
  used); self-hosting is a nice-to-have, not required.
- Keep the existing `[permalinks]` so blog and project URLs do not change.

## Left to the builder

- Exact CSS values, spacing, responsive breakpoints.
- Whether the homepage is one `layouts/index.html` with partials per section
  or inline; partials preferred.
- Thumbnail choice for the AI agent and Mini Payments cards (a neutral
  icon/illustration in the accent colour is fine; no stock photos).
- Image optimisation tooling (ImageMagick/`sips` on macOS both fine).
- Whether to keep tag pages at all; they add nothing for recruiters and
  may be disabled (`disableKinds = ["taxonomy", "term"]`) if nothing links
  to them.
