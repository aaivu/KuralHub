# filename: read_benchmark_json.py
# execution: true
import json
import os

# Read the benchmark.json file
try:
    with open('benchmark.json', 'r') as f:
        benchmark_data = json.load(f)
    
    # Print the structure (keys) of the JSON file
    print("Top-level keys in benchmark.json:")
    print(json.dumps(list(benchmark_data.keys()), indent=2))
    
    # Get a sample of the data if it's not too large
    if isinstance(benchmark_data, dict):
        # Get one key as a sample
        sample_key = next(iter(benchmark_data))
        print(f"\nSample entry for key '{sample_key}':")
        print(json.dumps(benchmark_data[sample_key], indent=2)[:1000] + "..." if len(json.dumps(benchmark_data[sample_key], indent=2)) > 1000 else json.dumps(benchmark_data[sample_key], indent=2))
    
    # Check if we have a datasets directory
    print("\nChecking for datasets directory:")
    if os.path.exists('datasets'):
        print("Datasets directory exists!")
        # List some language directories as examples
        lang_dirs = os.listdir('datasets')
        print(f"Example language directories: {lang_dirs[:5] if len(lang_dirs) > 5 else lang_dirs}")
    else:
        print("Datasets directory not found in the current location.")
except Exception as e:
    print(f"Error reading the file: {e}")