# filename: create_benchmark_page.py
# execution: true
import json
import html

# Load benchmark data
with open('benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

# Load language families
with open('language_families.json', 'r') as f:
    language_to_family = json.load(f)

# Create benchmark.html
benchmark_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benchmark Results - KuralHub</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        .model-cell:hover {
            background-color: rgba(79, 70, 229, 0.1);
        }
        .accuracy-high {
            background-color: rgba(16, 185, 129, 0.2);
        }
        .accuracy-medium {
            background-color: rgba(245, 158, 11, 0.2);
        }
        .accuracy-low {
            background-color: rgba(239, 68, 68, 0.2);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-indigo-600 text-white shadow-lg">
        <div class="container mx-auto px-6 py-3 flex justify-between items-center">
            <a href="index.html" class="text-2xl font-bold">KuralHub</a>
            <div class="space-x-4">
                <a href="index.html" class="hover:text-indigo-200">Home</a>
                <a href="benchmark.html" class="hover:text-indigo-200 font-semibold">Benchmark</a>
                <a href="datasets.html" class="hover:text-indigo-200">Datasets</a>
            </div>
        </div>
    </nav>

    <!-- Header Section -->
    <div class="bg-indigo-700 text-white py-10">
        <div class="container mx-auto px-6">
            <h1 class="text-3xl font-bold mb-2">Benchmark Results</h1>
            <p class="text-lg">Comprehensive evaluation of Speech Emotion Recognition models across different languages</p>
        </div>
    </div>

    <!-- Controls Section -->
    <div class="container mx-auto px-6 py-6">
        <div class="bg-white p-4 rounded-lg shadow-md mb-6">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="mb-4 md:mb-0">
                    <h2 class="text-xl font-bold text-gray-800">Filter Options</h2>
                </div>
                <div class="flex flex-wrap gap-2">
                    <select id="familyFilter" class="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="all">All Language Families</option>
                        <!-- Language families will be populated via JavaScript -->
                    </select>
                    <select id="modelFilter" class="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="all">All Models</option>
                        <!-- Models will be populated via JavaScript -->
                    </select>
                    <button id="resetFilters" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500">
                        Reset Filters
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Benchmark Results Section -->
    <div class="container mx-auto px-6 pb-12">
        <div id="benchmarkResults">
            <div class="text-center py-10">
                <i class="fas fa-spinner fa-spin text-3xl text-indigo-600"></i>
                <p class="mt-2 text-gray-600">Loading benchmark results...</p>
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

    <script src="scripts.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', async function() {
            // Load benchmark data
            const benchmarkData = await loadBenchmarkData();
            const languageFamilies = await loadLanguageFamilies();
            
            if (!benchmarkData || !languageFamilies) {
                document.getElementById('benchmarkResults').innerHTML = 
                    '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">' +
                    '<strong class="font-bold">Error!</strong>' +
                    '<span class="block sm:inline"> Failed to load benchmark data.</span>' +
                    '</div>';
                return;
            }
            
            // Get all models
            const allModels = new Set();
            for (const lang in benchmarkData) {
                for (const dataset in benchmarkData[lang]) {
                    for (const benchmark of benchmarkData[lang][dataset]) {
                        allModels.add(benchmark.model);
                    }
                }
            }
            
            // Get all language families
            const allFamilies = new Set();
            for (const lang in languageFamilies) {
                allFamilies.add(languageFamilies[lang].family);
            }
            
            // Populate filter dropdowns
            const familyFilter = document.getElementById('familyFilter');
            Array.from(allFamilies).sort().forEach(family => {
                const option = document.createElement('option');
                option.value = family;
                option.textContent = family;
                familyFilter.appendChild(option);
            });
            
            const modelFilter = document.getElementById('modelFilter');
            Array.from(allModels).sort().forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelFilter.appendChild(option);
            });
            
            // Group languages by family and subfamily
            const languagesByFamily = {};
            for (const lang in languageFamilies) {
                const family = languageFamilies[lang].family;
                const subfamily = languageFamilies[lang].subfamily;
                
                if (!languagesByFamily[family]) {
                    languagesByFamily[family] = {};
                }
                
                if (subfamily) {
                    if (!languagesByFamily[family][subfamily]) {
                        languagesByFamily[family][subfamily] = [];
                    }
                    languagesByFamily[family][subfamily].push(lang);
                } else {
                    if (!languagesByFamily[family]['_none']) {
                        languagesByFamily[family]['_none'] = [];
                    }
                    languagesByFamily[family]['_none'].push(lang);
                }
            }
            
            // Function to render benchmark results
            function renderBenchmarkResults(familyFilter = 'all', modelFilter = 'all') {
                let html = '';
                
                // Sort families alphabetically
                const sortedFamilies = Object.keys(languagesByFamily).sort();
                
                for (const family of sortedFamilies) {
                    if (familyFilter !== 'all' && familyFilter !== family) continue;
                    
                    html += `
                        <div class="mb-10">
                            <h2 class="text-2xl font-bold text-gray-800 mb-4">${family} Family</h2>
                    `;
                    
                    // Sort subfamilies alphabetically
                    const sortedSubfamilies = Object.keys(languagesByFamily[family]).sort();
                    
                    for (const subfamily of sortedSubfamilies) {
                        if (subfamily !== '_none') {
                            html += `<h3 class="text-xl font-semibold text-gray-700 mb-3 mt-6">${subfamily} Subfamily</h3>`;
                        }
                        
                        const languages = languagesByFamily[family][subfamily];
                        
                        for (const lang of languages.sort()) {
                            if (!benchmarkData[lang]) continue;
                            
                            html += `
                                <div class="bg-white rounded-lg shadow-md p-4 mb-6">
                                    <h4 class="text-lg font-semibold text-gray-800 mb-3">${lang}</h4>
                            `;
                            
                            for (const dataset in benchmarkData[lang]) {
                                html += `
                                    <div class="mb-4">
                                        <h5 class="text-md font-medium text-gray-700 mb-2">${dataset}</h5>
                                        <div class="overflow-x-auto">
                                            <table class="min-w-full bg-white border border-gray-200">
                                                <thead>
                                                    <tr>
                                                        <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Model</th>
                                                        <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Validation Accuracy</th>
                                                        <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test Accuracy</th>
                                                        <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Status</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                `;
                                
                                const benchmarks = benchmarkData[lang][dataset];
                                
                                for (const benchmark of benchmarks) {
                                    if (modelFilter !== 'all' && modelFilter !== benchmark.model) continue;
                                    
                                    const valAccClass = getAccuracyClass(benchmark.val_accuracy);
                                    const testAccClass = getAccuracyClass(benchmark.test_accuracy);
                                    
                                    html += `
                                        <tr class="model-cell">
                                            <td class="py-2 px-4 border-b border-gray-200">${benchmark.model}</td>
                                            <td class="py-2 px-4 border-b border-gray-200 ${valAccClass}">${(benchmark.val_accuracy * 100).toFixed(1)}%</td>
                                            <td class="py-2 px-4 border-b border-gray-200 ${testAccClass}">${(benchmark.test_accuracy * 100).toFixed(1)}%</td>
                                            <td class="py-2 px-4 border-b border-gray-200">${benchmark.completed}</td>
                                        </tr>
                                    `;
                                }
                                
                                html += `
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                `;
                            }
                            
                            html += `</div>`;
                        }
                    }
                    
                    html += `</div>`;
                }
                
                return html;
            }
            
            // Helper function to get CSS class based on accuracy value
            function getAccuracyClass(accuracy) {
                if (accuracy >= 0.7) return 'accuracy-high';
                if (accuracy >= 0.5) return 'accuracy-medium';
                return 'accuracy-low';
            }
            
            // Initial render
            document.getElementById('benchmarkResults').innerHTML = renderBenchmarkResults();
            
            // Add event listeners for filters
            document.getElementById('familyFilter').addEventListener('change', function() {
                const familyValue = this.value;
                const modelValue = document.getElementById('modelFilter').value;
                document.getElementById('benchmarkResults').innerHTML = renderBenchmarkResults(familyValue, modelValue);
            });
            
            document.getElementById('modelFilter').addEventListener('change', function() {
                const familyValue = document.getElementById('familyFilter').value;
                const modelValue = this.value;
                document.getElementById('benchmarkResults').innerHTML = renderBenchmarkResults(familyValue, modelValue);
            });
            
            document.getElementById('resetFilters').addEventListener('click', function() {
                document.getElementById('familyFilter').value = 'all';
                document.getElementById('modelFilter').value = 'all';
                document.getElementById('benchmarkResults').innerHTML = renderBenchmarkResults();
            });
        });
    </script>
</body>
</html>
"""

with open('website/benchmark.html', 'w') as f:
    f.write(benchmark_html)
print("Created benchmark.html page")

# Now create the datasets.html page
datasets_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datasets - KuralHub</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-indigo-600 text-white shadow-lg">
        <div class="container mx-auto px-6 py-3 flex justify-between items-center">
            <a href="index.html" class="text-2xl font-bold">KuralHub</a>
            <div class="space-x-4">
                <a href="index.html" class="hover:text-indigo-200">Home</a>
                <a href="benchmark.html" class="hover:text-indigo-200">Benchmark</a>
                <a href="datasets.html" class="hover:text-indigo-200 font-semibold">Datasets</a>
            </div>
        </div>
    </nav>

    <!-- Header Section -->
    <div class="bg-indigo-700 text-white py-10">
        <div class="container mx-auto px-6">
            <h1 class="text-3xl font-bold mb-2">SER Datasets</h1>
            <p class="text-lg">Comprehensive collection of Speech Emotion Recognition datasets across different languages</p>
        </div>
    </div>

    <!-- Language Selection Section -->
    <div class="container mx-auto px-6 py-6">
        <div class="bg-white p-4 rounded-lg shadow-md mb-6">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="mb-4 md:mb-0">
                    <h2 class="text-xl font-bold text-gray-800">Select Language</h2>
                </div>
                <div class="flex flex-wrap gap-2">
                    <select id="languageSelector" class="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="">Choose a language</option>
                        <!-- Languages will be populated via JavaScript -->
                    </select>
                </div>
            </div>
        </div>
    </div>

    <!-- Dataset Content Section -->
    <div class="container mx-auto px-6 pb-12">
        <div id="datasetContent" class="bg-white rounded-lg shadow-md p-6">
            <div class="text-center py-10">
                <p class="text-gray-600">Select a language to view its dataset information</p>
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

    <script src="scripts.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', async function() {
            // Load benchmark data to get languages
            const benchmarkData = await loadBenchmarkData();
            const languageFamilies = await loadLanguageFamilies();
            
            if (!benchmarkData || !languageFamilies) {
                document.getElementById('datasetContent').innerHTML = 
                    '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">' +
                    '<strong class="font-bold">Error!</strong>' +
                    '<span class="block sm:inline"> Failed to load data.</span>' +
                    '</div>';
                return;
            }
            
            // Populate language selector
            const languageSelector = document.getElementById('languageSelector');
            Object.keys(benchmarkData).sort().forEach(lang => {
                const option = document.createElement('option');
                option.value = lang;
                option.textContent = lang;
                languageSelector.appendChild(option);
            });
            
            // Function to load markdown content
            async function loadMarkdownContent(language) {
                try {
                    // Extract language code from the language string, e.g., "English (en)" -> "en"
                    const langCode = language.match(/\\((\\w+)\\)/)[1].toLowerCase();
                    
                    // For demonstration, we're creating placeholder content
                    // In a real scenario, you would fetch the actual Markdown files
                    const readmePath = `datasets/${langCode}/README.md`;
                    
                    // Simulate loading README.md
                    // In production, you would replace this with an actual fetch of the file
                    const readmeContent = `# ${language} SER Datasets Overview
                    
This page provides an overview of Speech Emotion Recognition datasets available for ${language}.

## Available Datasets

${Object.keys(benchmarkData[language]).map(dataset => `
### ${dataset}

This dataset contains speech samples with emotional content in ${language}.
For detailed information, see the [dataset details](${langCode}/${dataset.toLowerCase().replace(/[^a-z0-9]/gi, '_')}.html).
`).join('')}

## Benchmark Results

The table below shows the best performing models for ${language} SER:

| Dataset | Best Model | Test Accuracy |
|---------|------------|---------------|
${Object.keys(benchmarkData[language]).map(dataset => {
    const benchmarks = benchmarkData[language][dataset];
    let bestModel = benchmarks[0];
    for (const benchmark of benchmarks) {
        if (benchmark.test_accuracy > bestModel.test_accuracy) {
            bestModel = benchmark;
        }
    }
    return `| ${dataset} | ${bestModel.model} | ${(bestModel.test_accuracy * 100).toFixed(1)}% |`;
}).join('\\n')}
`;
                    
                    return readmeContent;
                } catch (error) {
                    console.error('Error loading markdown content:', error);
                    return `# Error Loading Content
                    
Unable to load dataset information for ${language}.

Please try again later or contact the KuralHub team for assistance.`;
                }
            }
            
            // Add event listener for language selector
            languageSelector.addEventListener('change', async function() {
                const selectedLanguage = this.value;
                if (!selectedLanguage) {
                    document.getElementById('datasetContent').innerHTML = 
                        '<div class="text-center py-10"><p class="text-gray-600">Select a language to view its dataset information</p></div>';
                    return;
                }
                
                document.getElementById('datasetContent').innerHTML = 
                    '<div class="text-center py-10"><i class="fas fa-spinner fa-spin text-3xl text-indigo-600"></i><p class="mt-2 text-gray-600">Loading dataset information...</p></div>';
                
                const markdownContent = await loadMarkdownContent(selectedLanguage);
                document.getElementById('datasetContent').innerHTML = `
                    <div class="prose max-w-none">
                        ${marked.parse(markdownContent)}
                    </div>
                `;
            });
        });
    </script>
</body>
</html>
"""

with open('website/datasets.html', 'w') as f:
    f.write(datasets_html)
print("Created datasets.html page")

# Create a simple README file for the website
readme = """# KuralHub - Speech Emotion Recognition Benchmark

This website showcases the results of a comprehensive research initiative focused on Speech Emotion Recognition (SER) across 30 languages.

## Pages

- **Home Page (index.html)**: Overview of the project
- **Benchmark Page (benchmark.html)**: Detailed benchmark results organized by language families
- **Datasets Page (datasets.html)**: Information about SER datasets for each language

## Data Files

- **benchmark.json**: Contains all benchmark results
- **language_families.json**: Maps languages to their respective language families

## Usage

Simply open index.html in a web browser to navigate the site.

## Future Work

In a production environment, the datasets directory would contain Markdown files with detailed information about each dataset.
"""

with open('website/README.md', 'w') as f:
    f.write(readme)
print("Created README.md for the website")

# Create a simple placeholder structure for the datasets directory
import os
os.makedirs('website/datasets', exist_ok=True)
print("Created placeholder datasets directory")

print("All website files have been created successfully.")