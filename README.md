<!-- Banner -->

<h1 align="center">📜 Benchmarking LLMs for Translating Classical Chinese Poetry</h1>
<p align="center">
  <em>“The three difficulties in translation are:adequate, fluent, and elegant.” — Yan Fu (1898)</em>  
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Paper-EMNLP%202025-blue" />
  <img src="https://img.shields.io/badge/Language-English%20%26%20Chinese-red" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
  <img src="https://img.shields.io/badge/Poetry-Tang%20%7C%20Song%20%7C%20Yuan-yellow" />
</p>

---

## 🌸 Overview

This repository introduces **PoetMT**, the first benchmark for **translating Classical Chinese Poetry into English**.  
We evaluate **Large Language Models (LLMs)** on three dimensions:

- **Adequacy (信)** → Accuracy of meaning & cultural faithfulness  
- **Fluency (达)** → Smoothness of rhythm & structural alignment  
- **Elegance (雅)** → Poetic beauty & aesthetic depth  

We also propose **RAT (Retrieval-Augmented Translation)**, which integrates historical and literary knowledge to improve performance.

---

## ✨ Key Features

✅ **PoetMT Benchmark** — All poems from **Tang, Song, Yuan** dynasties  
✅ **Three-Dimensional Evaluation** — GPT-4-based metrics: *Beauty of Sound (BS)*, *Beauty of Form (BF)*, *Beauty of Meaning (BM)*  
✅ **RAT Method** — retrieval-augmented framework leveraging a **Classical Poetry Knowledge Base**  
✅ **Superior Results** — significantly closer to human evaluation than standard LLM baselines  

---

## 📂 Dataset

- **PoetMT Dataset**
  - Human expert translations  
  - Supports **sentence-level adequacy** & **discourse-level elegance** tasks  

- **Knowledge Base**
  - 30,000+ classical poems with:  
    - Dynasty & historical background  
    - Modern Chinese translations  
    - Author introductions  
    - Poetic structure & analysis  

---

## 📊 Results

| Method       | COMET ↑ | BLEURT ↑ | LLM-BM ↑ | LLM-BS ↑ | LLM-BF ↑ | LLM-Avg ↑ |
|--------------|---------|----------|----------|----------|----------|-----------|
| GPT-4        | 60.3    | 43.0     | 4.0      | 3.7      | 3.6      | 3.8       |
| ChatGPT      | 61.1    | 42.4     | 3.3      | 3.2      | 2.9      | 3.1       |
| **RAT (Ours)** | **62.7** | **43.9** | **4.1** | **3.9** | **3.9** | **4.0**   |

📌 **RAT outperforms all baselines**, especially in **Elegance (BM)**, aligning closely with human evaluation.

---

## 🔮 Future Directions

- 🌍 **Cross-cultural generation** — extend to other literary traditions  
- 🎨 **Multimodal integration** — enrich translation with images & audio context  
- 📏 **Expanded evaluation** — design broader aesthetic and cultural metrics  

---

## 📜 Citation

If you use this project, please cite our EMNLP 2025 paper:

```bibtex
@inproceedings{chen2025benchmarking,
  title={Benchmarking LLMs for Translating Classical Chinese Poetry: Evaluating Adequacy, Fluency, and Elegance},
  author={Chen, Andong and Lou, Lianzhang and Chen, Kehai and Bai, Xuefeng and Xiang, Yang and Yang, Muyun and Zhao, Tiejun and Zhang, Min},
  booktitle={Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing},
  year={2025}
}
