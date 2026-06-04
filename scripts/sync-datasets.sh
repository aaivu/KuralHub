#!/usr/bin/env bash
# Regenerate the self-contained website data under docs/ from the repo's
# canonical sources (datasets/, results/benchmark.json, language_families).
# Run this whenever datasets/ or the benchmark results change.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "› Mirroring dataset markdown into docs/datasets/ ..."
rm -rf docs/datasets
rsync -a --include='*/' --include='*.md' --exclude='*' datasets/ docs/datasets/

echo "› Rebuilding docs/data/languages.json ..."
python3 scripts/build_languages_manifest.py

echo "› Copying benchmark + family data ..."
cp results/benchmark.json docs/data/benchmark.json

echo "✓ docs/ is up to date ($(find docs/datasets -name '*.md' | wc -l | tr -d ' ') markdown files)."
