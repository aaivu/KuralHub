import os
import re

def extract_accuracy(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        match = re.search(r"accuracy\s+([0-9\.]+)", content)
        return float(match.group(1)) if match else None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def generate_markdown(directory, output_file):
    entries = []
    
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
                entries.append((language_code, dataset_name, model_name, val_acc, test_acc, completed))
    
    with open(output_file, "w") as md_file:
        md_file.write("# Model Benchmarks\n\n")
        md_file.write("| Language Code | Dataset Name | Model Name | Val Accuracy | Test Accuracy | Completed |\n")
        md_file.write("|--------------|-------------|------------|--------------|--------------|-----------|\n")
        
        for lang, dataset, model, val_acc, test_acc, completed in entries:
            val_acc_str = f"{val_acc:.2f}" if val_acc is not None else "N/A"
            test_acc_str = f"{test_acc:.2f}" if test_acc is not None else "N/A"
            md_file.write(f"| {lang} | {dataset} | {model} | {val_acc_str} | {test_acc_str} | {completed} |\n")
    
    print(f"Markdown file '{output_file}' generated successfully!")

directory = "./train_val_test_logs"
output_file = "benchmark.md"
generate_markdown(directory, output_file)
