import os
import re
import json
from collections import defaultdict
from src.utils.constant import LANGUAGE

def get_language_name(code):
    for lang in LANGUAGE:
        if lang.value == code:
            return f"{lang.name.capitalize()} ({code})"
    return code

def extract_accuracy(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        match = re.search(r"accuracy\s+([0-9\.]+)", content)
        return float(match.group(1)) if match else None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def generate_benchmark(directory, output_md, output_json):
    data = defaultdict(lambda: defaultdict(list))
    json_data = {}
    
    for folder in sorted(os.listdir(directory)):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            parts = folder.split("_")
            if len(parts) >= 3:
                language_code = parts[0]
                dataset_name = parts[1]
                model_name = "_".join(parts[2:])
                
                test_file = os.path.join(folder_path, f"{folder}_test_classification_report.txt")
                val_file = os.path.join(folder_path, f"{folder}_val_classification_report.txt")
                
                test_acc = extract_accuracy(test_file) if os.path.exists(test_file) else None
                val_acc = extract_accuracy(val_file) if os.path.exists(val_file) else None
                
                completed = "✅" if test_acc is not None and val_acc is not None else "❌"
                data[language_code][dataset_name].append((model_name, val_acc, test_acc, completed))
                
                if get_language_name(language_code) not in json_data:
                    json_data[get_language_name(language_code)] = {}
                if dataset_name not in json_data[get_language_name(language_code)]:
                    json_data[get_language_name(language_code)][dataset_name] = []
                json_data[get_language_name(language_code)][dataset_name].append({
                    "model": model_name,
                    "val_accuracy": val_acc,
                    "test_accuracy": test_acc,
                    "completed": completed,
                    "logs_path": f"{language_code}_{dataset_name}_{model_name}",
                })
    
    with open(output_md, "w") as md_file:
        md_file.write("# Model Benchmarks\n\n")
        md_file.write("## Models Evaluated\n")
        md_file.write(", ".join(sorted(set(m for d in data.values() for models in d.values() for m, _, _, _ in models))) + "\n\n")
        
        for language_code, datasets in sorted(data.items()):
            language_name = get_language_name(language_code)
            md_file.write(f"## {language_name}\n\n")
            for dataset, models in sorted(datasets.items()):
                md_file.write(f"### {dataset}\n\n")
                md_file.write("| No | Model Name | Val Accuracy | Test Accuracy | Completed |\n")
                md_file.write("|----|------------|--------------|--------------|-----------|\n")
                no = 1
                for model, val_acc, test_acc, completed in sorted(models):
                    val_acc_str = f"{val_acc:.2f}" if val_acc is not None else "N/A"
                    test_acc_str = f"{test_acc:.2f}" if test_acc is not None else "N/A"
                    md_file.write(f"| {no} | {model} | {val_acc_str} | {test_acc_str} | {completed} |\n")
                    no += 1
                md_file.write("\n")
    
    with open(output_json, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    
    print(f"Markdown file '{output_md}' and JSON file '{output_json}' generated successfully!")

directory = "./results/train_val_test_logs"
output_md = "benchmark.md"
output_json = "./results/benchmark.json"
generate_benchmark(directory, output_md, output_json)
