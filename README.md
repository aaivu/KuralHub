<div align="center">

# 🎙️ KuralHub: A Comprehensive Review of Speech Emotion Recognition (SER) Datasets  

[![Latest Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/aaivu/KuralHub)  [![ACL Paper](https://img.shields.io/badge/ACL-Paper-orange)](https://arxiv.org/abs/xxxx.xxxxx)  [![License](https://img.shields.io/github/license/aaivu/KuralHub)](LICENSE)  [![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)](CONTRIBUTING.md)  

</div>


---

## 🔥 **What is KuralHub?**
**KuralHub** is a **comprehensive repository** that reviews and benchmarks **Speech Emotion Recognition (SER) datasets** across multiple languages.  
It provides **detailed metadata, access links, and benchmarks** using **fine-tuned monolingual models** for SER.

**📄 Read the paper:** TBD

---

## 🗂 **Repository Structure**
```
KuralHub/
│── datasets/             # Language-specific datasets
│   ├── english/
│   │   ├── README.md     # Overview of English SER datasets
│   │   ├── ravdess.md    # Dataset-specific details
│   ├── spanish/
│   │   ├── README.md
│   │   ├── dataset1.md
│── scripts/              # Data loaders
│── LICENSE               # License information
│── README.md             # Main repo documentation
│── CONTRIBUTING.md       # Contribution guidelines
│── CODE_OF_CONDUCT.md    # Code of conduct
│── requirements.txt      # Dependencies for processing scripts
```

---

## 📊 **SER Datasets Coverage**
This repository contains details for **58+ languages**, including **open-source and restricted** datasets.  
If a language has **no available dataset**, it is marked accordingly.

| Language | # Datasets | Open Access | Restricted | Not Available |
|----------|-----------|-------------|------------|--------------|
| English  | 10        | ✅ Yes      | 🔒 Yes     | ❌ No        |
| Spanish  | 5         | ✅ Yes      | 🔒 Yes     | ❌ No        |
| Tamil    | 2         | ✅ Yes      | ❌ No      | ❌ No        |
| [More...](datasets/README.md) | - | - | - | - |

---

## 🚀 **Benchmarks**
We fine-tune **pre-trained SER models** on monolingual datasets and report their **performance**.

| Model  | Language | Accuracy | F1-Score |
|--------|----------|----------|----------|
| Wav2Vec 2.0 | English | 85.2% | 0.88 |
| HuBERT | Spanish | 83.1% | 0.85 |
| [More...](benchmarks/) | - | - | - |

---

## 📥 **How to Use**
1. **Browse Datasets:** Navigate to `datasets/` for language-specific SER datasets.
2. **Download Datasets:** Follow access links in each dataset file.
3. **Run Benchmarks:** Check `benchmarks/` for model performance.

---

## 🎯 **Contribute to KuralHub**
💡 **Know of a missing dataset?** Help us expand KuralHub!  
📩 **Submit a pull request** or open an issue with new datasets.  

📖 **[Contribution Guidelines](CONTRIBUTING.md)**  

---

## 📜 Citation

If you are using this model or research findings, please cite the following paper:

```bibtex
@article{placeholder2024,
  author    = {Author(s)},
  title     = {Paper Title},
  journal   = {Conference/Journal},
  year      = {2024},
  volume    = {X},
  number    = {Y},
  pages     = {ZZ-ZZ},
  doi       = {10.XXXX/placeholder},
}
```

## 📬 Contact

<div style="width: 100%; overflow-x: auto;">
    <table style="width: 100%; text-align: left; border-collapse: collapse; margin-top: 20px;">
        <thead>
            <tr>
                <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4;">🏷️ <strong>Name</strong></th>
                <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4;">📧 <strong>Email</strong></th>
                <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4;">🔗 <strong>LinkedIn</strong></th>
                <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4;">📚 <strong>Google Scholar</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Luxshan Thavarasa</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:luxshan.20@cse.mrt.ac.lk">luxshan.20@cse.mrt.ac.lk</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://linkedin.com/in/lux-thavarasa">LinkedIn</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://scholar.google.com/citations?user=your-profile-link">Google Scholar</a></td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Jubeerathan Thevakumar</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:jubeerathan.20@cse.mrt.ac.lk">jubeerathan.20@cse.mrt.ac.lk</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://lk.linkedin.com/in/jubeerathan-thevakumar-87b9b8255">LinkedIn</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://scholar.google.com/citations?user=your-profile-link">Google Scholar</a></td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Thanikan Sivatheepan</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:thanikan.20@cse.mrt.ac.lk">thanikan.20@cse.mrt.ac.lk</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://lk.linkedin.com/in/sthanikan2000">LinkedIn</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://scholar.google.com/citations?user=your-profile-link">Google Scholar</a></td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Uthayasanker Thayasivam</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="mailto:rtuthaya@cse.mrt.ac.lk">rtuthaya@cse.mrt.ac.lk</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://lk.linkedin.com/in/rtuthaya">LinkedIn</a></td>
                <td style="padding: 10px; border: 1px solid #ddd;"><a href="https://scholar.google.com/citations?user=your-profile-link">Google Scholar</a></td>
            </tr>
        </tbody>
    </table>
</div>

## 🙏 Acknowledgment

I would like to thank Dr. Uthayasanker Thayasivam for his guidance as my supervisor, Braveenan Sritharan for his mentorship, and all the dataset owners for making their datasets available for us through open access or upon request. Your support has been invaluable.
