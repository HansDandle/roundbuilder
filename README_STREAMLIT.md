# 🎯 TriviaMaster - Online Trivia Round Builder

A simple web app to build custom trivia rounds from your CSV question database. Filter by category, difficulty, or keyword, then export professional DOCX files.

**Live Demo:** [trivia-master.streamlit.app](https://trivia-master.streamlit.app) (Coming soon)

---

## ✨ Features

- 📤 **Upload CSV** - Load your trivia questions (Question, Answer, Category, Difficulty)
- 🔍 **Smart Filtering** - Filter by category, difficulty level, or keyword search
- 🎲 **Random Selection** - Generate truly random rounds from filtered questions
- 📥 **Export to DOCX** - Download professional Word documents ready for printing/sharing
- 🚀 **No Installation** - Works in your web browser, no setup needed
- 💾 **Secure** - Your data never leaves your browser or stays on our servers

---

## 🚀 Quick Start

### Option 1: Use Online (Easiest)
1. Go to [trivia-master.streamlit.app](https://trivia-master.streamlit.app)
2. Upload your CSV file
3. Configure filters and click "Generate"
4. Download DOCX file

### Option 2: Run Locally

**Requirements:**
- Python 3.8+
- pip

**Installation:**
```bash
# Clone or download the project
cd trivia-master

# Install dependencies
pip install -r requirements_streamlit.txt

# Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📋 CSV File Format

Your CSV file should have these columns:

| Question | Answer | Category | Difficulty |
|----------|--------|----------|------------|
| What is the capital of France? | Paris | Geography | Easy |
| Who wrote Romeo and Juliet? | William Shakespeare | Literature | Medium |
| What is H2O? | Water | Science | Easy |

**Requirements:**
- Column names: `Question`, `Answer`, `Category`, `Difficulty` (case-insensitive)
- Additional columns are ignored but won't cause errors
- CSV encoding: UTF-8 (standard)

---

## 🎮 How to Use

### Step 1: Load Questions
1. Click "Upload CSV file with trivia questions"
2. Select your CSV file
3. Click "📥 Load CSV"
4. See stats: total questions, categories, difficulties

### Step 2: Configure Round
- **Category**: Filter to specific category or "All Categories"
- **Difficulty**: Choose a difficulty level or "All Difficulties"
- **Keyword** (optional): Search questions/answers containing a word
- **Number of Questions**: How many questions to include (1-100)
- **Round Name**: Give your round a name (appears in DOCX)

### Step 3: Generate
- Click "🎲 Generate Random Round"
- Review the 10 questions in the expandable list
- Each question shows: text, answer, category, difficulty

### Step 4: Export
- Click "📥 Export to DOCX"
- Click "⬇️ Download DOCX"
- Open in Microsoft Word, Google Docs, or any compatible program

---

## 📊 Example CSV

Here's a sample CSV you can test with:

```csv
Question,Answer,Category,Difficulty
What is the largest planet in our solar system?,Jupiter,Science,Easy
Who was the first President of the United States?,George Washington,History,Easy
What is the chemical symbol for gold?,Au,Science,Medium
In what year did the Titanic sink?,1912,History,Medium
What is the smallest prime number?,2,Mathematics,Easy
```

---

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial TriviaMaster"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file to `app.py`
   - Click "Deploy"

3. **Share your link!**
   - Your app is live at: `https://share.streamlit.io/USERNAME/trivia-master/main/app.py`

### Other Deployment Options
- **Render**: [render.com](https://render.com) (paid tier, but simple)
- **Railway**: [railway.app](https://railway.app)
- **Heroku**: [heroku.com](https://heroku.com) (paid)
- **Self-hosted**: Any server with Python 3.8+

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit (Python)
- **Backend**: SimpleRoundBuilder (pure Python)
- **Export**: python-docx
- **Hosting**: Streamlit Cloud (free tier)

### Dependencies
- `streamlit` - Web framework
- `pandas` - CSV handling
- `python-docx` - DOCX generation
- `nltk` - Text processing
- `numpy` - Numerical operations

### File Structure
```
trivia-master/
├── app.py                      # Main Streamlit app
├── requirements_streamlit.txt  # Dependencies
├── DEPLOYMENT.md              # Deployment guide
├── README.md                  # This file
└── trivia_master/
    ├── core/
    │   └── simple_round_builder.py
    ├── utils/
    │   └── docx_exporter.py
    ├── config.py
    └── __init__.py
```

---

## 💡 Tips & Tricks

### Generate Multiple Rounds
- Generate Round 1 → Export
- Generate Round 2 → Export
- Each gets a unique filename

### Filter for Specific Content
- **Keyword**: Search for "history" to get history-related questions
- **Difficulty**: "Easy" → Beginner round, "Hard" → Advanced round
- **Category**: "Science" → Science-only round

### Edit Exported DOCX
- Open in Word/Google Docs
- Add answer key section
- Add spacing for players to write answers
- Add scoring information
- Share with your trivia team!

---

## ❓ FAQ

**Q: Is my data safe?**
A: Yes! Your CSV file is never stored. It's uploaded to your browser session and deleted when you refresh.

**Q: Can I use very large CSV files?**
A: Streamlit Cloud has a 200MB file limit, so most CSV files work fine. A file with 100,000 questions is only ~5-10MB.

**Q: Can I modify the questions before exporting?**
A: Not in-app, but you can download the DOCX and edit it in Word.

**Q: Can I use this offline?**
A: Yes! Run locally with `streamlit run app.py` and it works completely offline.

**Q: Can I add custom formatting to the DOCX?**
A: Yes! Edit the DOCX after downloading, or modify `trivia_master/utils/docx_exporter.py` and redeploy.

**Q: What if I find a bug?**
A: Report it on GitHub Issues or contact the developer.

---

## 🔄 Update History

**v1.0** (Feb 2026)
- ✅ Initial release
- ✅ CSV upload
- ✅ Filtering by category/difficulty/keyword
- ✅ Random round generation
- ✅ DOCX export
- ✅ Streamlit Cloud deployment

---

## 📝 License

MIT License - Free to use, modify, and share!

---

## 🤝 Contributing

Want to improve TriviaMaster?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Support

- **GitHub Issues**: Report bugs or request features
- **Email**: [contact via repo]
- **Documentation**: See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

---

## 🎉 Get Started Now!

1. **[Try the online app](https://trivia-master.streamlit.app)** (Coming soon)
2. **[Run locally](#option-2-run-locally)** with your CSV
3. **[Deploy your own](DEPLOYMENT.md)** to share with others

---

Made with ❤️ using Streamlit
