#!/usr/bin/env python3
import csv
import html
import io
import json
import os
import re
import statistics as st
from collections import OrderedDict, defaultdict
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS = os.path.join(ROOT, "datasets")
LOGS = os.path.join(ROOT, "results", "train_val_test_logs")
DOCS = os.path.join(ROOT, "docs")
SITE = "https://aaivu.github.io/KuralHub"
REPO = "https://github.com/aaivu/KuralHub"
DOI = "10.21437/Interspeech.2026-3502"
DOI_URL = "https://doi.org/" + DOI
PDF_URL = (
    "https://www.isca-archive.org/interspeech_2026/"
    "thavarasa26_interspeech.pdf"
)
TITLE = (
    "KuralHub: Exposing Typological Capability Frontiers in "
    "Multilingual Speech Emotion Recognition"
)
CITATION = (
    "Thavarasa, L., Thevakumar, J., Sivatheepan, T., Thayasivam, U. (2026) "
    f"{TITLE}. Proc. Interspeech 2026, 4673-4678, doi: {DOI}"
)

# Families follow the labels in Figure 2 of the paper.
FAMILY = {
    "Afrikaans": ("Indo-European", "Germanic"),
    "Amharic": ("Afro-Asiatic", "Semitic"),
    "Arabic": ("Afro-Asiatic", "Semitic"),
    "Assamese": ("Indo-European", "Indo-Aryan"),
    "Azerbaijani": ("Turkic", "Oghuz"),
    "Bambara": ("Niger-Congo", "Mande"),
    "Bengali": ("Indo-European", "Indo-Aryan"),
    "Bhojpuri": ("Indo-European", "Indo-Aryan"),
    "Burmese": ("Sino-Tibetan", "Lolo-Burmese"),
    "Cebuano": ("Austronesian", "Philippine"),
    "Chinese": ("Sino-Tibetan", "Sinitic"),
    "Czech": ("Indo-European", "Slavic"),
    "Dutch": ("Indo-European", "Germanic"),
    "English": ("Indo-European", "Germanic"),
    "Filipino": ("Austronesian", "Philippine"),
    "French": ("Indo-European", "Romance"),
    "Fulflude": ("Niger-Congo", "Atlantic"),
    "German": ("Indo-European", "Germanic"),
    "Greek": ("Indo-European", "Hellenic"),
    "Gujarati": ("Indo-European", "Indo-Aryan"),
    "Hausa": ("Afro-Asiatic", "Chadic"),
    "Hindi": ("Indo-European", "Indo-Aryan"),
    "Hungarian": ("Uralic", "Ugric"),
    "Igbo": ("Niger-Congo", "Volta-Niger"),
    "Indonesian": ("Austronesian", "Malayic"),
    "Italian": ("Indo-European", "Romance"),
    "Japanese": ("Japonic", ""),
    "Javanese": ("Austronesian", "Malayo-Polynesian"),
    "Kannada": ("Dravidian", "South Dravidian"),
    "Kazakh": ("Turkic", "Kipchak"),
    "Khmer": ("Austroasiatic", "Khmeric"),
    "Korean": ("Koreanic", ""),
    "Kurdish": ("Indo-European", "Iranian"),
    "Magahi": ("Indo-European", "Indo-Aryan"),
    "Maithili": ("Indo-European", "Indo-Aryan"),
    "Malay": ("Austronesian", "Malayic"),
    "Malayalam": ("Dravidian", "South Dravidian"),
    "Nepali": ("Indo-European", "Indo-Aryan"),
    "Nigerian Pidgin": ("English-based creole", ""),
    "Northern Pashto": ("Indo-European", "Iranian"),
    "Northern Uzbek": ("Turkic", "Karluk"),
    "Odia": ("Indo-European", "Indo-Aryan"),
    "Persian": ("Indo-European", "Iranian"),
    "Polish": ("Indo-European", "Slavic"),
    "Portuguese": ("Indo-European", "Romance"),
    "Punjabi": ("Indo-European", "Indo-Aryan"),
    "Quechua": ("Quechuan", ""),
    "Romanian": ("Indo-European", "Romance"),
    "Russian": ("Indo-European", "Slavic"),
    "Saraiki": ("Indo-European", "Indo-Aryan"),
    "Sindhi": ("Indo-European", "Indo-Aryan"),
    "Sinhala": ("Indo-European", "Indo-Aryan"),
    "Somali": ("Afro-Asiatic", "Cushitic"),
    "Sotho": ("Niger-Congo", "Bantu"),
    "Spanish": ("Indo-European", "Romance"),
    "Sunda": ("Austronesian", "Malayo-Polynesian"),
    "Swahili": ("Niger-Congo", "Bantu"),
    "Swedish": ("Indo-European", "Germanic"),
    "Tagalog": ("Austronesian", "Philippine"),
    "Tamil": ("Dravidian", "South Dravidian"),
    "Telugu": ("Dravidian", "South-Central Dravidian"),
    "Thai": ("Kra-Dai", "Tai"),
    "Tswana": ("Niger-Congo", "Bantu"),
    "Turkish": ("Turkic", "Oghuz"),
    "Ukrainian": ("Indo-European", "Slavic"),
    "Urdu": ("Indo-European", "Indo-Aryan"),
    "Vietnamese": ("Austroasiatic", "Vietic"),
    "Xhosa": ("Niger-Congo", "Bantu"),
    "Yoruba": ("Niger-Congo", "Volta-Niger"),
    "Zulu": ("Niger-Congo", "Bantu"),
}
DISPLAY = {"Fulflude": "Fulfulde", "Sunda": "Sundanese"}

# (checkpoint, family, Hugging Face id, approx. params in millions, Fig. 3)
MODELS = [
    ("hubert-base-ls960", "HuBERT", "facebook/hubert-base-ls960", 95),
    ("hubert-large-ls960-ft", "HuBERT", "facebook/hubert-large-ls960-ft", 316),
    ("wav2vec2-base", "wav2vec 2.0", "facebook/wav2vec2-base", 95),
    ("wav2vec2-large-960h", "wav2vec 2.0", "facebook/wav2vec2-large-960h", 317),
    ("wav2vec2-large-lv60", "wav2vec 2.0", "facebook/wav2vec2-large-lv60", 317),
    ("wav2vec2-xls-r-300m", "wav2vec 2.0", "facebook/wav2vec2-xls-r-300m", 300),
    ("wav2vec2-xls-r-1b", "wav2vec 2.0", "facebook/wav2vec2-xls-r-1b", 1000),
    ("wavlm-base-plus", "WavLM", "microsoft/wavlm-base-plus", 95),
    ("wavlm-large", "WavLM", "microsoft/wavlm-large", 316),
    ("whisper-small", "Whisper", "openai/whisper-small", 244),
    ("whisper-large", "Whisper", "openai/whisper-large", 1550),
]  # fmt: skip
MODEL_ORDER = [m[0] for m in MODELS]
MODEL_FAMILY = {m[0]: m[1] for m in MODELS}

CODE_TO_FOLDER = {
    "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "bn": "Bengali",
    "de": "German", "el": "Greek", "en": "English", "es": "Spanish",
    "fa": "Persian", "fr": "French", "hi": "Hindi", "hu": "Hungarian",
    "id": "Indonesian", "it": "Italian", "ja": "Japanese", "kk": "Kazakh",
    "kn": "Kannada", "ko": "Korean", "or": "Odia", "pl": "Polish",
    "pt": "Portuguese", "qu": "Quechua", "ru": "Russian", "sw": "Swahili",
    "ta": "Tamil", "te": "Telugu", "tr": "Turkish", "ur": "Urdu",
    "zh": "Chinese",
}  # fmt: skip

# Run ID dataset name -> catalog file it was drawn from.
RUN_DATASET_FILE = {
    "AfrikaansEmotionalSpeechCorpus": "AfrikaansSE.md", "ASED": "ASED.md",
    "ANAD": "ANAD.md", "BANSpEmo": "BANSpEmo.md", "SUBESCO": "SUBESCO.md",
    "EmoDB": "EmoDB.md", "AESDD": "AESDD.md", "IESC": "IESC.md",
    "RAVDESS": "RAVDESS.md", "MESD": "MESD.md", "SHEMO": "ShEMO.md",
    "CaFE": "CaFE.md", "Hindi-Dataset": "VishalB.md",
    "HungarianEmotionalSpeechCorpus": "HESD.md",
    "IndoWaveSentiment": "IndoWaveSentiment.md", "EMOVO": "EMOVO.md",
    "Emozionalmente": "Emozionalmente.md", "JVNV": "JVNV.md",
    "KazakhEmotionalTTS": "KazEmoTTS.md",
    "Kannada-Dataset": "Agrawal_et_al_2022.md", "KESDy18": "KESDy18.md",
    "SITB-OSED": "SITB-OSED.md", "nEMO": "nEMO.md", "emoUERJ": "emoUERJ.md",
    "Quechua-Collao-Corpus": "Quechua-Collao.md", "RESD": "RESD.md",
    "Swahili-Dataset": "Kenyan_Swahili.md", "EmoTa": "EmoTa.md",
    "Telugu-Dataset": "Sowmith_et_al_2024.md", "TurEV-DB": "TurEV-DB.md",
    "Urdu-Dataset": "URDU-Dataset.md", "UrduSER": "UrduSER.md",
    "ESD": "ESD.md",
}  # fmt: skip

EMOTIONS = ["ANGER", "FEAR", "HAPPINESS", "NEUTRAL", "SADNESS"]
EMOJI = re.compile(
    "[\U0001f000-\U0001faff\U00002600-\U000027bf\U0001f1e6-\U0001f1ff"
    "←-⇿⌀-⏿️‍]"
)
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]*)\)")
EMPTY = {
    "", "-", "—", "...", "tbd", "n/a", "na", "none", "not specified",
    "not available", "unknown",
}  # fmt: skip
BOILERPLATE_NOTE = "fill the request process if the dataset is restricted"
BEST_TAG = '<span class="tag best">best</span>'
AUTHOR_URL = "https://luxshan2000.github.io/"
ISSUE_DATASET = f"{REPO}/issues/new?template=add-dataset.yml"
ISSUE_MODEL = f"{REPO}/issues/new?template=add-model.yml"
THEME_SCRIPT = (
    "<script>try{var t=localStorage.getItem('kh-theme');"
    "if(t)document.documentElement.setAttribute('data-theme',t)}"
    "catch(e){}</script>"
)
STAR_BUTTON = (
    f'<a class="star-btn" href="{REPO}" '
    'aria-label="Star KuralHub on GitHub" title="Star KuralHub on GitHub">'
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5'
    '-4.8-4.6 6.6-.9z"/></svg>'
    "<span>Star</span></a>"
)
THEME_BUTTON = (
    '<button class="theme-toggle" type="button" hidden '
    'aria-label="Switch theme">'
    '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>'
    "</svg>"
    '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" aria-hidden="true">'
    '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4'
    'M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'
    "</svg></button>"
)


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_]+", "-", s).strip("-")


def display(folder):
    return DISPLAY.get(folder, folder)


def lang_slug(folder):
    return slug(display(folder))


def clean(s):
    s = EMOJI.sub("", s or "")
    s = MD_LINK.sub(r"\1", s)
    s = re.sub(r"</?br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("**", "").replace("`", "").replace("_", " ")
    return re.sub(r"\s+", " ", s).strip(" :|")


def is_empty(s):
    t = clean(s).lower().strip(" .")
    return t in EMPTY or (t.startswith("[") and t.endswith("]"))


def safe_url(u):
    return u if re.match(r"^(https?://|mailto:)", u or "") else None


def links(raw):
    return [
        (clean(text) or url, url)
        for text, url in MD_LINK.findall(raw or "")
        if safe_url(url)
    ]


def first_url(pairs):
    return pairs[0][1] if pairs else None


def resolve_href(href, folder, prefix):
    if re.match(r"^(https?://|mailto:|#)", href):
        return href
    if re.match(r"^[a-z]+:", href, re.I):
        return "#"
    href = href[2:] if href.startswith("./") else href
    if href.lower() == "readme.md":
        return f"{prefix}languages/{lang_slug(folder)}.html"
    if href.endswith(".md") and "/" not in href:
        return "#" + slug(os.path.splitext(href)[0])
    target = os.path.normpath(os.path.join("datasets", folder, href))
    return f"{REPO}/blob/main/{quote(target)}"


def emph(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", s)


def md_inline(s, folder="", prefix=""):
    s = re.sub(r"</?br\s*/?>", " ", EMOJI.sub("", s or ""), flags=re.I)
    out, last = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)|`([^`]+)`", s):
        out.append(emph(esc(s[last : m.start()])))
        if m.group(3):
            out.append(f"<code>{esc(m.group(3))}</code>")
        else:
            href = resolve_href(m.group(2), folder, prefix)
            out.append(f'<a href="{esc(href)}">{emph(esc(m.group(1)))}</a>')
        last = m.end()
    out.append(emph(esc(s[last:])))
    return re.sub(r"\s+", " ", "".join(out)).strip()


def md_block(text, folder="", prefix=""):
    blocks, para, items = [], [], []

    def inline(s):
        return md_inline(s, folder, prefix)

    def flush():
        if para:
            blocks.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()
        if items:
            blocks.append(
                "<ul>"
                + "".join(f"<li>{inline(i)}</li>" for i in items)
                + "</ul>"
            )
            items.clear()

    for line in text.splitlines():
        t = line.strip()
        m = re.match(r"^([-*+]|\d+\.)\s+(.*)", t)
        if not t:
            flush()
        elif m:
            if para:
                flush()
            items.append(m.group(2))
        elif t.startswith("#"):
            flush()
            blocks.append(f"<h4>{inline(t.lstrip('# '))}</h4>")
        elif t.startswith(">"):
            flush()
            blocks.append(f'<p class="muted">{inline(t.lstrip("> "))}</p>')
        else:
            if items:
                flush()
            para.append(t)
    flush()
    return "\n".join(blocks)


def field(text, label):
    # Labels may carry an emoji inside the bold, e.g. "**🔤 ISO Code:**".
    m = re.search(
        r"\*\*[^*\w]*" + label + r"\s*:?\s*\*\*\s*:?(.*)", text, re.I
    )
    return m.group(1).strip() if m else ""


def section(text, heading):
    m = re.search(
        r"^##[^\n]*" + heading + r"[^\n]*\n(.*?)(?=^---|^## |\Z)",
        text,
        re.M | re.S | re.I,
    )
    return m.group(1).strip() if m else ""


def value(text, label):
    raw = field(text, label)
    return "" if is_empty(raw) else clean(raw)


def number(s):
    m = re.search(r"\d[\d,]*", s or "")
    return m.group(0).replace(",", "") if m else ""


def fmt(x, nd=2):
    return "" if x is None else f"{x:.{nd}f}"


def pct(x):
    return "" if x is None else f"{x * 100:.1f}"


def jsonld(obj):
    text = json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{text}</script>'


def inject(path, name, payload):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    with open(path, encoding="utf-8") as f:
        s = f.read()
    if start not in s or end not in s:
        raise SystemExit(f"marker {name} not found in {path}")
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    s = pat.sub(lambda _: f"{start}\n{payload}\n{end}", s, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def write_json(name, obj, indent=2):
    text = json.dumps(obj, ensure_ascii=False, indent=indent)
    write(os.path.join(DOCS, "data", name), text + "\n")


def access_kind(s):
    t = clean(s).lower()
    if any(w in t for w in ("open", "free", "public")):
        return "Open"
    if any(w in t for w in ("request", "restricted", "agreement")):
        return "On request"
    if any(w in t for w in ("paid", "commercial", "purchase", "ldc")):
        return "Paid"
    return clean(s) or "Unknown"


def parse_table(md):
    rows = []
    for line in md.splitlines():
        t = line.strip()
        if not t.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in t.strip("|").split("|")]
        if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            rows.append(cells)
    return rows


def parse_language(folder):
    path = os.path.join(DATASETS, folder)
    readme = next(f for f in os.listdir(path) if f.lower() == "readme.md")
    text = open(os.path.join(path, readme), encoding="utf-8").read()
    meta = {}
    rows = parse_table(section(text, "Available Datasets"))
    if rows:
        head = [clean(c).lower() for c in rows[0]]
        col = {
            k: next((i for i, h in enumerate(head) if k in h), None)
            for k in ("speaker", "sample")
        }
        for r in rows[1:]:
            found = MD_LINK.findall(r[0])
            if found:
                meta[found[0][1].lstrip("./")] = {
                    k: clean(r[i]) if i is not None and i < len(r) else ""
                    for k, i in col.items()
                }
    files = sorted(
        f
        for f in os.listdir(path)
        if f.lower().endswith(".md") and f.lower() != "readme.md"
    )
    datasets, seen = [], set()
    for f in files:
        d = parse_dataset(folder, f, meta.get(f, {}))
        while d["anchor"] in seen:
            d["anchor"] += "-2"
        seen.add(d["anchor"])
        datasets.append(d)
    fam, branch = FAMILY[folder]
    countries = value(text, "Major Spoken Countries") or value(
        text, "Major Spoken Regions"
    )
    return {
        "folder": folder,
        "name": display(folder),
        "slug": lang_slug(folder),
        "family": fam,
        "branch": branch,
        "iso": value(text, "ISO Code"),
        "countries": countries,
        "readme": readme,
        "datasets": datasets,
    }


def parse_dataset(folder, fname, table_meta):
    text = open(os.path.join(DATASETS, folder, fname), encoding="utf-8").read()
    stem = os.path.splitext(fname)[0]
    h1 = re.search(r"^#\s+(.+)$", text, re.M)
    short = re.split(r"\s+-\s+", clean(h1.group(1)) if h1 else stem)[0]
    short = short.strip() or stem
    full = value(text, "Dataset Name")
    access_md = section(text, "Access")
    cites = re.findall(r"```[a-z]*\n(.*?)```", section(text, "Citation"), re.S)
    note = re.search(r"Note:\**\s*(.*)", access_md)
    note = clean(note.group(1)) if note else ""
    contact = field(access_md, "Contact")
    if not contact:
        m = re.search(r"Contact:\s*(.*)", access_md)
        contact = m.group(1) if m else ""
    lic_raw = field(text, "License")
    meta = {k: v for k, v in table_meta.items() if not is_empty(v)}
    return {
        "file": fname,
        "anchor": slug(stem),
        "name": short,
        "full_name": full if full.lower() != short.lower() else "",
        "type": value(text, "Dataset Type"),
        "emotions": value(text, "Emotion Categories"),
        "size": value(text, "Size"),
        "speakers": meta.get("speaker", ""),
        "samples": meta.get("sample", ""),
        "recording": value(text, "Recording Environment"),
        "license": "" if is_empty(lic_raw) else clean(lic_raw),
        "license_url": first_url(links(lic_raw)) or "",
        "access": access_kind(field(text, "Access")),
        "overview_md": section(text, "Overview"),
        "website": links(field(access_md, "Official Website")),
        "paper": links(field(access_md, "Papers?")),
        "download": links(field(access_md, "Download Links?")),
        "file_format": value(access_md, "File ?Format"),
        "contact": links(contact),
        "note": "" if BOILERPLATE_NOTE in note.lower() else note,
        "citations": [
            c.strip()
            for c in cites
            if c.strip()
            and "thavarasa26_interspeech" not in c
            and c.strip().upper() != "TBD"
        ],
    }


languages = [
    parse_language(d)
    for d in sorted(os.listdir(DATASETS))
    if os.path.isdir(os.path.join(DATASETS, d))
]
missing = [L["folder"] for L in languages if L["folder"] not in FAMILY]
if missing:
    raise SystemExit(f"add these languages to FAMILY: {missing}")
by_name = sorted(languages, key=lambda L: L["name"])
all_datasets = [(L, d) for L in languages for d in L["datasets"]]
catalog_name = {(L["folder"], d["file"]): d["name"] for L, d in all_datasets}


def read_report(path):
    if not os.path.exists(path):
        return None
    out = {"per_emotion": {}}
    for line in open(path, encoding="utf-8"):
        s = line.split()
        if s and s[0] in EMOTIONS and len(s) >= 5:
            out["per_emotion"][s[0]] = float(s[3])
        elif s and s[0] == "accuracy":
            out["accuracy"] = float(s[1])
        elif s and s[0] in ("macro", "weighted"):
            out[s[0]] = [float(x) for x in s[2:5]]
    return out


runs = []
model_re = "|".join(re.escape(m) for m in MODEL_ORDER)
for run_id in sorted(os.listdir(LOGS)):
    m = re.match(rf"^([a-z]{{2}})_(.+)_({model_re})$", run_id)
    if not m:
        continue
    code, ds, model = m.groups()
    base = os.path.join(LOGS, run_id, run_id)
    test = read_report(f"{base}_test_classification_report.txt")
    val = read_report(f"{base}_val_classification_report.txt")
    if not test:
        continue
    folder = CODE_TO_FOLDER[code]
    entry = RUN_DATASET_FILE.get(ds, "")
    runs.append(
        {
            "run_id": run_id,
            "language": display(folder),
            "language_folder": folder,
            "iso": code,
            "family": FAMILY[folder][0],
            "dataset": ds,
            "catalog_dataset": catalog_name.get((folder, entry), ""),
            "catalog_entry": entry,
            "model": model,
            "model_family": MODEL_FAMILY[model],
            "val_accuracy": val.get("accuracy") if val else None,
            "test_accuracy": test.get("accuracy"),
            "test_macro_precision": test["macro"][0],
            "test_macro_recall": test["macro"][1],
            "test_macro_f1": test["macro"][2],
            "test_weighted_f1": test["weighted"][2],
            "test_f1_per_emotion": test["per_emotion"],
        }
    )
runs.sort(
    key=lambda r: (r["language"], r["dataset"], MODEL_ORDER.index(r["model"]))
)

by_lang, by_ds = defaultdict(list), OrderedDict()
for r in runs:
    by_lang[r["language_folder"]].append(r)
    by_ds.setdefault((r["language_folder"], r["dataset"]), []).append(r)
by_ds = OrderedDict(
    sorted(by_ds.items(), key=lambda kv: (display(kv[0][0]), kv[0][1]))
)
bench_langs = sorted(by_lang, key=display)
n_runs, n_bench_ds = len(runs), len(by_ds)


def best(rows):
    return max(
        rows, key=lambda r: (r["test_accuracy"] or 0, r["test_macro_f1"])
    )


lang_stats = {}
for folder in bench_langs:
    accs = [r["test_accuracy"] for r in by_lang[folder]]
    b = best(by_lang[folder])
    lang_stats[folder] = {
        "folder": folder,
        "name": display(folder),
        "family": FAMILY[folder][0],
        "n_datasets": len({r["dataset"] for r in by_lang[folder]}),
        "mean": st.mean(accs),
        "sd": st.stdev(accs),
        "median": st.median(accs),
        "max": max(accs),
        "best_model": b["model"],
    }
stats_by_mean = sorted(lang_stats.values(), key=lambda s: -s["mean"])

model_stats = []
for mid, fam, hf, params in MODELS:
    rows = [r for r in runs if r["model"] == mid]
    model_stats.append(
        {
            "model": mid,
            "family": fam,
            "hf": hf,
            "params": params,
            "acc": st.mean(r["test_accuracy"] for r in rows),
            "macro_f1": st.mean(r["test_macro_f1"] for r in rows),
            "weighted_f1": st.mean(r["test_weighted_f1"] for r in rows),
        }
    )

write_json(
    "languages.json",
    [
        {
            "name": L["name"],
            "folder": L["folder"],
            "slug": L["slug"],
            "family": L["family"],
            "branch": L["branch"] or None,
            "iso": L["iso"],
            "countries": L["countries"],
            "dataset_count": len(L["datasets"]),
            "datasets": [d["name"] for d in L["datasets"]],
            "benchmarked": L["folder"] in by_lang,
            "url": f"{SITE}/languages/{L['slug']}.html",
        }
        for L in languages
    ],
)
write_json(
    "datasets.json",
    [
        {
            "name": d["name"],
            "full_name": d["full_name"] or None,
            "language": L["name"],
            "family": L["family"],
            "type": d["type"],
            "emotions": d["emotions"],
            "size": d["size"] or None,
            "samples": d["samples"] or None,
            "speakers": d["speakers"] or None,
            "recording": d["recording"] or None,
            "access": d["access"],
            "license": d["license"] or None,
            "website": first_url(d["website"]),
            "paper": first_url(d["paper"]),
            "download": first_url(d["download"]),
            "benchmarked": any(
                r["catalog_entry"] == d["file"]
                for r in by_lang.get(L["folder"], [])
            ),
            "url": f"{SITE}/languages/{L['slug']}.html#{d['anchor']}",
            "source": f"{REPO}/blob/main/datasets/"
            f"{quote(L['folder'])}/{quote(d['file'])}",
        }
        for L, d in all_datasets
    ],
)
write_json("runs.json", runs, indent=1)
write_json(
    "language_families.json",
    {
        L["name"]: {"family": L["family"], "branch": L["branch"] or None}
        for L in languages
    },
)
cols = [
    "run_id", "language", "iso", "family", "dataset", "catalog_dataset",
    "model", "model_family", "val_accuracy", "test_accuracy",
    "test_macro_precision", "test_macro_recall", "test_macro_f1",
    "test_weighted_f1",
]  # fmt: skip
buf = io.StringIO()
w = csv.writer(buf, lineterminator="\n")
w.writerow(cols + [f"test_f1_{e.lower()}" for e in EMOTIONS])
for r in runs:
    w.writerow(
        [r[c] for c in cols]
        + [r["test_f1_per_emotion"].get(e, "") for e in EMOTIONS]
    )
write(os.path.join(DOCS, "data", "runs.csv"), buf.getvalue())

NAV = [
    ("index.html", "Paper", "home"),
    ("speech-emotion-recognition.html", "Guide", "guide"),
    ("benchmark.html", "Results", "benchmark"),
    ("datasets.html", "Datasets", "datasets"),
    ("index.html#contribute", "Contribute", "contribute"),
    ("index.html#cite", "Cite", "cite"),
    (REPO, "GitHub", "github"),
]


def nav_html(prefix, active):
    items = "".join(
        f'<a href="{esc(h if h.startswith("http") else prefix + h)}"'
        f'{" aria-current=page" if k == active else ""}>{label}</a>'
        for h, label, k in NAV
    )
    return (
        '<header class="topbar"><div class="topbar-inner">'
        f'<a class="brand" href="{prefix}index.html">KuralHub</a>'
        f'<nav aria-label="Site">{items}</nav>{STAR_BUTTON}{THEME_BUTTON}'
        "</div></header>"
    )


def footer_html(prefix):
    return f"""<footer class="site"><div class="inner">
  <span>KuralHub · Interspeech 2026 · <a href="{DOI_URL}">doi:{DOI}</a> · Maintained by <a href="{AUTHOR_URL}" rel="author">Luxshan Thavarasa</a></span>
  <nav aria-label="Footer">
    <a href="{prefix}index.html">Paper</a>
    <a href="{prefix}speech-emotion-recognition.html">Guide</a>
    <a href="{prefix}benchmark.html">Results</a>
    <a href="{prefix}datasets.html">Datasets</a>
    <a href="{prefix}llms.txt">llms.txt</a>
    <a href="{prefix}llms-full.txt">llms-full.txt</a>
    <a href="{REPO}">GitHub</a>
    <a href="{prefix}index.html#contribute">Contribute</a>
  </nav>
</div></footer>"""


for page, active in [
    ("index.html", "home"),
    ("benchmark.html", "benchmark"),
    ("datasets.html", "datasets"),
    ("speech-emotion-recognition.html", "guide"),
]:
    inject(os.path.join(DOCS, page), "NAV", nav_html("", active))
    inject(os.path.join(DOCS, page), "FOOTER", footer_html(""))

T, N = "text", "num"


def table(caption, heads, rows, attrs="", foot=""):
    th = "".join(
        f'<th{" class=num" if kind == N else ""}'
        f'{f" data-sort={kind}" if kind else ""}>{label}</th>'
        for label, kind in heads
    )
    return (
        f'<div class="table-wrap"><table{attrs}>'
        + (f"<caption>{caption}</caption>" if caption else "")
        + f"<thead><tr>{th}</tr></thead><tbody>{''.join(rows)}</tbody>"
        + (f"<tfoot>{foot}</tfoot>" if foot else "")
        + "</table></div>"
    )


def td(v, nd=2):
    return f'<td class="num">{fmt(v, nd)}</td>'


def heat_td(v):
    if v is None:
        return '<td class="heat"></td>'
    color = "#fff" if v > 0.62 else "inherit"
    return (
        f'<td class="heat" data-v="{v:.4f}" '
        f'style="background:rgba(var(--heat),{v * 0.85:.2f});color:{color}">'
        f"{fmt(v)}</td>"
    )


def lang_link(folder, prefix=""):
    return (
        f'<a href="{prefix}languages/{lang_slug(folder)}.html">'
        f"{esc(display(folder))}</a>"
    )


def logs_td(r):
    return (
        f'<td><a href="{REPO}/tree/main/results/train_val_test_logs/'
        f'{esc(r["run_id"])}">logs</a></td>'
    )


def options(values):
    return "".join(
        f'<option value="{esc(v)}">{esc(v)}</option>' for v in values
    )


def ds_label(r):
    return esc(r["catalog_dataset"] or r["dataset"])


idx = os.path.join(DOCS, "index.html")
inject(
    idx,
    "LANGSTATS",
    table(
        "<b>Table A.</b> Test accuracy per language over all 11 models and "
        "all of the language's datasets, sorted by mean. Computed from the "
        "released logs. Click a column to re-sort.",
        [
            ("Language", T), ("Family", T), ("Datasets", N), ("Mean", N),
            ("SD", N), ("Median", N), ("Best", N), ("Best run", T),
        ],  # fmt: skip
        [
            f'<tr><td>{lang_link(s["folder"])}</td><td>{esc(s["family"])}</td>'
            f'<td class="num">{s["n_datasets"]}</td>{td(s["mean"], 3)}'
            f'{td(s["sd"], 3)}{td(s["median"])}{td(s["max"])}'
            f'<td class="mono">{esc(s["best_model"])}</td></tr>'
            for s in stats_by_mean
        ],
    ),
)
top = max(m["macro_f1"] for m in model_stats)
inject(
    idx,
    "MODELSTATS",
    table(
        "<b>Table B.</b> The 11 frozen backbones and their mean test scores "
        f"across all {n_bench_ds} datasets, computed from the released logs. "
        "These differ by a point or two from the per-model F1 figures quoted "
        "in the paper. Parameter counts are approximate.",
        [
            ("Family", T), ("Checkpoint", T), ("Params", N),
            ("Accuracy", N), ("Macro-F1", N), ("Weighted-F1", N),
        ],  # fmt: skip
        [
            f'<tr{" class=hl" if m["macro_f1"] == top else ""}>'
            f'<td>{esc(m["family"])}</td><td class="mono">'
            f'<a href="https://huggingface.co/{esc(m["hf"])}">'
            f'{esc(m["model"])}</a></td>'
            f'<td class="num" data-v="{m["params"]}">~{m["params"]:,}M</td>'
            f'{td(m["acc"])}{td(m["macro_f1"])}{td(m["weighted_f1"])}</tr>'
            for m in model_stats
        ],
    ),
)

bpath = os.path.join(DOCS, "benchmark.html")
best_rows = []
for s in sorted(lang_stats.values(), key=lambda s: s["name"]):
    b = best(by_lang[s["folder"]])
    best_rows.append(
        f'<tr><td>{lang_link(s["folder"])}</td><td>{esc(s["family"])}</td>'
        f'<td class="mono">{esc(b["model"])}</td><td>{ds_label(b)}</td>'
        f'<td class="num">{pct(b["test_accuracy"])}</td>'
        f'{td(b["test_macro_f1"])}<td class="num">{pct(s["mean"])}</td></tr>'
    )
inject(
    bpath,
    "BEST",
    table(
        "<b>Best single run per language.</b> Test accuracy (%) and macro-F1 "
        "of the top run, next to the mean over all of that language's runs.",
        [
            ("Language", T), ("Family", T), ("Best model", T), ("Dataset", T),
            ("Test acc.", N), ("Macro-F1", N), ("Mean acc.", N),
        ],  # fmt: skip
        best_rows,
    ),
)

matrix_rows = []
for (folder, ds), rs in by_ds.items():
    rm = {r["model"]: r for r in rs}
    mean = st.mean(r["test_accuracy"] for r in rs)
    cells = "".join(
        heat_td(rm[m]["test_accuracy"] if m in rm else None)
        for m in MODEL_ORDER
    )
    matrix_rows.append(
        f"<tr><td>{lang_link(folder)}</td><td>{ds_label(rs[0])}</td>{cells}"
        f'<td class="num" data-v="{mean:.4f}"><b>{fmt(mean)}</b></td></tr>'
    )
avg_cells = "".join(
    f'<td class="num"><b>{fmt(m["acc"])}</b></td>' for m in model_stats
)
inject(
    bpath,
    "MATRIX",
    table(
        "<b>Test accuracy, dataset × model.</b> Darker cells are higher. The "
        "last column is the mean over the 11 models.",
        [("Language", T), ("Dataset", T)]
        + [(f'<span class="mono">{esc(m)}</span>', N) for m in MODEL_ORDER]
        + [("Mean", N)],
        matrix_rows,
        foot=f'<tr><td colspan="2"><b>Mean over {n_bench_ds} datasets</b>'
        f"</td>{avg_cells}<td></td></tr>",
    ),
)

run_rows = [
    f'<tr data-lang="{esc(r["language"])}" data-model="{esc(r["model"])}" '
    f'data-family="{esc(r["model_family"])}">'
    f'<td>{lang_link(r["language_folder"])}</td><td>{ds_label(r)}</td>'
    f'<td class="mono">{esc(r["model"])}</td>{td(r["val_accuracy"])}'
    f'{td(r["test_accuracy"])}{td(r["test_macro_f1"])}'
    f'{td(r["test_weighted_f1"])}{logs_td(r)}</tr>'
    for r in runs
]
model_families = list(OrderedDict((m[1], 1) for m in MODELS))
inject(
    bpath,
    "RUNS",
    f"""<div class="filters" data-table="#runs-table">
  <input type="search" placeholder="Search language, dataset or model" aria-label="Search runs">
  <select data-key="lang" aria-label="Language"><option value="">All languages</option>{options(display(f) for f in bench_langs)}</select>
  <select data-key="family" aria-label="Model family"><option value="">All model families</option>{options(model_families)}</select>
  <select data-key="model" aria-label="Model"><option value="">All models</option>{options(MODEL_ORDER)}</select>
  <span class="count">{n_runs} runs</span>
</div>
"""
    + table(
        f"<b>All {n_runs} runs.</b> Validation accuracy, test accuracy, and "
        "test macro-F1 and weighted-F1. Each run links to its classification "
        "reports, confusion matrices and loss curve on GitHub.",
        [
            ("Language", T), ("Dataset", T), ("Model", T), ("Val acc.", N),
            ("Test acc.", N), ("Macro-F1", N), ("Weighted-F1", N),
            ("Logs", None),
        ],  # fmt: skip
        run_rows,
        attrs=' id="runs-table"',
    ),
)

dpath = os.path.join(DOCS, "datasets.html")
lang_rows = []
for L in by_name:
    names = ", ".join(esc(d["name"]) for d in L["datasets"])
    iso = L["iso"].split()[0] if L["iso"] else ""
    lang_rows.append(
        f'<tr data-family="{esc(L["family"])}" '
        f'data-has="{"yes" if L["datasets"] else "no"}">'
        f'<td>{lang_link(L["folder"])}</td><td>{esc(L["family"])}</td>'
        f'<td class="mono">{esc(iso)}</td>'
        f'<td class="num">{len(L["datasets"])}</td>'
        f'<td>{names or "<span class=muted>none found</span>"}</td>'
        f'<td>{"yes" if L["folder"] in by_lang else ""}</td></tr>'
    )
inject(
    dpath,
    "LANGTABLE",
    f"""<div class="filters" data-table="#langs">
  <input type="search" placeholder="Search languages or dataset names" aria-label="Search languages">
  <select data-key="family" aria-label="Language family"><option value="">All families</option>{options(sorted({L["family"] for L in languages}))}</select>
  <select data-key="has" aria-label="Has datasets"><option value="">With or without datasets</option><option value="yes">Has at least one dataset</option><option value="no">No dataset found</option></select>
  <span class="count">{len(languages)} languages</span>
</div>
"""
    + table(
        f"<b>All {len(languages)} surveyed languages.</b> Benchmarked marks "
        f"the {len(bench_langs)} languages used in the paper's experiments.",
        [
            ("Language", T), ("Family", T), ("ISO", T), ("Datasets", N),
            ("Dataset names", None), ("Benchmarked", T),
        ],  # fmt: skip
        lang_rows,
        attrs=' id="langs"',
    ),
)

ds_rows = [
    f'<tr data-access="{esc(d["access"])}" data-lang="{esc(L["name"])}">'
    f'<td><a href="languages/{L["slug"]}.html#{d["anchor"]}">'
    f'{esc(d["name"])}</a></td><td>{esc(L["name"])}</td>'
    f'<td>{esc(d["type"])}</td><td>{esc(d["emotions"])}</td>'
    f'<td class="num" data-v="{number(d["samples"])}">{esc(d["samples"])}</td>'
    f'<td>{esc(d["recording"])}</td><td>{esc(d["access"])}</td>'
    f'<td>{esc(d["license"])}</td></tr>'
    for L, d in sorted(
        all_datasets, key=lambda x: (x[0]["name"], x[1]["name"].lower())
    )
]
accesses = sorted({d["access"] for _, d in all_datasets})
inject(
    dpath,
    "DSTABLE",
    f"""<div class="filters" data-table="#ds">
  <input type="search" placeholder="Search name, emotion or licence" aria-label="Search datasets">
  <select data-key="lang" aria-label="Language"><option value="">All languages</option>{options(L["name"] for L in by_name if L["datasets"])}</select>
  <select data-key="access" aria-label="Access"><option value="">Any access</option>{options(accesses)}</select>
  <span class="count">{len(all_datasets)} datasets</span>
</div>
"""
    + table(
        f"<b>All {len(all_datasets)} datasets.</b> Values come from the "
        "dataset pages in the repository. A blank cell means the source did "
        "not say.",
        [
            ("Dataset", T), ("Language", T), ("Type", T),
            ("Emotion labels", None), ("Samples", N), ("Recording", T),
            ("Access", T), ("Licence", T),
        ],  # fmt: skip
        ds_rows,
        attrs=' id="ds"',
    ),
)
inject(
    dpath,
    "JSONLD",
    jsonld(
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Speech emotion recognition datasets by language",
            "url": f"{SITE}/datasets.html",
            "description": f"Catalog of {len(all_datasets)} speech emotion "
            f"recognition datasets across {len(languages)} widely spoken "
            "languages, compiled for the KuralHub paper (Interspeech 2026).",
            "isPartOf": {
                "@type": "WebSite",
                "name": "KuralHub",
                "url": f"{SITE}/",
            },
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(languages),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": f"{L['name']} speech emotion recognition "
                        "datasets",
                        "url": f"{SITE}/languages/{L['slug']}.html",
                    }
                    for i, L in enumerate(by_name)
                ],
            },
        }
    ),
)


def link_list(pairs):
    return ", ".join(f'<a href="{esc(u)}">{esc(t)}</a>' for t, u in pairs)


def dataset_section(L, d, prefix):
    lic = (
        f'<a href="{esc(d["license_url"])}">{esc(d["license"])}</a>'
        if d["license_url"]
        else esc(d["license"] or "Not stated")
    )
    facts = [
        ("Type", esc(d["type"])),
        ("Emotion labels", esc(d["emotions"])),
        ("Size", esc(d["size"])),
        ("Speakers", esc(d["speakers"])),
        ("Recording", esc(d["recording"])),
        ("Access", esc(d["access"])),
        ("Licence", lic),
        ("File format", esc(d["file_format"])),
        ("Website", link_list(d["website"])),
        ("Paper", link_list(d["paper"])),
        ("Download", link_list(d["download"])),
        ("Contact", link_list(d["contact"])),
    ]
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in facts if v)
    ids = sorted(
        {
            r["dataset"]
            for r in by_lang.get(L["folder"], [])
            if r["catalog_entry"] == d["file"]
        }
    )
    bench = (
        '<p class="callout small">Used in the KuralHub benchmark (run ID '
        f'<code>{esc(", ".join(ids))}</code>). See the results above.</p>'
        if ids
        else ""
    )
    cites = (
        "".join(
            f'<div class="cite-box"><button class="copy-btn" '
            f'data-copy="#{d["anchor"]}-bib{i}">Copy</button>'
            f'<pre id="{d["anchor"]}-bib{i}"><code>{esc(c)}</code></pre></div>'
            for i, c in enumerate(d["citations"])
        )
        or '<p class="muted">No citation listed in the source entry.</p>'
    )
    note = (
        f'<p class="muted small">Note: {esc(d["note"])}</p>'
        if d["note"]
        else ""
    )
    alt = (
        f'<p class="alt-name">{esc(d["full_name"])}</p>'
        if d["full_name"]
        else ""
    )
    path = f'datasets/{quote(L["folder"])}/{quote(d["file"])}'
    return f"""<section class="entry" id="{d['anchor']}">
<h2>{esc(d['name'])}</h2>
{alt}<dl class="facts">{dl}</dl>
{md_block(d['overview_md'], L['folder'], prefix)}
{note}
{bench}
<h3>Citation</h3>
{cites}
<p class="small muted">Source: <a href="{REPO}/blob/main/{path}">datasets/{esc(L['folder'])}/{esc(d['file'])}</a> · <a href="{REPO}/edit/main/{path}">Suggest an edit</a></p>
</section>"""


def bench_section(L):
    rs = by_lang.get(L["folder"])
    if not rs:
        return ""
    s = lang_stats[L["folder"]]
    out = [
        '<h2 id="benchmark">Benchmark results</h2>',
        f'<p>{esc(L["name"])} is one of the {len(bench_langs)} languages in '
        "the KuralHub benchmark. Each of the 11 frozen speech models was "
        "trained with a small classification head on the shared emotions "
        f"and scored on a held-out test split. Over all {len(rs)} runs the "
        f'mean test accuracy was <b>{pct(s["mean"])}%</b> (median '
        f'{pct(s["median"])}%). The best run reached <b>{pct(s["max"])}%</b> '
        f'with <code>{esc(s["best_model"])}</code>. '
        '<a href="../benchmark.html">Compare with other languages</a>.</p>',
    ]
    for ds in sorted({r["dataset"] for r in rs}):
        drs = [r for r in rs if r["dataset"] == ds]
        b = best(drs)
        d = next(
            (
                x
                for x in L["datasets"]
                if x["file"] == RUN_DATASET_FILE.get(ds)
            ),
            None,
        )
        label = (
            f'<a href="#{d["anchor"]}">{esc(d["name"])}</a>' if d else esc(ds)
        )
        rows = [
            f'<tr{" class=hl" if r is b else ""}><td class="mono">'
            f'{esc(r["model"])}{BEST_TAG if r is b else ""}</td>'
            f'<td>{esc(r["model_family"])}</td>{td(r["val_accuracy"])}'
            f'{td(r["test_accuracy"])}{td(r["test_macro_f1"])}'
            f'{td(r["test_weighted_f1"])}{logs_td(r)}</tr>'
            for r in drs
        ]
        out.append(
            table(
                f"<b>{label}</b> (run ID <code>{esc(ds)}</code>). Scores on "
                "the test split, best run highlighted.",
                [
                    ("Model", T), ("Family", T), ("Val acc.", N),
                    ("Test acc.", N), ("Macro-F1", N), ("Weighted-F1", N),
                    ("Logs", None),
                ],  # fmt: skip
                rows,
            )
        )
    return "\n".join(out)


def describe(L):
    name, names = L["name"], [d["name"] for d in L["datasets"]]
    n = len(names)
    if not n:
        return (
            f"No public speech emotion recognition dataset for {name} turned "
            "up in the KuralHub survey of 70 languages. Know of one? Add it."
        )
    listed = (
        names[0] if n == 1 else ", ".join(names[:-1]) + " and " + names[-1]
    )
    if len(listed) > 50:
        listed = ", ".join(names[:2]) + f" and {n - 2} more"
    tail = (
        " Benchmark results for 11 models."
        if L["folder"] in by_lang
        else " Labels, size, licence and access."
    )
    plural = "s" if n > 1 else ""
    desc = (
        f"{n} speech emotion recognition dataset{plural} for {name}: "
        f"{listed}.{tail}"
    )
    return desc if len(desc) <= 160 else desc[:157].rsplit(" ", 1)[0] + "…"


def dataset_jsonld(L, d, url):
    parts = [
        f"{d['name']} is a {L['name']} speech emotion recognition dataset"
        + (f" ({d['type']})." if d["type"] else "."),
        f"Emotion labels: {d['emotions']}." if d["emotions"] else "",
        f"Size: {d['size']}." if d["size"] else "",
        clean(d["overview_md"]),
    ]
    desc = " ".join(p for p in parts if p)
    if len(desc) < 50:
        desc += " Documented in the KuralHub survey of SER datasets."
    node = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": d["full_name"] or d["name"],
        "alternateName": d["name"] if d["full_name"] else None,
        "description": desc[:4900],
        "url": f"{url}#{d['anchor']}",
        "sameAs": first_url(d["website"]),
        "inLanguage": (L["iso"].split() or [L["name"]])[0],
        "keywords": [
            f"{L['name']} speech emotion recognition",
            "speech emotion recognition dataset",
            "emotional speech corpus",
        ],
        "license": d["license_url"] or None,
        "isAccessibleForFree": True if d["access"] == "Open" else None,
        "includedInDataCatalog": {
            "@type": "DataCatalog",
            "name": "KuralHub",
            "url": f"{SITE}/datasets.html",
        },
    }
    return {k: v for k, v in node.items() if v is not None}


def language_page(L):
    prefix, name, n = "../", L["name"], len(L["datasets"])
    url = f"{SITE}/languages/{L['slug']}.html"
    in_bench = L["folder"] in by_lang
    folder_url = f"{REPO}/tree/main/datasets/{quote(L['folder'])}"
    n_open = sum(1 for d in L["datasets"] if d["access"] == "Open")
    fam = L["family"] + (f" ({L['branch']})" if L["branch"] else "")
    desc = describe(L)
    if n:
        lede = (
            f"KuralHub lists <b>{n}</b> speech emotion recognition "
            f"dataset{'s' if n > 1 else ''} for {esc(name)}"
            + (
                f", {n_open} of them openly available"
                if n > 1 and n_open
                else ""
            )
            + ". Each entry below gives the emotion labels, size, recording "
            "setup, licence, where to get it and how to cite it."
        )
        overview = '<h2 id="datasets">Datasets at a glance</h2>' + table(
            "",
            [
                ("Dataset", T), ("Type", T), ("Samples", N), ("Speakers", N),
                ("Recording", T), ("Access", T), ("Licence", T),
            ],  # fmt: skip
            [
                f'<tr><td><a href="#{d["anchor"]}">{esc(d["name"])}</a></td>'
                f'<td>{esc(d["type"])}</td>'
                f'<td class="num" data-v="{number(d["samples"])}">'
                f'{esc(d["samples"])}</td>'
                f'<td class="num" data-v="{number(d["speakers"])}">'
                f'{esc(d["speakers"])}</td>'
                f'<td>{esc(d["recording"])}</td><td>{esc(d["access"])}</td>'
                f'<td>{esc(d["license"])}</td></tr>'
                for d in L["datasets"]
            ],
        )
    else:
        n_none = sum(1 for x in languages if not x["datasets"])
        lede = (
            "The KuralHub survey did not find any speech emotion recognition "
            f"dataset for {esc(name)}. It is one of {n_none} widely spoken "
            "languages with no emotional speech corpus we could locate."
        )
        overview = f"""<h2 id="contribute">Know of a dataset?</h2>
<div class="callout cta">
<p>Be the first to add a speech emotion dataset for {esc(name)}. Your own corpus, one from a paper, or one you found online all count. A link is enough to get started, and we will help with the rest.</p>
<ul class="links">
<li><a href="{ISSUE_DATASET}">Suggest a dataset (form)</a></li>
<li><a href="{folder_url}">Open a pull request</a></li>
</ul>
</div>
<p class="small muted">For a pull request, copy the template in <a href="{REPO}/tree/main/template/sample"><code>template/sample</code></a> into <code>datasets/{esc(L['folder'])}/</code> and fill in what you know.</p>"""
    if in_bench:
        s = lang_stats[L["folder"]]
        lede += (
            f" {esc(name)} is also part of the benchmark. The best of 11 "
            f"models reached {pct(s['max'])}% test accuracy "
            f"(<code>{esc(s['best_model'])}</code>)."
        )

    facts = [
        ("Language family", esc(fam)),
        ("ISO code", esc(L["iso"])),
        ("Spoken mainly in", esc(L["countries"])),
        ("Datasets listed", str(n)),
        ("In benchmark", "Yes" if in_bench else "No"),
    ]
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in facts if v)
    entries = "".join(
        f'<li><a href="#{d["anchor"]}">{esc(d["name"])}</a></li>'
        for d in L["datasets"]
    )
    toc = '<ol><li><a href="#top">Overview</a></li>'
    if n:
        toc += '<li><a href="#datasets">Datasets at a glance</a></li>'
    else:
        toc += '<li><a href="#contribute">Contribute</a></li>'
    if in_bench:
        toc += '<li><a href="#benchmark">Benchmark results</a></li>'
    if n:
        toc += f"<li>Dataset entries<ol>{entries}</ol></li>"
    toc += "</ol>"

    crumbs = [
        ("KuralHub", f"{SITE}/"),
        ("Datasets", f"{SITE}/datasets.html"),
        (name, url),
    ]
    ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": t, "item": u}
                for i, (t, u) in enumerate(crumbs)
            ],
        }
    ] + [dataset_jsonld(L, d, url) for d in L["datasets"]]
    md_alt = f"../datasets/{quote(L['folder'])}/{quote(L['readme'])}"
    title = f"{name} Speech Emotion Recognition Datasets | KuralHub"
    scripts = "\n".join(jsonld(x) for x in ld)
    sections = "".join(dataset_section(L, d, prefix) for d in L["datasets"])
    more_cta = (
        f'<p class="callout cta">Know another {esc(name)} speech emotion '
        f"dataset, or a newer version of one listed here? "
        f'<a href="{ISSUE_DATASET}">Suggest it</a> or '
        f'<a href="{folder_url}">open a pull request</a>.</p>'
        if n
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="KuralHub">
<meta property="og:title" content="{esc(name)} speech emotion recognition datasets">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="text/markdown" href="{md_alt}" title="Source Markdown">
<link rel="alternate" type="text/plain" href="../llms.txt" title="llms.txt">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="author" href="{AUTHOR_URL}">
<link rel="stylesheet" href="../css/styles.css">
{THEME_SCRIPT}
{scripts}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
{nav_html(prefix, "datasets")}
<div class="layout with-toc">
<aside class="toc"><nav aria-label="On this page">{toc}</nav></aside>
<main id="content">
<p class="crumbs" id="top"><a href="../index.html">KuralHub</a><span aria-hidden="true">/</span><a href="../datasets.html">Datasets</a><span aria-hidden="true">/</span>{esc(name)}</p>
<h1>{esc(name)} speech emotion recognition datasets</h1>
<p class="lede">{lede}</p>
<dl class="facts">{dl}</dl>
{overview}
{bench_section(L)}
{sections}
<hr>
{more_cta}
<p class="small muted">This page is generated from <a href="{folder_url}"><code>datasets/{esc(L['folder'])}/</code></a> in the KuralHub repository.
If you use a dataset, cite its authors. If KuralHub helped you find it, please also <a href="../index.html#cite">cite the KuralHub paper</a>.</p>
</main>
</div>
{footer_html(prefix)}
<script src="../js/site.js" defer></script>
</body>
</html>
"""


lang_dir = os.path.join(DOCS, "languages")
os.makedirs(lang_dir, exist_ok=True)
for f in os.listdir(lang_dir):
    if f.endswith(".html"):
        os.remove(os.path.join(lang_dir, f))
for L in languages:
    write(os.path.join(lang_dir, f"{L['slug']}.html"), language_page(L))

with_data = [L for L in by_name if L["datasets"]]
without = [L["name"] for L in by_name if not L["datasets"]]
summary = (
    "KuralHub is an open catalog of speech emotion recognition (SER) datasets "
    f"for the {len(languages)} most widely spoken languages, plus a benchmark "
    "of 11 self-supervised speech models (HuBERT, wav2vec 2.0, WavLM, "
    f"Whisper) on {n_bench_ds} datasets in {len(bench_langs)} languages "
    f'({n_runs} runs). It accompanies the Interspeech 2026 paper "{TITLE}" '
    f"(doi:{DOI}) by Luxshan Thavarasa ({AUTHOR_URL}), Jubeerathan "
    "Thevakumar, Thanikan Sivatheepan and Uthayasanker Thayasivam, "
    "University of Moratuwa, Sri Lanka."
)
findings = """Key findings (figures as published in the paper):

- No single model is best for every language. Whisper had the highest mean F1 (0.70 for whisper-small and whisper-large), then HuBERT-base (0.68) and WavLM (0.64 large, 0.63 base-plus). wav2vec 2.0 models generalised worst.
- Dravidian languages are hard for every model. Kannada mean accuracy 0.275, Tamil 0.306 (best 0.44), Telugu best 0.53.
- More pre-training data does not guarantee better SER. Mandarin (0.755) and Indonesian (0.720) did well, while French (0.421), Spanish (0.365) and Russian (0.344) did not.
- Larger models are not better. log(parameters) correlates negatively with F1 (r = -0.18, p = 0.0007), and wav2vec2-base (0.58) beat wav2vec2-large-960h (0.30) and wav2vec2-large-lv60 (0.25).
- Fear is the hardest emotion (F1 0.38). Anger (0.54) and neutral (0.52) are the easiest."""
lang_lines = "\n".join(
    f"- [{L['name']}]({SITE}/languages/{L['slug']}.html): "
    + ", ".join(d["name"] for d in L["datasets"])
    + (" (benchmarked)" if L["folder"] in by_lang else "")
    for L in with_data
)
llms = f"""# KuralHub

> {summary}

{findings}

Topics: speech emotion recognition (SER), emotion recognition from speech, voice emotion detection, emotion detection and emotion classification models, emotional speech datasets, multilingual and low-resource SER benchmarks, self-supervised speech models.

Survey coverage: {len(languages)} languages surveyed, {len(with_data)} with at least one SER dataset, {len(without)} with none, {len(all_datasets)} datasets documented.

Cite as:

```
{CITATION}
```

## Paper

- [Web version of the paper]({SITE}/): abstract, method, results, figures, tables, FAQ and citation
- [Paper as Markdown]({SITE}/paper.md): the same content in plain Markdown
- [PDF on the ISCA Archive]({PDF_URL}): Proc. Interspeech 2026, pages 4673-4678
- [DOI]({DOI_URL})

## Data

- [Benchmark results, CSV]({SITE}/data/runs.csv): one row per run ({n_runs} rows) with accuracy, macro and weighted F1, per-emotion F1
- [Benchmark results, JSON]({SITE}/data/runs.json): the same data as JSON
- [Dataset catalog, JSON]({SITE}/data/datasets.json): all {len(all_datasets)} datasets with language, emotion labels, size, access, licence and links
- [Languages, JSON]({SITE}/data/languages.json): all {len(languages)} languages with family, ISO code and dataset counts

## Pages

- [Speech emotion recognition guide]({SITE}/speech-emotion-recognition.html): what SER is, how emotion detection and emotion recognition models work, which datasets and models to use, how to evaluate, FAQ
- [Results]({SITE}/benchmark.html): best model per language, dataset x model accuracy matrix, all {n_runs} runs
- [Dataset catalog]({SITE}/datasets.html): searchable tables of all languages and datasets

## Datasets by language

{lang_lines}

No dataset found for: {", ".join(without)}.

## Support the project

KuralHub is free and maintained by its authors. People who find it useful can support it by starring the GitHub repository ({REPO}), which helps other researchers find it, and by citing the Interspeech 2026 paper.

## Optional

- [llms-full.txt]({SITE}/llms-full.txt): the full paper text, every result table and every dataset entry in one file
- [GitHub repository]({REPO}): code, per-run logs and the dataset Markdown sources
- [Contributing]({REPO}/blob/main/CONTRIBUTING.md): how to add a dataset or a model
- [Suggest a dataset]({ISSUE_DATASET}): issue form for a dataset KuralHub is missing
- [Suggest a model]({ISSUE_MODEL}): issue form for a model to add to the benchmark
"""

paper_md = open(os.path.join(DOCS, "paper.md"), encoding="utf-8").read()
full = [
    f"# {TITLE}",
    "",
    f"> {summary}",
    "",
    f"Short index for agents: {SITE}/llms.txt",
    "",
    paper_md.split("\n", 1)[1].strip(),
    "",
    "## Mean test score per model (computed from the released logs)",
    "",
    "| Model | Family | Params (approx.) | Accuracy | Macro-F1 | Weighted-F1 |",
    "|---|---|---|---|---|---|",
]
full += [
    f"| {m['model']} | {m['family']} | {m['params']}M | {fmt(m['acc'])} "
    f"| {fmt(m['macro_f1'])} | {fmt(m['weighted_f1'])} |"
    for m in model_stats
]
full += [
    "",
    "## Test accuracy per language (all models, all datasets)",
    "",
    "| Language | Family | Datasets | Mean | SD | Median | Best | Best run |",
    "|---|---|---|---|---|---|---|---|",
]
full += [
    f"| {s['name']} | {s['family']} | {s['n_datasets']} | {fmt(s['mean'], 3)} "
    f"| {fmt(s['sd'], 3)} | {fmt(s['median'])} | {fmt(s['max'])} "
    f"| {s['best_model']} |"
    for s in stats_by_mean
]
full += [
    "",
    "## All runs (test accuracy / macro-F1)",
    "",
    "| Language | Dataset | " + " | ".join(MODEL_ORDER) + " |",
    "|---|---|" + "---|" * len(MODEL_ORDER),
]
for (folder, ds), rs in by_ds.items():
    rm = {r["model"]: r for r in rs}
    cells = " | ".join(
        (
            f"{fmt(rm[m]['test_accuracy'])} / {fmt(rm[m]['test_macro_f1'])}"
            if m in rm
            else ""
        )
        for m in MODEL_ORDER
    )
    label = rs[0]["catalog_dataset"] or ds
    full.append(f"| {display(folder)} | {label} | {cells} |")
full += ["", "## Dataset catalog", ""]
for L in by_name:
    fam = L["family"] + (f", {L['branch']}" if L["branch"] else "")
    full += [
        f"### {L['name']}",
        "",
        f"Family: {fam}. ISO: {L['iso'] or 'n/a'}. Spoken in: "
        f"{L['countries'] or 'n/a'}. Page: {SITE}/languages/{L['slug']}.html",
        "",
    ]
    if not L["datasets"]:
        full += ["No SER dataset found in the survey.", ""]
    for d in L["datasets"]:
        bits = [
            ("Type", d["type"]),
            ("Emotions", d["emotions"]),
            ("Size", d["size"]),
            ("Access", d["access"]),
            ("Licence", d["license"]),
            ("Website", first_url(d["website"])),
            ("Paper", first_url(d["paper"])),
            ("Download", first_url(d["download"])),
        ]
        name = d["name"] + (f" ({d['full_name']})" if d["full_name"] else "")
        details = ". ".join(f"{k}: {v}" for k, v in bits if v)
        full.append(f"- **{name}**. {details}.")
    full.append("")

write(os.path.join(DOCS, "llms.txt"), llms)
write(os.path.join(DOCS, "llms-full.txt"), "\n".join(full).rstrip() + "\n")

urls = [
    f"{SITE}/",
    f"{SITE}/speech-emotion-recognition.html",
    f"{SITE}/benchmark.html",
    f"{SITE}/datasets.html",
]
urls += [f"{SITE}/languages/{L['slug']}.html" for L in languages]
write(
    os.path.join(DOCS, "sitemap.xml"),
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    + "</urlset>\n",
)

print(
    f"languages: {len(languages)} ({len(with_data)} with data), "
    f"datasets: {len(all_datasets)}, benchmark: {len(bench_langs)} "
    f"languages / {n_bench_ds} datasets / {n_runs} runs"
)
