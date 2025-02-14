<div align="center">

# 🎙️ KuralHub: A Comprehensive Review of Speech Emotion Recognition (SER) Datasets  

[![Latest Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/aaivu/KuralNet)  [![ACL Paper](https://img.shields.io/badge/ACL-Paper-orange)](https://arxiv.org/abs/xxxx.xxxxx)  [![License](https://img.shields.io/github/license/aaivu/KuralNet)](LICENSE)  [![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)](CONTRIBUTING.md)  

</div>


---

## 🔥 **What is KuralHub?**
**KuralNet** is a **comprehensive repository** that reviews and benchmarks **Speech Emotion Recognition (SER) datasets** across multiple languages.  
It provides **detailed metadata, access links, and benchmarks** using **fine-tuned monolingual models** for SER.

**📄 Read the paper:** TBD

---

## 🗂 **Repository Structure**
```
KuralNet/
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

## 🎯 **Contribute to KuralNet**
💡 **Know of a missing dataset?** Help us expand KuralNet!  
📩 **Submit a pull request** or open an issue with new datasets.  

📖 **[Contribution Guidelines](CONTRIBUTING.md)**  

---

## 📜 **Citing KuralNet**
If you use KuralNet, **cite our work**:

```
TBD
```

---

## 📜 **License**
📝 KuralNet is released under the **MIT License**.  
📄 See **[LICENSE](LICENSE)** for details.
