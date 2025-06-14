# 📊 WhatsApp Chat Analyzer

A Streamlit‑based Python application for analyzing WhatsApp chat exports — group or one-on-one. Parse `.txt` chat logs to generate meaningful insights through statistics, visualizations, sentiment and emoji analysis, word clouds, and more.

---

## 🔍 Features

- **Chat parsing**: Reads WhatsApp `.txt` chat exports (without media).
- **General stats**: Total messages, words, media, links shared.
- **Time-series insights**: Activity timelines by month and day.
- **User analysis**:
  - Most active participants overall.
  - Activity heatmaps showing peak days & hours.
- **Text visualization**:
  - Word cloud of frequent words.
  - Top used words list (with stopword filtering).
- **Emoji exploration**:
  - Emoji usage counts.
  - Emoji vs non-emoji message ratio.
  - Sentiment categorization (positive/neutral/negative).
- **Sentiment analysis**: Overall sentiment breakdown via text/emojis.
- **Interactive visuals**: Rich charts powered by Plotly/Streamlit :contentReference[oaicite:1]{index=1}.

---

## 🚀 Tech Stack

- **Python 3.7+**
- **Streamlit** – UI & dashboard  
- **NLTK** – Text preprocessing  
- **Plotly** – Charts & visuals  
- **Pandas** – Data wrangling  
- **Emoji** – Emoji parsing  
- **Other** – `re`, `wordcloud`, `matplotlib`, etc.

---

## ⚙️ Getting Started

### 1. Clone this repo  
```bash
git clone https://github.com/Pritush09/Whatsapp-Chat-Analyzer.git
cd Whatsapp-Chat-Analyzer
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run application
```
streamlit run app.py
```
The app will launch at:
```
http://localhost:8501
```

🚀 Usage
Export chat: From WhatsApp → More options → Export chat → Without media → Save .txt.

Upload file: Use the Streamlit sidebar file uploader.

Select user: Optionally filter by individual sender or view group overview.

View insights: Explore statistics, timelines, heatmaps, word clouds, emoji/sentiment breakdowns.

Download data: (If implemented) Export visualizations or summary tables.

🗂️ Project Structure
```
.
├── app.py             # Main Streamlit interface
├── preprocessor.py    # Parsing & cleaning chat data
├── helper.py          # Analysis/helpers functions
├── requirements.txt   # Python dependencies
├── stopwords.txt      # Word cloud / common word filter
└── README.md
```

🛠️ Contributing
Contributions are welcome! Feel free to:

🐞 Report bugs via issues

💡 Suggest new features

✅ Submit PRs — just fork, branch, commit, and open a pull request

