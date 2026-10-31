#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf docs/datasets
rsync -a --include='*/' --include='*.md' --exclude='*' datasets/ docs/datasets/
python3 scripts/build_site.py
