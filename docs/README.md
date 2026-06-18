# KuralHub website (`docs/`)

This folder is the **public website** for KuralHub, served by **GitHub Pages**.
It is fully self-contained (no build step, no framework) and works both locally
and on Pages.

**Live URL:** https://aaivu.github.io/KuralHub/

## Enable GitHub Pages (one-time)

> GitHub Pages on the free plan requires the repository to be **public**.

1. Make the repository public (Settings → General → Danger Zone → Change visibility).
2. Go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Set **Branch = `main`** and **Folder = `/docs`**, then **Save**.
5. Wait ~1 minute; the site goes live at `https://aaivu.github.io/KuralHub/`.

## Structure

```
docs/
├── index.html          Landing page (about, methodology, findings, team, citation)
├── benchmark.html      Interactive benchmark (filter by family / model)
├── datasets.html       Dataset catalog (search + browse 70+ languages)
├── css/styles.css      Design system
├── js/                 main.js · data.js · benchmark.js · datasets.js
├── data/               benchmark.json · language_families.json · languages.json
├── datasets/           Mirror of repo /datasets markdown (generated — see below)
└── assets/             favicon, charts (img/), profile photos (profiles/)
```

## Updating the site after changing data

The dataset docs and benchmark are **mirrored/generated** into `docs/` so the site
is self-contained. After editing `datasets/` or regenerating the benchmark, run:

```bash
./scripts/sync-datasets.sh
```

This re-mirrors `datasets/*.md` into `docs/datasets/`, rebuilds
`docs/data/languages.json`, and refreshes `docs/data/benchmark.json` from
`results/benchmark.json`.

## Researcher photos

Add square photos to `docs/assets/profiles/` — see the README there for the exact
filenames. Missing photos fall back to initials automatically.

## Local preview

```bash
make run_ui          # serves docs/ at http://localhost:8000
# or:
python3 -m http.server 8000 --directory docs
```

## SEO & AI / agent discovery (GEO/AEO)

The site is optimized for both classic search engines and AI answer engines:

- **Static, crawlable content** — the 70-language catalog (datasets page) and the
  "best model per language" table (benchmark page) are pre-rendered into the HTML
  by `scripts/build_site.py`, so bots that don't run JavaScript (most AI crawlers,
  and Google's first pass) still see the content. JS only enhances it.
- **Structured data (JSON-LD)** — `Dataset` (incl. an `ItemList` of all 90+
  datasets for Google Dataset Search), `ScholarlyArticle`, `FAQPage`, `WebSite`
  (+ sitelinks SearchAction), `Organization`, `CollectionPage`, `BreadcrumbList`.
- **`llms.txt` / `llms-full.txt`** — concise, structured summaries for LLMs/agents
  (per the llmstxt.org convention).
- **`robots.txt`** — explicitly *welcomes* AI crawlers (GPTBot, ClaudeBot,
  PerplexityBot, Google-Extended, CCBot, …) plus search bots; links the sitemap.
- **FAQ** with `FAQPage` schema targeting common queries ("what speech emotion
  datasets exist", "best model for SER", …) for featured snippets and AI answers.
- Per-page titles/descriptions/keywords, canonical URLs, Open Graph + Twitter
  cards, `sitemap.xml`, and `?q=` / `?lang=` deep links on the datasets page.

These regenerate via `./scripts/sync-datasets.sh` (which runs `build_site.py`).

### After the site is live — off-page steps (these drive ranking)

On-page is done; ranking #1 also needs these (do them once the repo is public):

1. **Google Search Console** — verify the site, submit `sitemap.xml`.
2. **Bing Webmaster Tools** — verify + submit sitemap.
3. **Google Dataset Search** — it auto-discovers via the `Dataset` JSON-LD once
   indexed; confirm at datasetsearch.research.google.com.
4. **Backlinks** — link the site from the paper, the GitHub repo's About/website
   field, your Google Scholar/lab pages, and list it on Papers with Code and
   Hugging Face. Backlinks + citations are the biggest ranking factor.

## To finalize once the paper is public

- Replace the "To appear" BibTeX note and the *Interspeech 2026 / Accepted* badge
  with the final citation, DOI / arXiv link.
- Fill in real Google Scholar profile links in `index.html` (`TEAM` array).
- Optionally replace `assets/img/og-image.png` with a custom social card.
