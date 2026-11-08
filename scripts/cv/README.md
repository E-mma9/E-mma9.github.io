# CV generator

`Emmanuel_Tekle_CV.pdf` (repo root and `static/`) is built by ReportLab from `content.yaml`. Lines that also appear on the site (role, certifications, client count, hobbies) use the site's wording. The rest of the CV is the October 2026 text.

From the repo root:

```bash
bash scripts/cv/generate.sh
```

That creates `scripts/cv/.venv` if needed, installs the pinned packages in `requirements.txt`, and writes the same bytes to:

- `static/Emmanuel_Tekle_CV.pdf` (what Hugo publishes)
- `Emmanuel_Tekle_CV.pdf` (the copy GitHub Pages serves from the repo root)

Running it again produces an identical file. `bash scripts/verify-site.sh --with-cv` regenerates the PDF and then runs the normal site build. Without `--with-cv`, the site build uses the PDF already committed under `static/`.
