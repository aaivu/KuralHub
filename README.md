<div align="center">

# KuralHub: Exposing Typological Capability Frontiers in Multilingual Speech Emotion Recognition

[![Interspeech 2026](https://img.shields.io/badge/Interspeech-2026-orange)](https://doi.org/10.21437/Interspeech.2026-3502)
[![Paper](https://img.shields.io/badge/Paper-PDF-red)](https://www.isca-archive.org/interspeech_2026/thavarasa26_interspeech.pdf)
[![DOI](https://img.shields.io/badge/DOI-10.21437%2FInterspeech.2026--3502-blue)](https://doi.org/10.21437/Interspeech.2026-3502)
[![Website](https://img.shields.io/badge/Website-aaivu.github.io%2FKuralHub-blue)](https://aaivu.github.io/KuralHub/)
[![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen)](CONTRIBUTING.md)

**[Website](https://aaivu.github.io/KuralHub/) · [Paper (PDF)](https://www.isca-archive.org/interspeech_2026/thavarasa26_interspeech.pdf) · [Dataset catalog](https://aaivu.github.io/KuralHub/datasets.html) · [Results](https://aaivu.github.io/KuralHub/benchmark.html)**

</div>

KuralHub is an open catalog of speech emotion recognition (SER) datasets for the 70 most widely spoken languages, and a benchmark of 11 self-supervised speech models on 33 of those datasets in 29 languages. It accompanies our Interspeech 2026 paper.

| | |
|---|---|
| Languages surveyed | 70 (45 with at least one dataset) |
| Datasets documented | 90 |
| Languages / datasets benchmarked | 29 / 33 |
| Models | 11 (HuBERT, wav2vec 2.0, WavLM, Whisper) |
| Training runs | 363 |

## Key findings

- **No model is best everywhere.** Whisper had the highest mean F1 (0.70), then HuBERT-base (0.68) and WavLM (0.63 to 0.64), but HuBERT won for nine languages and WavLM for English and Swahili.
- **Dravidian languages fail across the board.** Kannada averaged 0.275 accuracy and Tamil 0.306, with little spread between models.
- **More pre-training data is not enough.** Mandarin and Indonesian were easy, while French, Spanish and Russian were not.
- **Bigger models are not better.** log(parameters) is negatively correlated with F1 (r = −0.18, p = 0.0007).
- **Fear is the hardest emotion** (F1 0.38). Anger and neutral are the easiest.

The [website](https://aaivu.github.io/KuralHub/) has the full write-up with figures and tables.

## Repository layout

```
KuralHub/
├── datasets/<Language>/        # the survey: one folder per language
│   ├── Readme.md               #   language info + table of its datasets
│   └── <Dataset>.md            #   one file per dataset (labels, size, licence, access, BibTeX)
├── results/
│   ├── train_val_test_logs/    # 363 runs: classification reports, confusion matrices, loss curves
├── src/                        # data loading, model, training code
├── template/sample/            # template for adding a language or dataset
├── scripts/                    # website build (build_site.py, sync-datasets.sh)
└── docs/                       # the website (GitHub Pages)
```

## How to use

**Find a dataset.** Browse the [catalog](https://aaivu.github.io/KuralHub/datasets.html) or open `datasets/<Language>/Readme.md`. Each dataset file says how to get the data (direct download or request) and under which licence.

**Use the results.** Every run is in [`docs/data/runs.csv`](docs/data/runs.csv) (accuracy, macro/weighted F1, per-emotion F1) and on the [results page](https://aaivu.github.io/KuralHub/benchmark.html). Raw reports are in `results/train_val_test_logs/`.

**Re-run an experiment.**

```bash
make setup              # virtualenv + requirements (Python 3.12+)
make download_dataset   # needs a Kaggle API key in ~/.kaggle/kaggle.json
make meta_extract       # builds the per-dataset metadata CSVs
DATASET=EMOTA BASE_MODEL=WAVLM_LARGE make train_model
```

`DATASET` and `BASE_MODEL` take the names defined in `src/utils/constant.py`. `BATCH_SIZE`, `LEARNING_RATE`, `EPOCHS` and `EARLY_STOPPING_PATIENCE` can be set the same way.

## Contributing

Know of a dataset we missed, or found a mistake? Add it under `datasets/<Language>/` using the template in `template/sample/` and open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md). After changing `datasets/` or `results/`, run `./scripts/sync-datasets.sh` to rebuild the website.

## Citation

Thavarasa, L., Thevakumar, J., Sivatheepan, T., Thayasivam, U. (2026) KuralHub: Exposing Typological Capability Frontiers in Multilingual Speech Emotion Recognition. Proc. Interspeech 2026, 4673-4678, doi: [10.21437/Interspeech.2026-3502](https://doi.org/10.21437/Interspeech.2026-3502)

```bibtex
@inproceedings{thavarasa26_interspeech,
  title     = {{KuralHub: Exposing Typological Capability Frontiers in Multilingual Speech Emotion Recognition}},
  author    = {Luxshan Thavarasa and Jubeerathan Thevakumar and Thanikan Sivatheepan and Uthayasanker Thayasivam},
  year      = {2026},
  booktitle = {{Interspeech 2026}},
  pages     = {4673--4678},
  doi       = {10.21437/Interspeech.2026-3502},
  issn      = {2958-1796},
}
```

If you use one of the catalogued datasets, please also cite its original authors. Each dataset file includes their BibTeX.

## Authors

| Name | Email | LinkedIn |
|---|---|---|
| Luxshan Thavarasa\* | [luxshan.20@cse.mrt.ac.lk](mailto:luxshan.20@cse.mrt.ac.lk) | [LinkedIn](https://linkedin.com/in/lux-thavarasa) |
| Jubeerathan Thevakumar\* | [jubeerathan.25@cse.mrt.ac.lk](mailto:jubeerathan.25@cse.mrt.ac.lk) | [LinkedIn](https://lk.linkedin.com/in/jubeerathan-thevakumar-87b9b8255) |
| Thanikan Sivatheepan | [thanikan.20@cse.mrt.ac.lk](mailto:thanikan.20@cse.mrt.ac.lk) | [LinkedIn](https://lk.linkedin.com/in/sthanikan2000) |
| Uthayasanker Thayasivam (supervisor) | [rtuthaya@cse.mrt.ac.lk](mailto:rtuthaya@cse.mrt.ac.lk) | [LinkedIn](https://lk.linkedin.com/in/rtuthaya) |

\*Equal contribution. All authors are with the Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka.

## Acknowledgements

We thank Braveenan Sritharan for mentorship, and the creators of every dataset listed here for releasing their data openly or on request.

## License

Code and documentation in this repository are released under the [MIT License](LICENSE). The datasets themselves are not redistributed here and keep their own licences.
