#!/usr/bin/env python3
"""Build docs/data/languages.json from datasets/ and language_families.json."""
import os, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS = os.path.join(ROOT, "datasets")
FAMILIES = os.path.join(ROOT, "docs", "data", "language_families.json")
OUT = os.path.join(ROOT, "docs", "data", "languages.json")

fam = json.load(open(FAMILIES))
fmap = {}
for k, v in fam.items():
    m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", k)
    if m:
        fmap[m.group(1).strip()] = v

out = []
for d in sorted(os.listdir(DATASETS)):
    p = os.path.join(DATASETS, d)
    if not os.path.isdir(p):
        continue
    files = os.listdir(p)
    readme = next((f for f in files if f.lower() == "readme.md"), None)
    datasets = sorted(f for f in files if f.lower().endswith(".md") and f.lower() != "readme.md")
    info = fmap.get(d, {})
    out.append({
        "name": d, "folder": d, "readme": readme,
        "count": len(datasets), "datasets": datasets,
        "family": info.get("family"), "subfamily": info.get("subfamily"),
    })

json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=2)
print(f"  wrote {len(out)} languages, {sum(x['count'] for x in out)} dataset files")
