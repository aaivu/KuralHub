#!/usr/bin/env bash
# Regenerate the self-contained website under docs/ from the repo's canonical
# sources (datasets/*.md, results/benchmark.json, docs/data/language_families.json).
# Run this whenever datasets/ or the benchmark results change.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "› Mirroring dataset markdown into docs/datasets/ ..."
rm -rf docs/datasets
rsync -a --include='*/' --include='*.md' --exclude='*' datasets/ docs/datasets/

echo "› Copying benchmark data ..."
cp results/benchmark.json docs/data/benchmark.json

echo "› Building static content, structured data + llms.txt (SEO/AEO) ..."
python3 scripts/build_site.py

echo "✓ docs/ is up to date ($(find docs/datasets -name '*.md' | wc -l | tr -d ' ') markdown files)."
