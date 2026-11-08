#!/usr/bin/env bash
# One command from a clean checkout: create a venv, install pinned
# ReportLab, and rewrite both copies of Emmanuel_Tekle_CV.pdf.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python generate_cv.py
