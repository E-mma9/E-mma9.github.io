# Portfolio Redesign ("clean corporate") Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild emmanueltekle.nl as a light, professional Hugo site whose homepage sells Emmanuel to fintech/corporate recruiters in thirty seconds, with content taken from the new CV and the public GitHub repos.

**Architecture:** Same Hugo site, same deploy model (build output committed at repo root). All biographical facts move into `data/profile.yaml`; `layouts/index.html` composes homepage partials that read from it. Projects and posts stay Markdown under `content/`. One CSS file, rewritten for the light theme. A verification script builds the site and asserts on the output so every task has a checkable result.

**Tech Stack:** Hugo (extended, via Homebrew), Go templates, plain CSS, Inter from Google Fonts, `sips` for image work, bash + python3 for verification. No JS libraries.

**Spec:** `docs/superpowers/specs/2026-10-24-portfolio-redesign-design.md`

## Global Constraints

- Branch `feature/portfolio-redesign`; PR to `main`; never push to `main`.
- Facts: CV is leading over LinkedIn; Monitoring-Homelab repo README/`docs/architecture.md` is leading over CV/site/posts for homelab + monitoring; each project page must not claim anything not visible in the linked repo at HEAD.
- Site language English. No client names beyond what the CV says ("~50 client organisations", "~200 client organisations").
- Palette: bg `#ffffff`, text `#0f172a`, text-2 `#475569`, border `#e2e8f0`, panel `#f8fafc`, accent `#1d4ed8`, accent-hover `#1e40af`. Font Inter; monospace only in code blocks and the terminal block.
- Forbidden on any rendered page: `$ whoami`, `$ ls`, `$ cat`, `$ tail`, `$ echo`, blinking cursor, background grid, "learn out loud", "N100", "Ceph", "VLAN", "OPNsense", "fail2ban", "Fail2ban", "ServiceCrashed", "ProxmoxStorageWarn", "DiskSpaceLow", "harden.sh".
- Keep: GoatCounter snippet (production only), both RSS feeds, Formspree action `https://formspree.io/f/xaqlbeoa` with hidden `_subject`, `[permalinks]` for posts/projects, `CNAME`, `.nojekyll`.
- CV served at `/Emmanuel_Tekle_CV.pdf` (new content, same filename).
- Mobile: single column, 16px gutter, no horizontal scroll. Lighthouse target 95+ (checked manually at the end, not automated).
- Commit messages end with the attribution trailer given in the session.

## Review Focus

1. Phone width (375px): the stats row, the 2×2 project grid and the contact form's two-column name/email row must collapse to one column without horizontal scroll. Test added in Task 4 (CSS has the three `@media (max-width: 640px)` rules).
2. A planned certification has no image and no credential ID; the template must render it without an empty `<img>` or a dangling "Credential ID" label. Test in Task 6.
3. External links (GitHub, LinkedIn, CV, verify URL) open in a new tab with `rel="noopener noreferrer"`; internal anchors (`#work`, `#contact`) stay same-tab. Test in Task 6.
4. Every `<img>` under `static/img/projects/` is referenced with `width`/`height` and `loading="lazy"` so the page does not jump while loading. Test in Task 7.
5. The old `/about/` URL must still resolve (alias to `/`) and no stale generated page (old `css/main.min.*.css`, `tags/*`, `categories/*`, `about/index.html` from the old build) remains in the repo root after deploy. Test in Task 10.

---

### Task 1: Toolchain and verification script

**Files:**
- Create: `scripts/verify-site.sh`
- Modify: `.gitignore` (add nothing new unless needed; `public/` already ignored)

**Interfaces:**
- Produces: `scripts/verify-site.sh` — builds with `hugo --minify --destination public`, then runs the checks below against `public/`. Exit 0 = pass. Later tasks add lines to its FORBIDDEN list and link checks as they go; the script is the test harness for the whole plan.

- [ ] **Step 1: Install Hugo**

Run: `brew install hugo && hugo version`
Expected: a line starting `hugo v0.1` and containing `extended`.

- [ ] **Step 2: Build the current site to prove the toolchain works**

Run: `cd /Users/emmanuel/Private-Projects/E-mma9.github.io && hugo --minify --destination public && ls public/index.html`
Expected: build succeeds (warnings allowed), `public/index.html` exists.

- [ ] **Step 3: Write `scripts/verify-site.sh`**

Bash, `set -euo pipefail`, run from repo root. It must:
1. `hugo --minify --destination public --quiet`.
2. Fail if any file under `public/` matching `*.html` contains any string from the Global Constraints forbidden list (use `grep -rlF` with a here-doc list; print offending file + string).
3. Fail if any `href="/..."` or `src="/..."` in `public/**/*.html` points to a path that does not exist under `public/` (python3 -I one-file script inline via heredoc is fine; ignore `http`, `mailto`, `#`, and `index.xml`-style feed links only if the file exists).
4. Fail if `public/Emmanuel_Tekle_CV.pdf` is missing or smaller than 4000 bytes.
5. Print `OK` at the end.

- [ ] **Step 4: Run it against the current site and confirm it fails on the forbidden list**

Run: `bash scripts/verify-site.sh; echo "exit=$?"`
Expected: non-zero exit; output names `public/index.html` with `$ whoami` (or similar). This proves the check works.

- [ ] **Step 5: Commit**

```bash
git add scripts/verify-site.sh
git commit -m "chore: add site verification script (build, forbidden strings, dead links)"
```

---

### Task 2: Assets — CV, certificate image, project images

**Files:**
- Replace: `static/Emmanuel_Tekle_CV.pdf` (content of `Emmanuel_Tekle_CV_DevOps_Platform.pdf`)
- Create: `static/img/az-104-certificate.png`
- Create: `static/img/projects/monitoring/{pipeline,grafana-cluster-overview,prometheus-alert-rules,pagerduty-incident,proxmox-cluster}.png`
- Delete: `Emmanuel_Tekle_CV_DevOps_Platform.pdf` (root), `Emmanuel_Tekle_CV.pdf` (root, old build artefact), `Scherm­afbeelding 2026-10-22 om 14.53.53.png` (root), `assets/img/avatar.jpg`, `assets/img/avatar.jpg.PLACEHOLDER.md`

**Interfaces:**
- Produces: image paths above, referenced by Tasks 6 and 7. Dimensions after processing must be recorded in `data/profile.yaml` (cert) and project front matter (Task 7) as `width`/`height`.

- [ ] **Step 1: Move the CV into place and remove the root copies**

```bash
cp Emmanuel_Tekle_CV_DevOps_Platform.pdf static/Emmanuel_Tekle_CV.pdf
git rm -q Emmanuel_Tekle_CV.pdf
rm Emmanuel_Tekle_CV_DevOps_Platform.pdf
```

- [ ] **Step 2: Crop and scale the certificate screenshot**

The screenshot is 1570×1144 with a blue patterned border; the dark certificate card occupies roughly x 128–1432, y 128–1012. Crop to the card, scale to 1200px wide:

```bash
mkdir -p static/img/projects/monitoring
sips -c 884 1304 --cropOffset 128 128 "Scherm­afbeelding 2026-10-22 om 14.53.53.png" --out static/img/az-104-certificate.png
sips --resampleWidth 1200 static/img/az-104-certificate.png
sips -g pixelWidth -g pixelHeight static/img/az-104-certificate.png
```
Then open the result (`open static/img/az-104-certificate.png`) and confirm no blue border remains; adjust offsets if needed. Record the final width/height. Delete the original: `rm "Scherm­afbeelding 2026-10-22 om 14.53.53.png"`.

- [ ] **Step 3: Download and optimise the monitoring images**

Source: `https://raw.githubusercontent.com/E-mma9/Monitoring-Homelab/HEAD/` + path. Mapping:

| target | source path |
|---|---|
| `pipeline.png` | `docs/image.png` |
| `grafana-cluster-overview.png` | `Screenshots/grafana-cluster-overview.png` |
| `prometheus-alert-rules.png` | `Screenshots/prometheus-targets.png` |
| `pagerduty-incident.png` | `Screenshots/pagerduty-incident.png` |
| `proxmox-cluster.png` | `Schematics/ProxmoxCluster.png` |

Download into a fresh scratchpad directory, then `sips --resampleWidth 1400` on anything wider than 1400px, then copy into `static/img/projects/monitoring/`. Record each file's final pixel width/height (`sips -g pixelWidth -g pixelHeight`) in a note for Task 7.

- [ ] **Step 4: Verify sizes**

Run: `ls -l static/img/projects/monitoring/ static/img/az-104-certificate.png`
Expected: every file ≤ 300 KB. If one is larger, `sips --resampleWidth 1200` it again or `sips -s format png -s formatOptions low`.

- [ ] **Step 5: Remove the unused avatar**

```bash
git rm -q assets/img/avatar.jpg assets/img/avatar.jpg.PLACEHOLDER.md
```

- [ ] **Step 6: Commit**

```bash
git add static/ assets/
git commit -m "assets: new CV, AZ-104 certificate, monitoring project images"
```

---

### Task 3: Profile data and site config

**Files:**
- Create: `data/profile.yaml`
- Modify: `config/_default/hugo.toml`

**Interfaces:**
- Produces: `site.Data.profile` with the exact keys below; Tasks 5, 6 read them. `site.Params` keeps `author`, `email`, `github`, `linkedin`, `cv`, `location`, `goatcounter`, `description`.

- [ ] **Step 1: Write `data/profile.yaml`**

```yaml
name: Emmanuel Tekle
headline: "DevOps & Platform Engineer in the making."
availability: "Available Feb – Jul 2027 · full-time"
lead: >-
  Azure-certified (AZ-104) student at Saxion who ships production systems
  while studying. Designed and built, solo, an AI support agent that now
  handles every new ticket for ~50 client organisations of a managed
  service provider.
stats:
  - value: "AZ-104"
    label: "Microsoft Certified, Oct 2026"
  - value: "2 yrs"
    label: "hands-on production experience"
  - value: "7 weeks"
    label: "AI agent from idea to production"
experience:
  - role: "Automation & Infrastructure Intern"
    company: "JUICT B.V."
    note: "managed service provider"
    location: "Haaksbergen, NL"
    period: "Sep 2026 – Jan 2027"
    bullets:
      - "Automated standard IT changes end-to-end in production: self-service portal → Rewst RPA workflow → Autotask REST API, for ~200 client organisations."
      - "Sole owner of the Azure platform behind the company CRM: hosting, PostgreSQL, secrets management and the release pipeline."
  - role: "Systems Administrator"
    company: "Livio"
    note: "healthcare organisation"
    location: "Enschede, NL"
    period: "Apr 2025 – Aug 2026"
    bullets:
      - "Co-designed and ran the production Entra ID / hybrid identity platform: Conditional Access, RBAC, group design, Entra Connect sync and Group Policy."
      - "Operated within ISO 27001 / NEN 7510 for patient-related data: least privilege, access control, logging and audit."
certifications:
  - name: "Microsoft Certified: Azure Administrator Associate (AZ-104)"
    issuer: "Microsoft"
    status: earned
    date: "22 Oct 2026"
    expires: "23 Oct 2027"
    credential_id: "4C620F71E4B4DAAC"
    verify_url: "https://learn.microsoft.com/api/credentials/share/en-us/EmmanuelTekle/4C620F71E4B4DAAC"
    image: "/img/az-104-certificate.png"
    image_width: 1200   # replace with the value recorded in Task 2
    image_height: 814   # replace with the value recorded in Task 2
  - name: "HashiCorp Certified: Terraform Associate"
    issuer: "HashiCorp"
    status: planned
    date: "Exam planned Nov 2026"
  - name: "Certified Kubernetes Administrator (CKA)"
    issuer: "The Linux Foundation"
    status: planned
    date: "Exam planned Jan 2027"
education:
  degree: "Bachelor Cybersecurity & Cloud Engineering (HBO)"
  school: "Saxion University of Applied Sciences"
  location: "Enschede, NL"
  period: "Sep 2024 – Jul 2028 (expected)"
  detail: "Year 3 · Virtualisation (10), Public & Hybrid Cloud (9), Automated Infrastructures (9)"
beyond_work: "Outside work: competitive kickboxing (B-class, 9–1) and speedcubing (Dutch top 20, 2019)."
```

- [ ] **Step 2: Update `config/_default/hugo.toml`**

- `[params].description = "DevOps & Platform Engineer in the making. Azure-certified (AZ-104) Cloud & Cybersecurity student in Enschede, available Feb – Jul 2027."`
- Add top-level `disableKinds = ["taxonomy", "term"]`.
- Change `[markup.highlight].style` to `"github"` (light).
- Leave everything else.

- [ ] **Step 3: Verify Hugo loads the data without error**

Run: `hugo --minify --destination public --quiet && ls public/tags 2>&1 | head -1`
Expected: build OK; `ls: public/tags: No such file or directory`.

- [ ] **Step 4: Commit**

```bash
git add data/profile.yaml config/_default/hugo.toml
git commit -m "config: centralise profile facts in data/profile.yaml, disable taxonomies"
```

---

### Task 4: Stylesheet rewrite

**Files:**
- Rewrite: `assets/css/main.css`

**Interfaces:**
- Produces the class names every layout task uses. Lock them here:
  - layout: `.wrap` (max 760px), `.wrap-wide` (max 960px, homepage only)
  - nav: `.topnav`, `.nav-id`, `.nav-links`, `.nav-links a.active`, `.btn-cv`
  - buttons: `.btn`, `.btn-primary`, `.btn-secondary`
  - hero: `.hero`, `.badge`, `.hero h1`, `.lead`, `.hero-actions`, `.hero-links`
  - sections: `.section`, `.section-head` (h2 + optional right link `.section-link`)
  - stats: `.stats`, `.stat`, `.stat-value`, `.stat-label`
  - experience: `.timeline`, `.job`, `.job-head`, `.job-role`, `.job-org`, `.job-meta`, `.job ul`
  - projects: `.project-grid`, `.project-card`, `.card-thumb`, `.card-thumb img`, `.card-body`, `.card-title`, `.card-summary`, `.tags`, `.tag`, `.status` (+ `.status-live`, `.status-wip`, `.status-done`)
  - certs: `.certs`, `.cert`, `.cert-hero`, `.cert-image`, `.cert-name`, `.cert-meta`, `.cert-planned`
  - education: `.edu`, `.beyond`
  - lists: `.list`, `.list-item`, `.item-date`, `.item-title`, `.item-summary`
  - article: `.article`, `.article-title`, `.article-meta`, `.article-lede`, `.prose`, `.article-actions`, `.article-foot`
  - figures: `.figure`, `.figure img`, `.figure figcaption`, `.figure-dark` (dark padded panel for the two dark diagrams)
  - terminal: `.terminal`, `.terminal-bar`, `.terminal pre`, `.ok`
  - form: `.contact-form`, `.field-row`, `.field`, `.submit`
  - footer: `.sitefoot`, `.foot-links`

- [ ] **Step 1: Replace `assets/css/main.css`**

Write the stylesheet from scratch using the palette tokens on `:root` (`--bg`, `--text`, `--text-2`, `--border`, `--panel`, `--accent`, `--accent-hover`, `--sans`, `--mono`, `--radius: 12px`). Requirements the design pins:
- `body`: Inter, 16px, line-height 1.65, color `--text`, background `--bg`, no background-image.
- No `@keyframes`, no `text-shadow`, no gradients except none.
- `.badge`: inline-flex pill, `#eff6ff` background, `--accent` text, 8px green dot (`#16a34a`) before the text.
- `.hero h1`: `clamp(2rem, 6vw, 3.25rem)`, weight 800, letter-spacing -0.02em.
- `.btn-primary`: `--accent` background, white text; hover `--accent-hover`. `.btn-secondary`: 1px `--border`, `--text`.
- `.stats`: `grid-template-columns: repeat(3, 1fr)`; `.project-grid`: `repeat(2, 1fr)`; `.field-row`: `1fr 1fr`.
- `@media (max-width: 640px)`: all three of the above become `1fr`; `.wrap`/`.wrap-wide` padding 16px sides; `.topnav` wraps.
- `.card-thumb`: aspect-ratio 16/9, `--panel` background, overflow hidden; `img` object-fit cover.
- `.terminal`: background `#0f172a`, color `#e2e8f0`, radius, `pre` in `--mono` 0.85rem; `.ok` color `#4ade80`.
- `.figure-dark`: background `#0f172a`, padding 1rem, radius; image inside keeps aspect.
- `:focus-visible`: 2px `--accent` outline.
- `.prose` covers h2/h3, p, ul/ol, code (inline: `--panel` bg, 0.9em), pre (`.highlight` from Hugo: `--panel` bg, 1px border, overflow-x auto), blockquote, table, img (max-width 100%, radius).

- [ ] **Step 2: Verify the three responsive rules exist (Review Focus 1)**

Run: `grep -c "max-width: 640px" assets/css/main.css && grep -A12 "max-width: 640px" assets/css/main.css | grep -cE "\.stats|\.project-grid|\.field-row"`
Expected: first number ≥ 1, second number = 3.

- [ ] **Step 3: Verify no leftover dark-theme artefacts**

Run: `grep -nE "@keyframes|text-shadow|radial-gradient|linear-gradient|0b1015|45d68a" assets/css/main.css; echo "exit=$?"`
Expected: no lines, `exit=1`.

- [ ] **Step 4: Commit**

```bash
git add assets/css/main.css
git commit -m "style: light clean-corporate theme"
```

---

### Task 5: Base layout, head, nav, footer

**Files:**
- Modify: `layouts/_default/baseof.html`, `layouts/partials/head.html`, `layouts/partials/nav.html`, `layouts/partials/footer.html`

**Interfaces:**
- Consumes: CSS classes from Task 4; `site.Params` from Task 3.
- Produces: `baseof.html` with `{{ block "main" . }}` inside `<main class="wrap{{ if .IsHome }} wrap-wide{{ end }}">`.

- [ ] **Step 1: `head.html`**

- Title: home → `Emmanuel Tekle — DevOps & Platform Engineer`; other pages → `{{ .Title }} · Emmanuel Tekle`.
- `theme-color` `#ffffff`.
- Google Fonts link: only `Inter:wght@400;500;600;700;800` and `JetBrains+Mono:wght@400;500` with `display=swap`. Remove Space Grotesk.
- Favicon: same inline SVG technique, white rounded square `#ffffff` with a `#1d4ed8` circle, plus a 1px `#e2e8f0` stroke on the rect.
- Keep: description/og meta, canonical, both RSS `alternate` links, `rel="me"` links, CSS pipeline (minify + fingerprint + integrity), GoatCounter block unchanged.

- [ ] **Step 2: `nav.html`**

```html
<nav class="topnav">
  <a class="nav-id" href="{{ "/" | relURL }}">Emmanuel Tekle</a>
  <div class="nav-links">
    <a href="{{ "/#work" | relURL }}">Work</a>
    <a href="{{ "/projects/" | relURL }}"{{ if hasPrefix .RelPermalink "/projects" }} class="active"{{ end }}>Projects</a>
    <a href="{{ "/posts/" | relURL }}"{{ if hasPrefix .RelPermalink "/posts" }} class="active"{{ end }}>Writing</a>
    <a class="btn-cv" href="{{ site.Params.cv | relURL }}" target="_blank" rel="noopener noreferrer">CV ↓</a>
  </div>
</nav>
```

- [ ] **Step 3: `footer.html`**

`© {{ now.Year }} Emmanuel Tekle · {{ site.Params.location }}` left; right `.foot-links`: Email, GitHub, LinkedIn, CV, RSS (`/posts/index.xml`). External links get `target="_blank" rel="noopener noreferrer"`. Remove `.cursor` span.

- [ ] **Step 4: `baseof.html`**

Wrap: `<div class="page">` → nav partial → `<main class="wrap{{ if .IsHome }} wrap-wide{{ end }}">{{ block "main" . }}{{ end }}</main>` → footer partial. Nav and footer each sit in their own `.wrap-wide` container so they align with the widest content.

- [ ] **Step 5: Build and check**

Run: `hugo --minify --destination public --quiet && grep -c "Space+Grotesk" public/index.html; grep -o '<title>[^<]*' public/index.html`
Expected: `0` and `<title>Emmanuel Tekle — DevOps & Platform Engineer`.

- [ ] **Step 6: Commit**

```bash
git add layouts/_default/baseof.html layouts/partials/
git commit -m "layout: new head, nav with CV button, footer"
```

---

### Task 6: Homepage

**Files:**
- Rewrite: `layouts/index.html`
- Create: `layouts/partials/home/hero.html`, `stats.html`, `experience.html`, `projects.html`, `certifications.html`, `education.html`, `writing.html`, `contact.html`
- Create: `layouts/partials/project-card.html` (shared with Task 8 list page)
- Modify: `content/_index.md` (front matter only: keep title/description, add `aliases: ["/about/"]`, remove body text)
- Delete: `content/about.md`

**Interfaces:**
- Consumes: `site.Data.profile` (Task 3), CSS classes (Task 4), project front matter keys from Task 7: `summary`, `status` (`live`|`wip`|`done`), `tech` (list), `thumb` (image path or empty), `thumb_width`, `thumb_height`, `repo`, `weight`.
- Produces: `partials/project-card.html` taking a page `.` and rendering `.project-card` with thumb (image if `thumb` set, else an inline SVG placeholder panel: accent-coloured rounded square with a simple icon, builder's choice), title, summary, status pill, up to 4 tags.

- [ ] **Step 1: `layouts/index.html`**

```
{{ define "main" }}
{{ partial "home/hero.html" . }}
{{ partial "home/stats.html" . }}
{{ partial "home/experience.html" . }}
{{ partial "home/projects.html" . }}
{{ partial "home/certifications.html" . }}
{{ partial "home/education.html" . }}
{{ partial "home/writing.html" . }}
{{ partial "home/contact.html" . }}
{{ end }}
```

- [ ] **Step 2: Hero partial**

`.hero` with `.badge` = `profile.availability`, `<h1>` = `profile.headline`, `<p class="lead">` = `profile.lead`, `.hero-actions`: `<a class="btn btn-primary" href="{{ site.Params.cv | relURL }}" target="_blank" rel="noopener noreferrer">Download CV</a>` and `<a class="btn btn-secondary" href="#contact">Get in touch</a>`; `.hero-links`: GitHub, LinkedIn (external, new tab).

- [ ] **Step 3: Stats, experience, education partials**

- Stats: range `profile.stats` → `.stat` with `.stat-value` / `.stat-label`.
- Experience: `<section class="section" id="work">`, `.section-head` h2 "Experience"; range `profile.experience` → `.job`: `.job-head` (`.job-role`, `.job-org` = `company · note`), `.job-meta` = `location · period`, `<ul>` of bullets.
- Education: h2 "Education", `.edu` with degree, school, period, detail; then `<p class="beyond">` = `profile.beyond_work`.

- [ ] **Step 4: Projects partial**

h2 "Selected projects", `.section-link` → `/projects/` "All projects →". `{{ range first 4 (where site.RegularPages "Section" "projects").ByWeight }}{{ partial "project-card.html" . }}{{ end }}` inside `.project-grid`.

- [ ] **Step 5: Certifications partial (Review Focus 2 and 3)**

Range `profile.certifications`. For `status == "earned"`: `.cert.cert-hero` with `<img class="cert-image" src width height alt="{{ .name }} certificate" loading="lazy">` only `{{ with .image }}`, name, `.cert-meta` "Earned {{ .date }} · Expires {{ .expires }}", `{{ with .credential_id }}Credential ID {{ . }}{{ end }}`, `{{ with .verify_url }}<a href target="_blank" rel="noopener noreferrer">Verify on Microsoft Learn →</a>{{ end }}`. For `status == "planned"`: `.cert.cert-planned` with name and date only.

- [ ] **Step 6: Writing and contact partials**

- Writing: h2 "Latest writing", link "All posts →"; `.list` of `first 3` posts by date desc: `.item-date` (`02 Jan 2006`), `.item-title`.
- Contact: `<section class="section" id="contact">`, h2 "Get in touch", right side text "replies within 24h", then the existing form markup verbatim (same action, same fields, same hidden `_subject`), button class `btn btn-primary submit` with text "Send message". Below the form: "or email {{ site.Params.email }}" as a mailto link.

- [ ] **Step 7: Content changes**

`content/_index.md` front matter: title "Emmanuel Tekle", description = the params description, `aliases: ["/about/"]`; empty body. `git rm content/about.md`.

- [ ] **Step 8: Verify**

Run:
```bash
hugo --minify --destination public --quiet
grep -c 'id="work"' public/index.html            # expect 1
grep -c 'Available Feb – Jul 2027' public/index.html   # expect ≥1
grep -o 'Credential ID [A-Z0-9]*' public/index.html     # expect exactly one line: 4C620F71E4B4DAAC
grep -c 'Credential ID' public/index.html               # expect 1 (planned certs add none)
grep -c '<img[^>]*cert-image' public/index.html         # expect 1
grep -o 'href="https://[^"]*"[^>]*' public/index.html | grep -vc 'rel="noopener noreferrer"'   # expect 0
test -f public/about/index.html && grep -c 'http-equiv="refresh"' public/about/index.html   # expect 1
```

- [ ] **Step 9: Commit**

```bash
git add layouts/index.html layouts/partials/ content/_index.md content/about.md
git commit -m "home: hero, stats, experience, projects, certifications, education, writing, contact"
```

---

### Task 7: Project content (four pages) and single layout

**Files:**
- Create: `content/projects/ai-support-agent.md`, `content/projects/mini-payments-api.md`
- Rewrite: `content/projects/monitoring-homelab.md`, `content/projects/linux-security-hardening.md`, `content/projects/_index.md`
- Rewrite: `layouts/_default/single.html`
- Create: `layouts/shortcodes/figure.html`, `layouts/shortcodes/terminal.html`

**Interfaces:**
- Consumes: images from Task 2, classes from Task 4.
- Produces: front matter contract used by Task 6's card partial:
  `title, date, summary, status (live|wip|done), tech: [..], repo (optional URL), thumb (optional), thumb_width, thumb_height, weight, period (display string)`.
- Shortcodes: `{{< figure src="/img/..." alt="..." caption="..." width=1400 height=768 dark=true >}}` renders `.figure` (+`.figure-dark` when `dark`) with lazy img; `{{< terminal title="Security-audit.sh" >}}…{{< /terminal >}}` renders `.terminal` with `.terminal-bar` title and `<pre>` of the inner text, where lines starting with `✓ ` get `<span class="ok">`.

- [ ] **Step 1: `single.html`**

`.article`: h1 `.article-title`; `.article-meta`: `{{ with .Params.period }}` else date, `·` status pill (`.status.status-<status>` with text Live / In progress / Complete), `·` reading time for posts only; `.article-lede` = summary; `.article-actions`: `{{ with .Params.repo }}<a class="btn btn-secondary" target=_blank rel=noopener noreferrer>View on GitHub →</a>{{ end }}`; `.tags` from `tech` (projects) or `tags` (posts); `.prose` content; `.article-foot` back link ("← All projects" / "← All writing").

- [ ] **Step 2: Shortcodes** as specified in Interfaces. `figure.html` must emit `width`/`height` attributes and `loading="lazy"` (Review Focus 4).

- [ ] **Step 3: `ai-support-agent.md`**

Front matter: title "AI support agent in production", date 2026-10-01, period "Live since Oct 2026", status live, weight 10, summary "Solo-built agent that researches every new support ticket for ~50 client organisations and delivers a diagnosis note in 1–2 minutes.", tech `[Azure Container Apps, Service Bus, PostgreSQL, Key Vault, Bicep, Azure DevOps, Claude]`, no repo, no thumb.
Body, three h2 sections from the CV bullets, each 2–4 sentences, no extra facts:
- "What it does": idea to production in seven weeks; ~45 runs per workday; 200+ runs and zero data incidents in the first week; 17 read-only tools over Autotask, IT Glue and Datto RMM.
- "Platform as code": Container Apps, Service Bus queue + job, PostgreSQL, Key Vault via managed identities, ACR, Bicep, scale-to-zero; pipeline with unit tests, pip-audit, gitleaks, health-checked rollouts, PR build validation.
- "Security by design": one ticket per run, zero credentials inside the agent, secret fields filtered, prompt-injection attempts detected and refused. Closing line: a second agent for sales is in design, with an MCP server as the only write path and human approval before any send.
Optional inline SVG flow (ticket → queue → agent job → read-only tools → diagnosis note) inside a `.figure-dark`; skip if it would take more than 30 minutes.

- [ ] **Step 4: `mini-payments-api.md`**

Front matter: title "Mini Payments API", date 2026-10-24, period "Oct 2026 – present", status wip, weight 20, summary "Spring Boot payments service with PostgreSQL and Flyway, on its way to Kubernetes with a scanned CI/CD pipeline.", tech `[Java, Spring Boot, PostgreSQL, Flyway, Maven, Kubernetes]`, repo `https://github.com/E-mma9/mini-payments-api`.
Body: "What exists today" (accounts and transfers API, Flyway migration, unit test for transfer rules and an integration test for the transfer flow, Maven wrapper) and "Next" (Docker multi-stage build, Kubernetes manifests, GitHub Actions with Trivy, AKS via Terraform, Prometheus metrics). One sentence on why: preparation for platform work at a payments-grade standard.

- [ ] **Step 5: `monitoring-homelab.md`**

Front matter: title "Monitoring Homelab", date 2026-04-18, period "Feb – Apr 2026", status done, weight 30, summary "Production-style Prometheus, Grafana and Alertmanager stack on a 3-node Proxmox cluster, paging through PagerDuty.", tech `[Prometheus, Grafana, Alertmanager, blackbox_exporter, PagerDuty, Proxmox VE]`, repo `https://github.com/E-mma9/Monitoring-Homelab`, thumb `/img/projects/monitoring/pipeline.png` + its width/height.
Body sections: hero figure `pipeline.png` (dark); "What's running" (node_exporter on each host, Prometheus 15s scrape, Grafana dashboards, Alertmanager → PagerDuty, blackbox_exporter HTTP probes; everything except node_exporter in one LXC container); "Alert rules" table of the seven rules with threshold and `for` duration from the README; figure `prometheus-alert-rules.png`; "Dashboards" figure `grafana-cluster-overview.png`; "Paging" (PagerDuty text message, then phone call if not acknowledged) with figure `pagerduty-incident.png`; "The cluster underneath" (three nodes Dell OptiPlex / HP ProDesk, Proxmox VE 9 with HA, local storage only so failover copies the disk, ZFS pool on `pve` for backups, Tailscale, no ports exposed) with figure `proxmox-cluster.png` (dark); "What I learned" from README.

- [ ] **Step 6: `linux-security-hardening.md`**

Front matter: title "Linux Security Hardening", date 2026-04-20, period "Nov 2025 – Apr 2026", status done, weight 40, summary "Two Bash scripts that bring a fresh Ubuntu/Debian server to a sensible baseline and audit the result.", tech `[Bash, Ubuntu, SSH, UFW, auditd]`, repo `https://github.com/E-mma9/Linux-Security-Hardening`, no thumb.
Body: "What `harden-server.sh` does" (updates + unattended-upgrades; SSH: no root login, no password auth, port 2222; UFW default-deny with 2222/80/443; auditd enabled); "What `Security-audit.sh` reports" (SSH settings, UFW status, failed SSH logins from auth.log, pending updates); "Audit output" with a `{{< terminal title="sudo ./Security-audit.sh" >}}` block containing ~20 trimmed lines from the repo's `tests/output-example.txt` (SSH three lines, UFW status/default/rules for 2222/80/443, the "Audit Complete" line), with `✓ ` prefixes on the three SSH lines; "Why" (practice Linux admin and server security; scripts short enough to defend line by line); "What I'd do next" (Ansible once there is more than one server).

- [ ] **Step 7: `content/projects/_index.md`**

Title "Projects", description "Production work and homelab projects, with the code where it is public.", body one sentence, drop the Blowfish `cascade` block.

- [ ] **Step 8: Verify**

Run:
```bash
hugo --minify --destination public --quiet
ls public/projects/                                     # ai-support-agent mini-payments-api monitoring-homelab linux-security-hardening index.html index.xml
grep -c 'loading="lazy"' public/projects/monitoring-homelab/index.html    # expect 5
grep -o '<img[^>]*>' public/projects/monitoring-homelab/index.html | grep -vc 'width='   # expect 0
grep -c 'class="terminal' public/projects/linux-security-hardening/index.html   # expect ≥1
grep -c 'View on GitHub' public/projects/ai-support-agent/index.html             # expect 0
grep -c 'View on GitHub' public/projects/mini-payments-api/index.html            # expect 1
```

- [ ] **Step 9: Commit**

```bash
git add content/projects/ layouts/_default/single.html layouts/shortcodes/
git commit -m "projects: AI support agent, Mini Payments API, rewritten monitoring and hardening pages"
```

---

### Task 8: List pages (projects, writing)

**Files:**
- Rewrite: `layouts/_default/list.html`
- Modify: `content/posts/_index.md` (title "Writing", description "Notes from the homelab and from work.", drop `cascade`)

**Interfaces:**
- Consumes: `partial "project-card.html"` (Task 6).

- [ ] **Step 1: `list.html`**

h1 `.article-title` = `.Title`, `.article-lede` = `.Content`. If `.Section == "projects"`: `.project-grid` of all pages `.ByWeight` via the card partial. Else: `.list` of pages by date desc with `.item-date`, `.item-title`, `.item-summary`.

- [ ] **Step 2: Verify**

Run: `hugo --minify --destination public --quiet && grep -c 'project-card' public/projects/index.html && grep -c 'item-title' public/posts/index.html`
Expected: `4` and `3`.

- [ ] **Step 3: Commit**

```bash
git add layouts/_default/list.html content/posts/_index.md
git commit -m "lists: project grid and writing list in the new style"
```

---

### Task 9: Blog post factual corrections

**Files:**
- Modify: `content/posts/why-i-run-a-proxmox-cluster.md`, `content/posts/building-a-monitoring-stack-from-scratch.md`, `content/posts/hardening-ubuntu-with-bash.md`

**Interfaces:** none.

- [ ] **Step 1: `why-i-run-a-proxmox-cluster.md`**

Keep title, date, tags, tone. Rewrite "Hardware" to: three second-hand small-form-factor PCs (Dell OptiPlex, HP ProDesk), Intel i5; `pve` 16 GB RAM, 238 GB NVMe plus a 931 GB HDD as a ZFS pool for backups; `node2` and `node3` 8 GB RAM with 119 GB NVMe/SSD; Proxmox VE 9. Drop prices and power figures. "Why three": keep, replace the Pi-hole HA pair claim with "Proxmox HA restarts a failed service up to three times on the same node, then migrates it"; keep live migration and failure-mode points. Replace "Networks" with: one bridged LAN via `vmbr0`, no VLANs yet, Tailscale mesh for remote access, nothing exposed. Replace "Storage" with: local storage only; no Ceph because it would need an extra disk per node; HA failover copies the disk so it takes minutes, acceptable at home. Rewrite "What I'd do differently" to: add shared storage (an extra disk per node for Ceph, or NFS) so failover is seconds instead of minutes; segment the network next.

- [ ] **Step 2: `building-a-monitoring-stack-from-scratch.md`**

Change job name `nodes` → `proxmox-nodes` and targets to `192.168.1.249:9100`, `192.168.1.211:9100`, `192.168.1.74:9100` (from the README). Replace the probe targets with two generic local services (`http://192.168.1.211:3000` style; take real ones from the repo's `prometheus.yml` if present, else use the two from the README's screenshots). Replace "Three Proxmox nodes… One VM runs… Another runs…" with: node_exporter on each host; Prometheus, Alertmanager, Grafana and blackbox_exporter together in one LXC container. Add one paragraph listing the seven rules by name with their `for` durations. Keep the Alertmanager, test-alert and "tripped me up" sections (they do not contradict the repo), but change "SMS" wording to "text message, then a phone call if I don't acknowledge".

- [ ] **Step 3: `hardening-ubuntu-with-bash.md`**

Script names → `harden-server.sh`, `Security-audit.sh`. Remove the `fail2ban` bullet and the "Exits non-zero on drift" bullet. Replace the "Idempotency" section with "Keeping it simple": the script uses `sed -i 's/^#\?PermitRootLogin .*/PermitRootLogin no/'` style one-liners that match both the commented default and an existing value, and `ufw` skips rules that already exist, so re-running is safe; show the three real `sed` lines from the repo. Replace "The audit script" section's fictional `check()` function with the real approach: `grep -E '^(Port|PermitRootLogin|PasswordAuthentication)' /etc/ssh/sshd_config`, `ufw status verbose`, `grep "Failed password" /var/log/auth.log | tail -20`, `apt list --upgradable`; mention that a next step is turning it into `[OK]/[FAIL]` checks with an exit code. Keep "When this stops being the right tool" and "Repo".

- [ ] **Step 4: Verify**

Run: `bash scripts/verify-site.sh`
Expected: `OK` (the forbidden-string check now passes for the whole site; if it fails, the output names the file and string to fix).

- [ ] **Step 5: Commit**

```bash
git add content/posts/
git commit -m "posts: correct facts to match the Monitoring-Homelab and hardening repos"
```

---

### Task 10: Deploy build to repo root and clean stale output

**Files:**
- Delete (root, generated): `about/`, `css/`, `tags/`, `categories/`, `posts/`, `projects/`, `index.html`, `index.xml`, `sitemap.xml`
- Create (root, generated): fresh copies of everything in `public/`
- Modify: `scripts/verify-site.sh` (add a `--deploy` flag that performs the steps below)

**Interfaces:** none.

- [ ] **Step 1: Add `--deploy` to `scripts/verify-site.sh`**

After all checks pass, when `--deploy` is given: `rm -rf about css tags categories posts projects index.html index.xml sitemap.xml robots.txt`, then `cp -R public/. .` (this re-creates `index.html`, `posts/`, `projects/`, `css/`, `about/` alias, `sitemap.xml`, `robots.txt`, `index.xml`, `img/`, `Emmanuel_Tekle_CV.pdf`, `CNAME`). Never touch `content`, `layouts`, `assets`, `static`, `config`, `data`, `docs`, `scripts`, `.nojekyll`, `.gitignore`.

- [ ] **Step 2: Run it**

Run: `bash scripts/verify-site.sh --deploy && git status --short | head -40`
Expected: `OK`, then a status showing deletions under `tags/`, `categories/`, old `css/main.min.4505…css`, and new files under `img/`, `projects/ai-support-agent/`, `projects/mini-payments-api/`.

- [ ] **Step 3: Verify Review Focus 5**

Run:
```bash
ls css/            # exactly one main.min.*.css
ls tags categories 2>&1 | head -2   # No such file or directory
grep -c 'http-equiv="refresh"' about/index.html   # 1
test -f .nojekyll && cat CNAME     # emmanueltekle.nl
diff <(cd public && find . -type f | sort) <(find . -type f -not -path './.git/*' -not -path './public/*' -not -path './resources/*' -not -path './content/*' -not -path './layouts/*' -not -path './assets/*' -not -path './static/*' -not -path './config/*' -not -path './data/*' -not -path './docs/*' -not -path './scripts/*' -not -path './archetypes/*' -not -path './.vscode/*' -not -path './.superpowers/*' -not -name '.gitignore' -not -name '.nojekyll' -not -name 'go.mod' | sort)
```
Expected for the diff: no output (root generated files == `public/`).

- [ ] **Step 4: Serve locally and eyeball on desktop and phone width**

Run: `hugo server --minify --port 1313 --disableFastRender` (background), then open `http://localhost:1313/` in the browser at full width and at 375px (responsive mode). Check: no horizontal scroll, CV button opens the new PDF, certificate image shows without blue border, project images load, contact form fields stack on mobile, `/about/` redirects to `/`. Run Lighthouse (Chrome DevTools) on `/`: record the four scores in the PR description; all should be ≥ 95. Fix what is below and rerun.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "deploy: build clean-corporate site to repo root"
```

---

### Task 11: PR

- [ ] **Step 1: Push the branch and open a draft PR to `main`**

Run: `git push -u origin feature/portfolio-redesign` then open the PR (GitHub web or `gh` if installed). Title: "Portfolio redesign: clean corporate theme, CV and project updates". Body: three bullets (what changed, where facts come from, Lighthouse scores), link to the spec, and the attribution footer from the session.

- [ ] **Step 2: Report back** with the PR URL and the Lighthouse scores. Merging is Emmanuel's call.
