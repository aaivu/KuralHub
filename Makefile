.PHONY: venv setup sync test lint format-check format clear help

help:
	@echo "Available targets for KuralHub:"
	@echo "  venv           - Create and activate a virtual environment"
	@echo "  setup          - Install pip and project dependencies"
	@echo "  sync           - Install project dependencies"
	@echo "  test           - Run tests using pytest"
	@echo "  lint           - Run flake8 for linting (src only)"
	@echo "  format-check   - Check code formatting using black and isort (src only)"
	@echo "  format         - Format code using black and isort (src only)"
	@echo "  clear          - Clean up temporary files like __pycache__ and .pytest_cache"

venv:
	python3 -m venv .venv
	@echo "Virtual environment created. Run 'source .venv/bin/activate' to activate it."

setup: venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements.txt
	@echo "Dependencies installed."

sync:
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && pip install -r dev-requirements.txt
	@echo "Dependencies synchronized."

test:
	. .venv/bin/activate && pytest src/

test_all:
	export ENVIRONMENT=local && . .venv/bin/activate && pytest src/

lint:
	. .venv/bin/activate && flake8 src/

format_check:
	. .venv/bin/activate && black --check --line-length 79 src/ && isort --check src/

format:
	. .venv/bin/activate && black --line-length 79 src/ && isort src/

download_dataset:
	. .venv/bin/activate && python3 -m src.scripts.download_datasets

upload_dataset:
	. .venv/bin/activate && python3 -m src.scripts.bulk_kaggle_dataset_uploader

meta_extract:
	. .venv/bin/activate && python3 -m src.scripts.meta_extractor

train_model:
	. .venv/bin/activate && python3 -m src.scripts.run_training

generate_benchmark:
	. .venv/bin/activate && python3 generate_benchmark.py

run_ui:
	python -m http.server 8000

clear:
	@echo "Cleaning up..."
	rm -rf __pycache__ .pytest_cache dist build *.egg-info
	@echo "Done."