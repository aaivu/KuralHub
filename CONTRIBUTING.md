# Contributing to KuralHub

KuralHub grows with outside help. 25 of the 70 languages we surveyed still have no speech emotion dataset we could find, and the benchmark so far covers 11 models. New datasets, new models and corrections are all welcome.

## Suggest something quickly

You don't need to write any code to help.

- [Suggest a dataset](https://github.com/aaivu/KuralHub/issues/new?template=add-dataset.yml): a name and a link are enough.
- [Suggest a model](https://github.com/aaivu/KuralHub/issues/new?template=add-model.yml): tell us which checkpoint to try.
- Spotted a mistake? Every dataset section on the [website](https://aaivu.github.io/KuralHub/datasets.html) has a "Suggest an edit" link.

## Add a dataset

1. Fork the repository and create a branch, e.g. `add-dataset/<language>-<name>`.
2. Copy `template/sample/dataset.md` to `datasets/<Language>/<DatasetName>.md` and fill in what you know. Leave a field as `Not Specified` rather than guessing.
3. Add a row for it to the table in `datasets/<Language>/Readme.md`.
4. For a language that has no folder yet, copy `template/sample/Readme.md` as well, and add the language to `FAMILY` in `scripts/build_site.py`.
5. Run `make site` (or `./scripts/sync-datasets.sh`) to rebuild the website, then open a pull request.

## Add a model to the benchmark

Results are only comparable if every model uses the same recipe: frozen backbone, mean-pooled last-layer features, the two-layer head in `src/model/model.py`, and the default settings in `src/scripts/run_training.py`.

1. Add the checkpoint to `BASE_MODEL` in `src/utils/constant.py`.
2. Map it to a feature extractor in `FeatureExtractorFactory` in `src/model/base_models.py`. Encoders that take raw waveforms (`input_values`), like wav2vec 2.0, HuBERT and WavLM, work with the base class as is. Whisper-style models that take log-Mel features follow `WhisperFeatureExtractor`.
3. Set up the data (`make download_dataset` needs a Kaggle API key, then `make meta_extract`).
4. Train on each benchmark dataset, for example:

   ```bash
   DATASET=EMOTA BASE_MODEL=YOUR_MODEL make train_model
   ```

   Logs are written to `results/train_val_test_logs/<iso>_<dataset>_<model>/`.
5. Add the model to `MODELS` in `scripts/build_site.py`, run `make site`, and open a pull request with the code changes and the new log folders.

Running every dataset needs a GPU and some time. A pull request covering a few datasets is still useful, so say which ones you ran.

## Before you open a pull request

```bash
make setup          # Python 3.12+
make lint
make test
```

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md). Questions are welcome as issues.
