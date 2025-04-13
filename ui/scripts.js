// Function to load benchmark data
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
