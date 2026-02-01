# Deploy TriviaMaster to Streamlit Cloud

## Option 1: Deploy Free to Streamlit Cloud (Recommended)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial TriviaMaster commit"
git remote add origin https://github.com/YOUR_USERNAME/trivia-master.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set main file path to: `app.py`
6. Click "Deploy"

**That's it!** Your app is live at: `https://share.streamlit.io/YOUR_USERNAME/trivia-master/main/app.py`

### Features:
- ✅ Free tier (unlimited apps)
- ✅ Auto-deploys on GitHub push
- ✅ SSL certificate included
- ✅ Custom domain support (paid)

---

## Option 2: Deploy to Other Platforms

### Render.com (Free tier available)
```bash
# Create render.yaml in project root
```

### Railway.app
```bash
# Similar to Render, very simple deployment
```

### Heroku (Paid)
```bash
heroku create your-app-name
git push heroku main
```

---

## Local Testing

Before deploying, test locally:

```bash
pip install -r requirements_streamlit.txt
streamlit run app.py
```

Then open: `http://localhost:8501`

---

## File Structure for Deployment

```
trivia-master/
├── app.py                      # Main Streamlit app
├── requirements_streamlit.txt  # Python dependencies
├── .gitignore                  # Git ignore file
├── README.md                   # This file
└── trivia_master/              # Your package
    ├── core/
    │   └── simple_round_builder.py
    ├── utils/
    │   └── docx_exporter.py
    ├── config.py
    └── __init__.py
```

---

## Environment Variables (if needed)

If you add database or API keys later, set them in Streamlit Cloud:
- App settings → Secrets
- Add environment variables there

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'trivia_master'"
- Make sure directory structure is correct
- Verify `trivia_master/__init__.py` exists

### "File upload not working"
- Streamlit Cloud has temp file storage
- Our app uses `/tmp/` which works on all platforms

### "DOCX export fails"
- Ensure `python-docx` is in requirements
- Check temp directory permissions

---

## Performance Notes

- **CSV Upload**: Streamlit Cloud has 200MB file size limit
- **Processing**: Instant for most CSV files
- **Caching**: Use `@st.cache_data` decorator for larger files (already optimized)

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy to Streamlit Cloud
3. ✅ Test with your CSV
4. ✅ Share the URL with friends/colleagues
5. 🎉 Done!

---

**Questions?** Check the [Streamlit docs](https://docs.streamlit.io) or GitHub issues
