const datasets = {
  "Japanese": ["Keio-ESD", "OGVC"],
  "German": ["EMO-DB"],
  "Mandarin Chinese": ["EMOVIE", "M3ED", "CASIA"],
  "Portuguese": ["emoUERJ"],
  "French": ["CaFE"],
  "Indonesian": ["IndoWaveSentiment"],
  "Spanish": ["MESD", "ESCorpus-PE"],
  "Bengali": ["SUBESCO"],
  "Hindi": ["NoName"],
  "English": ["IEMOCAP", "RAVDESS", "CREMA-D"],
  "Italian": ["Emozionalmente", "EMOVO"],
  "Arabic": ["BAVED", "MDER"],
  "Urdu": ["URDU-Dataset"],
  "Russian": ["Dusha"],
  "Korean": ["KESDy18"]
};

// Render datasets dynamically
const datasetList = document.getElementById("dataset-list");
Object.keys(datasets).forEach(language => {
  const expander = document.createElement("details");
  expander.className = "bg-white shadow p-4 rounded-lg";

  const summary = document.createElement("summary");
  summary.className = "cursor-pointer text-lg font-medium";
  summary.textContent = language;

  const list = document.createElement("ul");
  list.className = "ml-4 mt-2";
  datasets[language].forEach(dataset => {
    const listItem = document.createElement("li");
    listItem.innerHTML = `<a href="./datasets/${language}/${dataset}/${dataset}.md" target="_blank" class="text-primary hover:underline">${dataset}</a>`;
    list.appendChild(listItem);
  });

  expander.appendChild(summary);
  expander.appendChild(list);
  datasetList.appendChild(expander);
});
