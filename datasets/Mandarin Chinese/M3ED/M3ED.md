# M3ED (Multi-modal Multi-scene Multi-label Emotional Dialogue Database)  

## Dataset Overview

- **Name:** M3ED (RUCM3ED)  
- **Institution:** Renmin University of China  
- **Year:** 2022  
- **Authors:** Zhao, W., Zhang, Z., et al.  
- **Homepage:** [GitHub Repository](https://github.com/AIM3-RUC/RUCM3ED)  

## Dataset Content

- **Duration:** ~500 TV episodes  
- **Sessions:** 56 different TV series  
- **Speakers:** 626 unique speakers  
- **Dialogues:** 990 total dialogues  
- **Utterances:** 24,449 total utterances  
- **Language:** Chinese  

## Technical Details

- **Text Features:**
  - RoBERTa word-level features with mean pooling
  - Fine-tuned emotional features
- **Audio Features:**
  - IS10 emotional features (z-normalized)
  - wav2vec sentence-level features
  - Fine-tuned emotional features
- **Structure:**
  - 9,082 conversation turns
  - Average 9.17 turns per dialogue
  - Average 2.69 utterances per turn

## Emotional Content

- **Primary Emotions (Label ID):**  
  - Happy (0)
  - Neutral (1)
  - Sad (2)
  - Disgust (3)
  - Anger (4)
  - Fear (5)
  - Surprise (6)

- **Emotional Patterns:**
  - Inter-turn emotion shifts: 5,396
  - Inter-turn emotion inertia: 2,696
  - Intra-turn emotion shifts: 2,879
  - Intra-turn emotion inertia: 10,891
  - Blended emotions: 11% of utterances

## Data Distribution

- **Training Set:**
  - 685 dialogues
  - 17,427 utterances
  - 38 TV series
- **Validation Set:**
  - 126 dialogues
  - 2,821 utterances
  - 7 TV series
- **Test Set:**
  - 179 dialogues
  - 4,201 utterances
  - 11 TV series

## Key Resources & Links

- **Dataset Homepage:** [GitHub](https://github.com/AIM3-RUC/RUCM3ED)  
- **Features Download:** [Baidu Pan](https://pan.baidu.com/s/1xip42FAEBeBteSMUNYtHtQ) (code: y95k)  
- **Audio Download:** [Baidu Pan](https://pan.baidu.com/s/1JvaTabyKoQiWx2GtAIhpdw) (code: 6b5q)  

## Citation
If you use this dataset in your research, please cite the original paper.
