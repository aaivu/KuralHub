#!/usr/bin/env python3
"""
Build the static, crawlable parts of the KuralHub site for SEO + AI/agent
discovery (GEO/AEO). Generates:

  - docs/data/languages.json            (language/dataset manifest)
  - static language tiles               -> injected into docs/datasets.html
  - Dataset ItemList JSON-LD            -> injected into docs/datasets.html
  - static "best model per language"    -> injected into docs/benchmark.html
  - docs/llms.txt, docs/llms-full.txt   (LLM/agent-facing summaries)

Everything is regenerated from the canonical sources (datasets/*.md,
results/benchmark.json, docs/data/language_families.json). Idempotent.
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS = os.path.join(ROOT, "datasets")
DOCS = os.path.join(ROOT, "docs")
FAMILIES = os.path.join(DOCS, "data", "language_families.json")
BENCH = os.path.join(ROOT, "results", "benchmark.json")
SITE = "https://aaivu.github.io/KuralHub"

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF←-⇿⌀-⏿️‍]"
)


def clean(s):
    s = EMOJI.sub("", s or "")
    s = re.sub(r"<[^>]+>", " ", s)            # strip html tags
    s = re.sub(r"[*_`#>|]", " ", s)            # strip md markup
    s = re.sub(r"\s+", " ", s).strip(" -:\t")
    return s.strip()


def field(text, label):
    m = re.search(rf"{label}\s*[:：]\**\s*(.+)", text, re.IGNORECASE)
    return clean(m.group(1)) if m else ""


def pretty_name(fname, text):
    h1 = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if h1:
        name = clean(h1.group(1))
        name = re.split(r"\s+-\s+", name)[0].strip()
        if name:
            return name
    return os.path.splitext(fname)[0].replace("_", " ")


# ---------------------------------------------------------------- load data
fam_raw = json.load(open(FAMILIES))
fmap = {}
for k, v in fam_raw.items():
    m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", k)
    if m:
        fmap[m.group(1).strip()] = v

languages = []
all_datasets = []
for d in sorted(os.listdir(DATASETS)):
    p = os.path.join(DATASETS, d)
    if not os.path.isdir(p):
        continue
    files = os.listdir(p)
    readme = next((f for f in files if f.lower() == "readme.md"), None)
    ds_files = sorted(f for f in files if f.lower().endswith(".md") and f.lower() != "readme.md")
    info = fmap.get(d, {})
    entry = {
        "name": d, "folder": d, "readme": readme,
        "count": len(ds_files), "datasets": ds_files,
        "family": info.get("family"), "subfamily": info.get("subfamily"),
    }
    languages.append(entry)
    for f in ds_files:
        text = open(os.path.join(p, f), encoding="utf-8", errors="ignore").read()
        all_datasets.append({
            "lang": d, "file": f,
            "name": pretty_name(f, text),
            "emotions": field(text, "Emotion Categories"),
            "license": field(text, "License"),
            "access": field(text, "Access"),
            "family": info.get("family"),
        })

json.dump(languages, open(os.path.join(DOCS, "data", "languages.json"), "w"),
          ensure_ascii=False, indent=2)

bench = json.load(open(BENCH))
n_models = sorted({b["model"] for L in bench.values() for ds in L.values() for b in ds})
n_runs = sum(len(ds) for L in bench.values() for ds in L.values())

# best model per language (by test accuracy across its datasets)
best_per_lang = []
for lang, dss in bench.items():
    best = None
    for ds, rows in dss.items():
        for r in rows:
            if best is None or r["test_accuracy"] > best["test_accuracy"]:
                best = {**r, "dataset": ds}
    if best:
        m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", lang)
        best_per_lang.append({
            "language": m.group(1).strip() if m else lang,
            "code": m.group(2) if m else "",
            "dataset": best["dataset"], "model": best["model"],
            "test": best["test_accuracy"],
        })
best_per_lang.sort(key=lambda x: x["language"])


# ---------------------------------------------------------------- injectors
def inject(path, start, end, payload):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    s2 = pat.sub(start + "\n" + payload + "\n" + end, s, count=1)
    if s2 == s and start not in s:
        raise SystemExit(f"marker {start} not found in {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s2)


def esc(s):
    return html.escape(s or "", quote=True)


# static language tiles
tiles = []
for L in languages:
    fam = f'<div class="fam">{esc((L["family"] or "").upper())}</div>' if L["family"] else ""
    tiles.append(
        f'<button class="lang-tile" data-folder="{esc(L["folder"])}">'
        f'<div class="name">{esc(L["name"])}</div>'
        f'<div class="meta">{L["count"]} dataset{"" if L["count"]==1 else "s"}</div>'
        f'{fam}</button>'
    )
inject(os.path.join(DOCS, "datasets.html"), "<!-- LANGS:START -->", "<!-- LANGS:END -->",
       "".join(tiles))

# Dataset ItemList JSON-LD
items = []
for i, ds in enumerate(all_datasets, 1):
    desc = f'{ds["name"]} — a {ds["lang"]} speech emotion recognition (SER) dataset cataloged in KuralHub.'
    extra = []
    if ds["emotions"]:
        extra.append("Emotions: " + ds["emotions"] + ".")
    if ds["access"]:
        extra.append("Access: " + ds["access"] + ".")
    if extra:
        desc += " " + " ".join(extra)
    node = {
        "@type": "Dataset",
        "name": ds["name"],
        "description": desc[:340],
        "inLanguage": ds["lang"],
        "keywords": [f"{ds['lang']} speech emotion recognition", "SER dataset",
                     "emotion dataset", "speech dataset"],
        "isAccessibleForFree": True,
        "url": f"{SITE}/datasets.html",
        "isPartOf": {"@type": "WebSite", "name": "KuralHub", "url": f"{SITE}/"},
    }
    if ds["license"] and ds["license"].lower() not in ("not specified", "-", "not available"):
        node["license"] = ds["license"]
    items.append({"@type": "ListItem", "position": i, "item": node})

itemlist = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Speech Emotion Recognition datasets cataloged by KuralHub",
    "numberOfItems": len(items),
    "itemListElement": items,
}
inject(os.path.join(DOCS, "datasets.html"),
       "<!-- JSONLD:DATASETS:START -->", "<!-- JSONLD:DATASETS:END -->",
       '<script type="application/ld+json">\n'
       + json.dumps(itemlist, ensure_ascii=False, indent=1) + "\n</script>")

# benchmark static summary
rows = "".join(
    f'<tr><td>{esc(b["language"])} <span style="color:var(--faint)">{esc(b["code"])}</span></td>'
    f'<td class="model">{esc(b["model"])}</td>'
    f'<td>{esc(b["dataset"])}</td>'
    f'<td><span class="acc good">{b["test"]*100:.1f}%</span></td></tr>'
    for b in best_per_lang
)
summary = (
    '<h2 style="font-size:1.3rem; margin-bottom:6px;">Best model per language</h2>'
    f'<p style="color:var(--muted); margin-bottom:18px;">Across {len(best_per_lang)} benchmarked languages, '
    f'{len(n_models)} pretrained speech models and {n_runs} fine-tuning runs — the highest test accuracy reached for each language.</p>'
    '<div class="table-scroll"><table class="bench"><thead><tr>'
    '<th>Language</th><th>Top model</th><th>Dataset</th><th>Best test accuracy</th>'
    f'</tr></thead><tbody>{rows}</tbody></table></div>'
)
inject(os.path.join(DOCS, "benchmark.html"),
       "<!-- BENCHSUMMARY:START -->", "<!-- BENCHSUMMARY:END -->", summary)


# ---------------------------------------------------------------- llms.txt
def md_list_langs():
    out = []
    for L in languages:
        fam = f' ({L["family"]})' if L["family"] else ""
        out.append(f'- {L["name"]}{fam} — {L["count"]} dataset(s)')
    return "\n".join(out)


llms = f"""# KuralHub

> KuralHub is a comprehensive survey and benchmark of Speech Emotion Recognition (SER) datasets across the world's languages. It catalogs 90+ SER datasets spanning 70+ languages and benchmarks {len(n_models)} pretrained speech models (HuBERT, wav2vec 2.0, WavLM, Whisper) on 29 languages across {n_runs} fine-tuning experiments. Maintained by the aaivu lab, University of Moratuwa, Sri Lanka. To appear at Interspeech 2026.

KuralHub helps researchers and practitioners (1) find speech emotion / emotion-speech datasets for a given language, and (2) see which speech model performs best per language.

## Key facts
- Languages surveyed: 70+
- Datasets cataloged: 90+
- Languages benchmarked: 29
- Speech models benchmarked: {len(n_models)} ({", ".join(n_models)})
- Fine-tuning experiments: {n_runs}
- Protocol: each pretrained speech encoder is fine-tuned per language (monolingual) with a classification head on a frozen backbone; validation and test accuracy reported.

## Pages
- [Home / overview]({SITE}/): project summary, methodology, key findings, team, citation.
- [Benchmark]({SITE}/benchmark.html): validation/test accuracy for every model on every benchmarked dataset; best model per language.
- [Datasets catalog]({SITE}/datasets.html): all 70+ languages with dataset metadata and access links.

## Machine-readable data
- Benchmark results (JSON): {SITE}/data/benchmark.json
- Language manifest (JSON): {SITE}/data/languages.json
- Language families (JSON): {SITE}/data/language_families.json

## Citation
Thavarasa, L., Thevakumar, J., Sivatheepan, T., Thayasivam, U. "KuralHub: A Comprehensive Review of Speech Emotion Recognition Datasets." To appear, Interspeech 2026.

## Repository
{SITE.replace("aaivu.github.io/KuralHub", "github.com/aaivu/KuralHub")}
"""

best_lines = "\n".join(
    f'- {b["language"]}: best model {b["model"]} on {b["dataset"]} — {b["test"]*100:.1f}% test accuracy'
    for b in best_per_lang
)
llms_full = llms + f"""
## All languages and dataset counts
{md_list_langs()}

## Best model per benchmarked language
{best_lines}
"""

open(os.path.join(DOCS, "llms.txt"), "w", encoding="utf-8").write(llms)
open(os.path.join(DOCS, "llms-full.txt"), "w", encoding="utf-8").write(llms_full)

print(f"✓ {len(languages)} languages, {len(all_datasets)} datasets, "
      f"{len(best_per_lang)} benchmarked, {n_runs} runs")
print("✓ injected static tiles + Dataset JSON-LD + benchmark summary")
print("✓ wrote llms.txt + llms-full.txt")
