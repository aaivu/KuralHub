# KuralHub: Exposing Typological Capability Frontiers in Multilingual Speech Emotion Recognition

Luxshan Thavarasa\*, Jubeerathan Thevakumar\*, Thanikan Sivatheepan, Uthayasanker Thayasivam
Department of Computer Science and Engineering, University of Moratuwa, Colombo, Sri Lanka
\*Equal contribution

Interspeech 2026, Sydney, Australia, pages 4673-4678. DOI: [10.21437/Interspeech.2026-3502](https://doi.org/10.21437/Interspeech.2026-3502).
PDF: https://www.isca-archive.org/interspeech_2026/thavarasa26_interspeech.pdf
Website: https://aaivu.github.io/KuralHub/ · Code and data: https://github.com/aaivu/KuralHub

In numbers: 70 languages surveyed, 90 datasets documented, 29 languages and 33 datasets benchmarked, 11 models, 363 training runs.

## Abstract

Speech Emotion Recognition (SER) advancements are constrained by high-resource bias, limiting global access. To address this, we introduce KuralHub, an open-science initiative democratizing SER for under-resourced languages. We evaluate 11 self-supervised models (WavLM, HuBERT, Wav2vec 2.0, Whisper) across 33 datasets in 29 diverse languages. Beyond standard benchmarking, our study reveals a critical typological bias: cross-lingual transferability is dictated more by structural linguistic properties than pre-training data volume. While models easily adapt to Mandarin or Amharic, they systematically fail on the Dravidian family. Crucially, we demonstrate that simply scaling model parameters fails to resolve this bottleneck. By exposing these linguistic capability frontiers, KuralHub provides a vital roadmap for developing equitable, typologically-aware speech technologies for all speakers.

Index terms: speech emotion recognition, under-resourced languages, benchmarking

## Key findings

1. **No model is best everywhere.** Whisper had the highest mean F1 (0.70 for both whisper-small and whisper-large), followed by HuBERT-base (0.68) and WavLM (0.64 large, 0.63 base-plus). Even so, HuBERT came out on top for nine languages and WavLM for English and Swahili (Table 2).
2. **Dravidian languages fail across the board.** Kannada averaged 0.275 test accuracy and Tamil 0.306 (best single run 0.44). Telugu never got above 0.53. The spread between models is small, so they fail in the same way.
3. **More pre-training data does not guarantee better results.** Mandarin (0.755) and Indonesian (0.720) were easy. French (0.421), Spanish (0.365) and Russian (0.344) were not, and Persian, Arabic, Odia, Amharic and Quechua all beat several European languages.
4. **Bigger models are not better.** The log of parameter count is negatively correlated with F1 (r = −0.18, p = 0.0007). wav2vec2-base (0.58) beat both wav2vec2-large-960h (0.30) and wav2vec2-large-lv60 (0.25).
5. **Fear is the hardest emotion.** Its mean F1 was 0.38, against 0.54 for anger and 0.52 for neutral. The order holds across languages.

## 1 Introduction

Speech emotion recognition (SER) means working out from a voice alone whether the speaker sounds angry, happy, sad, afraid or neutral. Voice assistants, call-centre analytics and health monitoring all depend on it. Most SER research, though, covers a handful of high-resource languages, and the world has more than 7,000.

Emotional speech datasets for other languages are scattered across papers, Kaggle pages and lab websites, and each is described differently, so just finding them is slow. It is also unclear how well self-supervised speech models such as HuBERT, wav2vec 2.0, WavLM and Whisper carry over to emotion recognition in languages they saw little of during pre-training.

KuralHub (*kural*, குரல், is Tamil for "voice") addresses both problems. We looked for emotional speech datasets in the 70 most widely spoken languages and documented every one we found in the same format. We then trained emotion classifiers on top of 11 frozen pretrained models for 33 of those datasets, covering 29 languages, with a single recipe, and studied where they work and where they break.

## 2 The dataset survey

We took the 70 most widely spoken languages listed in Ethnologue and searched academic repositories and public sources for emotional speech corpora in each. 45 of the 70 have at least one dataset. For the remaining 25 we found none. The catalog documents 90 datasets in total.

The repository is organised by language. Each language has a folder (`datasets/<Language>/`) whose `Readme.md` gives the language family, ISO code, where it is spoken and a table of its datasets. Every dataset then gets its own Markdown file with the emotion labels, size, speakers, recording setup (acted, elicited or spontaneous), licence, how to get it, the original paper and a BibTeX entry. The website builds one page per language from those files: https://aaivu.github.io/KuralHub/datasets.html

### Which datasets were benchmarked

A dataset was included in the benchmark if it (i) had clearly annotated emotion labels, (ii) covered at least three of five target emotions (anger, happiness, sadness, neutral and fear), and (iii) had at least 50 utterances per emotion. 33 datasets in 29 languages qualified. They differ in recording conditions, in how emotion was elicited (acted or spontaneous), in speaker demographics and in their emotion labels, which makes them a fair test of how well a model generalises.

**Table 1.** The datasets used in the benchmark, part of the full survey (from the paper). \* marks high-resource languages. #Emo: emotions. #Samples: samples.

| Language | Dataset | #Emo | #Samples |
|---|---|---|---|
| Afrikaans | AfrikaansSE | 8 | 800 |
| Amharic | ASED | 5 | 2,474 |
| Arabic | ANAD | 3 | 1,384 |
| Bengali | BANSpEmo | 6 | 792 |
| Bengali | SUBESCO | 7 | 7,000 |
| Chinese\* | ESD | 5 | 17,500 |
| English\* | IESC | 5 | 600 |
| English\* | RAVDESS | 7 | 1,440 |
| French\* | CaFE | 7 | 936 |
| German\* | EmoDB | 7 | 535 |
| Greek | AESDD | 5 | 500 |
| Hindi\* | IITKGP-SEHSC | 8 | 12,000 |
| Hungarian | HESD | 8 | 760 |
| Indonesian | IndoWaveSentiment | 5 | 300 |
| Italian\* | EMOVO | 7 | 564 |
| Italian\* | Emozionalmente | 7 | 6,902 |
| Japanese\* | JVNV | 6 | 1,615 |
| Kannada | Agrawal et al. | 6 | 468 |
| Kazakh | KazEmoTTS | 6 | 54,760 |
| Korean\* | KESDy18 | 7 | 2,880 |
| Odia | SITB-OSED | 6 | 12,110 |
| Persian | ShEMO | 6 | 3,000 |
| Polish | nEMO | 6 | 4,481 |
| Portuguese\* | emoUERJ | 4 | 377 |
| Quechua | Quechua Collao | 9 | 12,420 |
| Russian\* | Dusha | 4 | 300,000 |
| Spanish\* | MESD | 6 | 432 |
| Swahili | Kenyan Swahili SER | 5 | 300 |
| Tamil | EmoTa | 5 | 936 |
| Telugu | Sowmith et al. | 5 | 468 |
| Turkish | TurEV-DB | 4 | 1,735 |
| Urdu | URDU-Dataset | 4 | 400 |
| Urdu | UrduSER | 7 | 3,500 |

## 3 Benchmark setup

### Models

11 pretrained speech encoders from four families: HuBERT (hubert-base-ls960, hubert-large-ls960-ft), wav2vec 2.0 (wav2vec2-base, wav2vec2-large-960h, wav2vec2-large-lv60, wav2vec2-xls-r-300m, wav2vec2-xls-r-1b), WavLM (wavlm-base-plus, wavlm-large) and Whisper (whisper-small, whisper-large). All are the public Hugging Face checkpoints under facebook/, microsoft/ and openai/.

### Training and evaluation

Every backbone stays frozen. Only a small classification head on top is trained, which keeps the comparison cheap and fair and needs far less labelled data than full fine-tuning.

1. Audio is resampled to 16 kHz, normalised with librosa and passed through the frozen backbone.
2. The last-layer hidden states are averaged over time, giving one embedding per clip.
3. A two-layer feed-forward head maps the embedding to emotion classes: linear (to 512 units), GELU, dropout (0.3), linear.
4. The head is trained with cross-entropy loss and Adam (learning rate 1e-3, halved when validation loss stalls for 2 epochs) for up to 30 epochs, with early stopping after 5 epochs without improvement.

Each dataset is split 70% / 15% / 15% into training, validation and test sets. Runs use whichever of the five target emotions a dataset contains. We report precision, recall, F1 and accuracy on the held-out test set, per emotion and as macro and weighted averages. The hidden size, dropout, learning rate schedule, patience and pooling come from the released code rather than the paper.

## 4 Results

### 4.1 The language matters more than how much pre-training data it had

Mean test accuracy over all models and languages was 0.52 (σ = 0.19). A common assumption is that languages with more pre-training data will do better. The results only partly support that.

Mandarin Chinese, a high-resource language, was easy (mean 0.755, median 0.90), and so was Indonesian (0.720, median 0.77). Other high-resource languages were not. French (0.421), Spanish (0.365) and Russian (0.344) were all mediocre. Several lower-resource languages did well instead: Persian (0.67, median 0.76) and Arabic (0.66, σ = 0.08) were stable, and Odia (0.643, best 0.83), Amharic (0.636, best 0.90) and Quechua all beat several European languages.

Pre-training volume alone does not decide the outcome. Languages with stable phonetics, consistent pronunciation rules and standardised corpora seem easier for self-supervised models to learn. High dialect variation and spontaneous speech add acoustic noise that pulls performance down.

Figure 1 (radar chart): model accuracy across languages. https://aaivu.github.io/KuralHub/assets/fig/fig1-model-accuracy-by-language.png

### 4.2 Systematic failure on Dravidian languages

The clearest pattern is that every model does badly on the Dravidian languages. Kannada (μ = 0.275, σ = 0.085, median 0.26) and Tamil (μ = 0.306, σ = 0.088, max 0.44) are among the worst languages in the benchmark, and Telugu peaks at 0.53.

The small standard deviations matter. Almost every model fails on Kannada and Tamil in much the same way, which points to a limitation in current self-supervised architectures rather than an unlucky choice of model. Dravidian languages are morphologically complex, highly agglutinative and rich in retroflex consonants. Handling that takes fine-grained temporal modelling, and the strided CNN front-ends these models use may throw away the phonetic detail needed.

Figure 2 (heatmap): mean macro-F1 of each model across language families. Dravidian and Uralic consistently score lower than the other families. https://aaivu.github.io/KuralHub/assets/fig/fig2-f1-by-language-family.png

The shape of each language's score distribution sorts languages into two groups:

- **Widely solved (negative skew).** Mandarin (skew −0.87) and Amharic (−0.39). Most models do well, so the language is easy to reach.
- **Capability frontier (positive skew).** Kannada (+1.17) and Spanish (+0.72). Median scores sit near the bottom (Kannada 0.26, Spanish 0.27), and only a few larger or specialised models do better.

**Table 2.** Best model family for each language (from the paper).

| Best model | Languages |
|---|---|
| HuBERT | French, Greek, Hindi, Hungarian, Indonesian, Japanese, Russian, Telugu, Urdu |
| WavLM | English, Swahili |
| Whisper | Afrikaans, Amharic, Arabic, Bengali, Chinese, German, Italian, Kannada, Kazakh, Korean, Odia, Persian, Polish, Portuguese, Quechua, Spanish, Tamil, Turkish |

No single model is best for every language, so model choice for multilingual SER has to depend on the language.

### 4.3 Architecture matters, size does not

Across all 33 datasets, the Whisper models had the highest mean F1 (0.70 for both whisper-small and whisper-large), followed by HuBERT-base (0.68) and WavLM (0.64 for wavlm-large, 0.63 for wavlm-base-plus). Whisper and HuBERT held up well across languages, while the wav2vec 2.0 models generalised worst.

To separate architecture from dataset and language effects we fitted a linear mixed-effects model, F1 ~ Family + (1|Dataset) + (1|Language). The reference family had a mean F1 of 0.524. Against it, wav2vec 2.0 was clearly worse (β = −0.195, p < .001) while WavLM (β = +0.091) and Whisper (β = +0.170) were better (both p < .001). About 40% of the total variance came from differences between datasets and languages.

Bigger models within a family were not reliably better. wav2vec2-base (μ = 0.58, σ = 0.17) beat wav2vec2-large-960h (μ = 0.30, σ = 0.11) and wav2vec2-large-lv60 (μ = 0.25, σ = 0.10). Across all models:

- Raw parameter count had no significant linear relationship with F1 (r = 0.035, 95% CI [−0.068, 0.138], p = 0.50).
- Log parameter count was significantly negatively correlated with F1 (r = −0.177, 95% CI [−0.275, −0.075], p = 0.0007). Spearman's ρ = −0.344 (p = 1.6 × 10⁻¹¹) agrees.
- A second mixed-effects model, F1 ~ log(ModelSize) + (1|Dataset) + (1|Language), gave β = −0.048 (SE = 0.0125, p = 0.000125). Multiplying the parameter count by e (about 2.7×) lowered F1 by roughly 4.8 points.

Dataset-level variance (0.0113) dominated language-level variance (≈ 0), largely because 25 of the 29 languages had only one dataset. Adding parameters does not, by itself, improve multilingual emotion recognition.

Figure 3 (line chart): mean macro-F1 of each model against its parameter count, grouped by architecture family. https://aaivu.github.io/KuralHub/assets/fig/fig3-f1-vs-parameters.png

### 4.4 Which emotions are hard

**Table 3.** Precision, recall and F1 per emotion, averaged across datasets (from the paper).

| Emotion | Precision | Recall | F1 |
|---|---|---|---|
| Anger | 0.57 | 0.57 | 0.54 |
| Fear | 0.47 | 0.37 | 0.38 |
| Happiness | 0.52 | 0.43 | 0.44 |
| Neutral | 0.46 | 0.65 | 0.52 |
| Sadness | 0.54 | 0.48 | 0.46 |

Neutral and anger were the easiest to recognise and fear the hardest. The same order shows up across languages, which fits cross-cultural studies of emotion perception and suggests some acoustic cues are shared.

Errors came mainly from three sources: low-resource languages with little pre-training data, spontaneous rather than acted speech, and emotional expressions that are not prototypical. For example, the acted Amharic ASED dataset scored 24% higher than spontaneous-speech datasets with similar resources.

## 5 Limitations and future work

Across 11 models and 29 languages, the structure of a language limited cross-lingual transfer in SER more than the amount of pre-training data or the number of model parameters did. Some families, Dravidian in particular, sit at a "capability frontier" where current models fail systematically.

The study has limits:

- To keep evaluation cheap and comparable we used frozen last-layer features. Paralinguistic cues that live in intermediate layers may be under-represented.
- Dataset conditions, such as acted versus spontaneous speech, account for about 40% of the variance in performance, which complicates clean comparisons between languages.
- 25 of the 29 languages are represented by a single dataset.

Better multilingual SER will need more than larger models. We hope KuralHub helps others work on typology-aware pre-training and layer-wise fine-tuning.

## 6 Using KuralHub

- Find a dataset: https://aaivu.github.io/KuralHub/datasets.html (one page per language, e.g. https://aaivu.github.io/KuralHub/languages/tamil.html)
- All runs: https://aaivu.github.io/KuralHub/benchmark.html, https://aaivu.github.io/KuralHub/data/runs.csv, https://aaivu.github.io/KuralHub/data/runs.json
- Dataset catalog as JSON: https://aaivu.github.io/KuralHub/data/datasets.json
- Per-run logs: https://github.com/aaivu/KuralHub/tree/main/results/train_val_test_logs
- Re-run an experiment: `make setup`, `make download_dataset` (needs a Kaggle API key), `make meta_extract`, `DATASET=EMOTA BASE_MODEL=WAVLM_LARGE make train_model` (names from `src/utils/constant.py`). Requires Python 3.12+.
- Add a dataset: https://github.com/aaivu/KuralHub/blob/main/CONTRIBUTING.md

## Contribute a dataset or a model

KuralHub grows with outside help. 25 of the 70 surveyed languages still have no emotional speech dataset we could find, and the benchmark so far covers 11 models.

- Suggest a dataset: https://github.com/aaivu/KuralHub/issues/new?template=add-dataset.yml
- Suggest a model for the benchmark: https://github.com/aaivu/KuralHub/issues/new?template=add-model.yml
- How to add either one yourself: https://github.com/aaivu/KuralHub/blob/main/CONTRIBUTING.md

## Citation

Thavarasa, L., Thevakumar, J., Sivatheepan, T., Thayasivam, U. (2026) KuralHub: Exposing Typological Capability Frontiers in Multilingual Speech Emotion Recognition. Proc. Interspeech 2026, 4673-4678, doi: 10.21437/Interspeech.2026-3502

```bibtex
@inproceedings{thavarasa26_interspeech,
  title     = {{KuralHub: Exposing Typological Capability Frontiers in Multilingual Speech Emotion Recognition}},
  author    = {Luxshan Thavarasa and Jubeerathan Thevakumar and Thanikan Sivatheepan and Uthayasanker Thayasivam},
  year      = {2026},
  booktitle = {{Interspeech 2026}},
  pages     = {4673--4678},
  doi       = {10.21437/Interspeech.2026-3502},
  issn      = {2958-1796},
}
```

## Authors

- Luxshan Thavarasa\* (luxshan.20@cse.mrt.ac.lk)
- Jubeerathan Thevakumar\* (jubeerathan.25@cse.mrt.ac.lk)
- Thanikan Sivatheepan (thanikan.20@cse.mrt.ac.lk)
- Uthayasanker Thayasivam, supervisor (rtuthaya@cse.mrt.ac.lk)

\*Equal contribution. Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka.
