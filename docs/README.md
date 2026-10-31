# KuralHub website (`docs/`)

The public website at https://aaivu.github.io/KuralHub/, served by GitHub Pages from the `docs/` folder on `main`. Plain HTML and CSS, no framework, no build step on the server.

## Pages

| File | What it is | Edited by |
|---|---|---|
| `index.html` | The paper as a web page (abstract, method, results, FAQ, citation) | hand, plus generated tables |
| `benchmark.html` | Best model per language, dataset × model matrix, all 363 runs | hand, plus generated tables |
| `datasets.html` | Searchable tables of all languages and datasets | hand, plus generated tables |
| `languages/<slug>.html` | One page per language with every dataset entry | fully generated |
| `paper.md` | Markdown version of `index.html` (also folded into `llms-full.txt`) | hand |
| `llms.txt`, `llms-full.txt` | Plain-text versions for LLMs and agents ([llmstxt.org](https://llmstxt.org/)) | generated |
| `data/` | `runs.csv`, `runs.json`, `datasets.json`, `languages.json`, `language_families.json` | generated |
| `sitemap.xml`, `robots.txt` | Crawling | generated / hand |
| `datasets/` | Mirror of the repository's `datasets/*.md` | generated |

Blocks between `<!-- NAME:START -->` and `<!-- NAME:END -->` in the hand-written pages are overwritten by the build. Edit everything else directly.

## Rebuilding

After changing anything in `datasets/` or `results/`:

```bash
./scripts/sync-datasets.sh
```

This mirrors the dataset Markdown and runs `scripts/build_site.py` (standard library only, Python 3.9+). The script parses the dataset files and the 363 classification reports in `results/train_val_test_logs/` and regenerates everything listed above. `make site` does the same.

If you add a new language folder, also add it to `FAMILY` in `scripts/build_site.py`. If you add a benchmark run on a new dataset, map its run ID to the catalog file in `RUN_DATASET_FILE`.

If you change prose in `index.html`, update `paper.md` to match.

## Local preview

```bash
make run_ui    # http://localhost:8000
```

## Search and AI discoverability

- Every page is static HTML, so crawlers that do not run JavaScript see all content. `js/site.js` only adds sorting, filtering, copy buttons and figure zoom.
- `index.html` carries Google Scholar `citation_*` meta tags and JSON-LD for `ScholarlyArticle`, `Dataset`, `SoftwareSourceCode`, `FAQPage` and `WebSite`. Each language page has `BreadcrumbList` and one `Dataset` node per catalogued dataset (for Google Dataset Search).
- `llms.txt` and `llms-full.txt` are linked from every page footer and from `<link rel="alternate">` in the page heads.
- `robots.txt` only takes effect at a host root. For a project site like this one, crawlers read `https://aaivu.github.io/robots.txt` instead, so submit `sitemap.xml` directly in Google Search Console and Bing Webmaster Tools.
