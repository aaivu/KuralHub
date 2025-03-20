import concurrent.futures
import json
import os

from kaggle.api.kaggle_api_extended import KaggleApi

from src.utils.constant import DATASET


def dataset_exists(api, dataset):
    """Check if dataset already exists on Kaggle."""
    owner, dataset_name = dataset.url.split("/")
    datasets = api.dataset_list(user=owner)
    dataset_ids = [d.ref for d in datasets]

    return dataset.url in dataset_ids


def create_metadata(dataset):
    """Create dataset-metadata.json for Kaggle upload."""
    metadata_path = os.path.join(dataset.path, "dataset-metadata.json")
    os.makedirs(dataset.path, exist_ok=True)

    metadata = {
        "title": f"SER-{dataset.name}",
        "id": dataset.url,
        "licenses": [{"name": "CC0-1.0"}],
    }

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Metadata created for {dataset.name} at {metadata_path}")


def upload_to_kaggle(api, dataset):
    """Upload dataset to Kaggle if not already uploaded."""
    if dataset_exists(api, dataset):
        print(f"⏩ Skipping {dataset.name}, already exists on Kaggle.")
        return

    if not os.path.exists(dataset.path):
        print(f"❌ Dataset path not found: {dataset.path}")
        return

    try:
        create_metadata(dataset)
        api.dataset_create_new(dataset.path)
        print(f"🚀 Successfully uploaded: {dataset.name}")
    except Exception as e:
        print(f"⚠️ Error uploading {dataset.name}: {e}")


def main():
    api = KaggleApi()
    api.authenticate()

    datasets = [dataset_enum.value for dataset_enum in DATASET]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(upload_to_kaggle, api, dataset): dataset
            for dataset in datasets
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                dataset = futures[future]
                print(f"⚠️ Failed to upload {dataset.name}: {e}")


if __name__ == "__main__":
    main()
