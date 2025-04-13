# filename: create_website_files.py
# execution: true
import json
import os
import html

# First, let's update our language families mapping to include Turkish
with open('language_families.json', 'r') as f:
    language_to_family = json.load(f)

# Add Turkish to the correct language family
language_to_family["Turkish (tr)"] = {"family": "Turkic", "subfamily": None}

# Save the updated mapping
with open('language_families.json', 'w') as f:
    json.dump(language_to_family, f, indent=2)
print("Updated language families mapping to include Turkish in the Turkic family")

# Load benchmark data
with open('benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

# Create directory structure
os.makedirs('website', exist_ok=True)
print("Created website directory")

# Generate index.html (Home Page)
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KuralHub - Speech Emotion Recognition Benchmark</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-indigo-600 text-white shadow-lg">
        <div class="container mx-auto px-6 py-3 flex justify-between items-center">
            <a href="index.html" class="text-2xl font-bold">KuralHub</a>
            <div class="space-x-4">
                <a href="index.html" class="hover:text-indigo-200">Home</a>
                <a href="benchmark.html" class="hover:text-indigo-200">Benchmark</a>
                <a href="datasets.html" class="hover:text-indigo-200">Datasets</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <div class="bg-indigo-700 text-white py-16">
        <div class="container mx-auto px-6 text-center">
            <h1 class="text-4xl font-bold mb-4">Speech Emotion Recognition Benchmark</h1>
            <p class="text-xl mb-8">Comprehensive evaluation of SER across 30+ languages and 11 state-of-the-art models</p>
            <div class="flex justify-center space-x-4">
                <a href="benchmark.html" class="bg-white text-indigo-700 px-6 py-2 rounded-lg font-semibold hover:bg-indigo-100">View Benchmark</a>
                <a href="datasets.html" class="bg-transparent border border-white text-white px-6 py-2 rounded-lg font-semibold hover:bg-indigo-600">Explore Datasets</a>
            </div>
        </div>
    </div>

    <!-- Project Description -->
    <div class="container mx-auto px-6 py-12">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl font-bold text-gray-800 mb-6">About the Project</h2>
            <p class="text-lg text-gray-600 mb-6">
                KuralHub is a comprehensive research initiative focused on Speech Emotion Recognition (SER) across the world's languages. 
                We have benchmarked all available datasets for over 100 languages and identified 30 languages with suitable SER datasets.
            </p>
            <p class="text-lg text-gray-600 mb-6">
                Our methodology involves fine-tuning state-of-the-art speech models by adding a classification head on top while freezing the base model. 
                We evaluated each language individually (not multilingual) using the following models:
            </p>
            <div class="bg-gray-100 p-4 rounded-lg mb-6">
                <ul class="list-disc pl-6 text-gray-700 space-y-1">
"""

# Add models dynamically from the data
with open('benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

all_models = set()
for lang, datasets in benchmark_data.items():
    for dataset, benchmarks in datasets.items():
        for entry in benchmarks:
            all_models.add(entry["model"])

for model in sorted(all_models):
    index_html += f"                    <li>{html.escape(model)}</li>\n"

index_html += """                </ul>
            </div>
            <p class="text-lg text-gray-600 mb-8">
                Our research provides insights into the performance of these models across different languages and datasets,
                helping researchers and practitioners select the most appropriate models for their specific language needs.
            </p>
            
            <div class="flex justify-center mt-10">
                <div class="w-full max-w-3xl">
                    <h3 class="text-2xl font-bold text-gray-800 mb-4 text-center">Languages by Family</h3>
                    <canvas id="languageFamiliesChart" class="w-full h-64"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Features Section -->
    <div class="bg-gray-100 py-12">
        <div class="container mx-auto px-6">
            <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Key Features</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <div class="text-3xl text-indigo-600 mb-4"><i class="fas fa-chart-bar"></i></div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Comprehensive Benchmarks</h3>
                    <p class="text-gray-600">Compare the performance of 11 state-of-the-art speech models across 30 languages.</p>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <div class="text-3xl text-indigo-600 mb-4"><i class="fas fa-database"></i></div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Dataset Repository</h3>
                    <p class="text-gray-600">Access detailed information about SER datasets for each supported language.</p>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <div class="text-3xl text-indigo-600 mb-4"><i class="fas fa-globe"></i></div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Language Diversity</h3>
                    <p class="text-gray-600">Explore emotion recognition across diverse language families from around the world.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-8">
        <div class="container mx-auto px-6">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="mb-6 md:mb-0">
                    <h2 class="text-2xl font-bold">KuralHub</h2>
                    <p class="text-gray-400">Speech Emotion Recognition Research</p>
                </div>
                <div class="flex space-x-6">
                    <a href="#" class="text-gray-400 hover:text-white"><i class="fab fa-github text-xl"></i></a>
                    <a href="#" class="text-gray-400 hover:text-white"><i class="fab fa-twitter text-xl"></i></a>
                    <a href="#" class="text-gray-400 hover:text-white"><i class="fab fa-linkedin text-xl"></i></a>
                </div>
            </div>
            <hr class="border-gray-700 my-6">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <p class="text-gray-400">© 2025 KuralHub. All rights reserved.</p>
                <div class="mt-4 md:mt-0">
                    <p class="text-gray-400">Developed by the KuralHub Team</p>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Count languages by family for the chart
        const languageFamilies = """

# Generate language family counts for the chart
family_counts = {}
for lang, info in language_to_family.items():
    family = info["family"]
    if family not in family_counts:
        family_counts[family] = 0
    family_counts[family] += 1

index_html += json.dumps(family_counts)

index_html += """;
        
        // Create language families chart
        document.addEventListener('DOMContentLoaded', function() {
            const ctx = document.getElementById('languageFamiliesChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(languageFamilies),
                    datasets: [{
                        data: Object.values(languageFamilies),
                        backgroundColor: [
                            '#4F46E5', '#7C3AED', '#EC4899', '#F59E0B', '#10B981',
                            '#3B82F6', '#8B5CF6', '#EC4899', '#F97316', '#14B8A6',
                            '#6366F1', '#A855F7', '#D946EF', '#F59E0B', '#06B6D4'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        },
                        title: {
                            display: true,
                            text: 'Languages by Family'
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

with open('website/index.html', 'w') as f:
    f.write(index_html)
print("Created index.html (home page)")

# Let's also create the core JavaScript file that will load benchmark data dynamically
benchmark_loader_js = """// Function to load benchmark data
async function loadBenchmarkData() {
    try {
        const response = await fetch('benchmark.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading benchmark data:', error);
        return null;
    }
}

// Function to load language family mapping
async function loadLanguageFamilies() {
    try {
        const response = await fetch('language_families.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading language families:', error);
        return null;
    }
}
"""

with open('website/scripts.js', 'w') as f:
    f.write(benchmark_loader_js)
print("Created scripts.js for dynamic data loading")

# Create a copy of the benchmark and language families JSON in the website directory
with open('website/benchmark.json', 'w') as f:
    json.dump(benchmark_data, f, indent=2)

with open('website/language_families.json', 'w') as f:
    json.dump(language_to_family, f, indent=2)
print("Copied benchmark.json and language_families.json to website directory")

print("Basic website structure created. Home page (index.html) ready.")