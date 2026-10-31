.PHONY: help venv setup test test_all lint format_check format clear \
	download_dataset meta_extract train_model site run_ui

PYTHON ?= python3.12
VENV = . .venv/bin/activate &&

help:
	@echo "setup             create .venv and install requirements-dev.txt (Python 3.12+)"
	@echo "test / test_all   run unit tests / also the model-download tests"
	@echo "lint              flake8 on src/"
	@echo "format            black + isort on src/ and scripts/"
	@echo "download_dataset  fetch the benchmark corpora from Kaggle"
	@echo "meta_extract      build meta_csvs/ for every dataset"
	@echo "train_model       train one head (DATASET=... BASE_MODEL=...)"
	@echo "site              rebuild the website in docs/"
	@echo "run_ui            serve docs/ at http://localhost:8000"

venv:
	$(PYTHON) -m venv .venv

setup: venv
	$(VENV) pip install --upgrade pip && pip install -r requirements-dev.txt

test:
	$(VENV) pytest src/

test_all:
	$(VENV) ENVIRONMENT=local pytest src/

lint:
	$(VENV) flake8 src/

format_check:
	$(VENV) black --check --line-length 79 src/ scripts/ && isort --check --profile black --line-length 79 src/

format:
	$(VENV) black --line-length 79 src/ scripts/ && isort --profile black --line-length 79 src/

download_dataset:
	$(VENV) python -m src.scripts.download_datasets

meta_extract:
	$(VENV) python -m src.scripts.meta_extractor

train_model:
	$(VENV) python -m src.scripts.run_training

site:
	./scripts/sync-datasets.sh

run_ui:
	python3 -m http.server 8000 --directory docs

clear:
	rm -rf __pycache__ .pytest_cache dist build *.egg-info
