# filename: create_language_families.py
# execution: true
import json

# Define language families mapping
language_families = {
    # Indo-European
    "Indo-European": {
        "Germanic": ["Afrikaans (af)", "German (de)", "English (en)"],
        "Romance": ["Spanish (es)", "French (fr)", "Italian (it)", "Portuguese (pt)"],
        "Slavic": ["Polish (pl)", "Russian (ru)"],
        "Indo-Iranian": ["Persian (fa)", "Hindi (hi)", "Urdu (ur)", "Bengali (bn)"],
        "Hellenic": ["Greek (el)"]
    },
    # Afro-Asiatic
    "Afro-Asiatic": {
        "Semitic": ["Arabic (ar)"],
        "Cushitic": ["Amharic (am)"]
    },
    # Dravidian
    "Dravidian": ["Tamil (ta)", "Telugu (te)", "Kannada (kn)"],
    # Sino-Tibetan
    "Sino-Tibetan": ["Chinese (zh)"],
    # Japonic
    "Japonic": ["Japanese (ja)"],
    # Koreanic
    "Koreanic": ["Korean (ko)"],
    # Austronesian
    "Austronesian": ["Indonesian (id)"],
    # Uralic
    "Uralic": ["Hungarian (hu)"],
    # Niger-Congo
    "Niger-Congo": ["Swahili (sw)"],
    # Other
    "Other": ["Odia (or)"]
}

# Flatten the language families for easy lookups
language_to_family = {}
for family, subfamilies in language_families.items():
    if isinstance(subfamilies, list):
        for lang in subfamilies:
            language_to_family[lang] = {"family": family, "subfamily": None}
    else:
        for subfamily, langs in subfamilies.items():
            for lang in langs:
                language_to_family[lang] = {"family": family, "subfamily": subfamily}

# Load the benchmark data
with open('benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

# Check if all languages are covered in our family mapping
all_langs = set(benchmark_data.keys())
mapped_langs = set(language_to_family.keys())
missing_langs = all_langs - mapped_langs

print("Languages in benchmark.json:", len(all_langs))
print("Languages mapped to families:", len(mapped_langs))
if missing_langs:
    print("Missing language mappings for:", missing_langs)
    # Assign missing languages to "Other" category
    for lang in missing_langs:
        language_to_family[lang] = {"family": "Other", "subfamily": None}

# Save the language family mapping to use in our HTML
with open('language_families.json', 'w') as f:
    json.dump(language_to_family, f, indent=2)

print("Language families mapping created and saved to language_families.json")

# Get models used across all datasets
all_models = set()
for lang, datasets in benchmark_data.items():
    for dataset, benchmarks in datasets.items():
        for entry in benchmarks:
            all_models.add(entry["model"])

print("\nModels used in benchmarks:")
for model in sorted(all_models):
    print(f"- {model}")