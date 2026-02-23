# 🚀 Deployment Guide

## Quick Deployment to Streamlit Cloud (Recommended)

### Step 1: Prepare Your Code

Make sure all files are ready:
```bash
# Check you have these files
ls -la
# Should see: app.py, agent.py, requirements.txt, etc.
```

### Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Agent Automation Pipeline"

# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/ai-agent-automation-pipeline.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: [share.streamlit.io](https://share.streamlit.io/)
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Select your repository**: `ai-agent-automation-pipeline`
5. **Set configuration**:
   - **Main file path**: `app.py`
   - **Python version**: 3.9 or higher
6. **Click "Deploy"**

⏱️ Deployment takes 2-3 minutes

### Step 4: Add API Key (Optional)

For enhanced AI features:

1. In Streamlit Cloud, go to your app
2. Click **"Settings"** (⚙️ icon)
3. Go to **"Secrets"** tab
4. Add:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-key-here"
   ```
5. App will automatically restart

### Step 5: Share Your Live Link

Your app will be available at:
```
https://your-app-name.streamlit.app
```

Share this link with your manager for testing! 🎉

## Alternative Deployment Options

### Option 1: Render

1. Create account at [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repository
4. Set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy

### Option 2: Railway

1. Create account at [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select repository
4. Railway auto-detects Streamlit
5. Deploy

### Option 3: Heroku

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Deploy via Heroku CLI or GitHub integration

## Local Testing Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Test at http://localhost:8501
```

## Troubleshooting

### Issue: App won't deploy
- ✅ Check `requirements.txt` has all dependencies
- ✅ Verify `app.py` is in root directory
- ✅ Ensure Python version is 3.9+

### Issue: PDF export not working
- ✅ Install reportlab: `pip install reportlab`
- ✅ Check it's in `requirements.txt`

### Issue: API key not working
- ✅ Verify key is in Streamlit secrets
- ✅ Check key format is correct
- ✅ App will work without API key (uses fallback)

## Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Can enter invoice and policy text
- [ ] "Run Task" button works
- [ ] Report displays correctly
- [ ] JSON download works
- [ ] PDF export works (if reportlab installed)
- [ ] Share link with manager

---

**Need help?** Check [INSTALL.md](INSTALL.md) for installation issues.
