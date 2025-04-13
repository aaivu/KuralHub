# KuralHub - Speech Emotion Recognition Benchmark Website

## Overview

This website showcases the results of comprehensive Speech Emotion Recognition (SER) research across 30 languages. It provides:

1. An overview of the project
2. Detailed benchmark results organized by language families
3. Information about SER datasets for each language

## Website Structure

- **Home Page (index.html)**: Project overview with interactive language family chart
- **Benchmark Page (benchmark.html)**: Detailed benchmark results with filtering options
- **Datasets Page (datasets.html)**: Information about SER datasets with dynamic Markdown loading

## Files and Directories

- **website/**: Main website directory
  - **index.html, benchmark.html, datasets.html**: Main HTML pages
  - **scripts.js**: JavaScript for dynamic data loading
  - **benchmark.json**: Benchmark results data
  - **language_families.json**: Language family mappings
  - **datasets/**: Directory containing Markdown files for each language
    - **<lang_code>/**: Subdirectories for each language (e.g., en, fr, de)
      - **README.md**: Overview of datasets for the language
      - **<dataset_name>.md**: Details about specific datasets

## How to Use

1. Run the server script:
   ```
   python start_server.py
   ```

2. Open a web browser and navigate to:
   ```
   http://localhost:8000
   ```

## How to Update

### Adding New Languages or Datasets

1. Update the `benchmark.json` file with new language/dataset benchmarks
2. Update the `language_families.json` file if adding a new language family
3. Create appropriate Markdown files in the datasets directory

### Customizing the Website

- Edit the HTML files directly to change layout or styling
- Modify `scripts.js` to change dynamic loading behavior

## Project Information

This project (KuralHub) provides a comprehensive review of Speech Emotion Recognition datasets across multiple languages and benchmarks their performance using various pre-trained models. The website makes this information accessible and easy to navigate.

## Team

KuralHub Research Team
