# 📁 Files to Push to GitHub

## ✅ Files to INCLUDE (Push These)

### Core Application Files
- ✅ `app.py` - Main Streamlit UI
- ✅ `agent.py` - Agent orchestrator
- ✅ `config.py` - Configuration

### Tools Directory
- ✅ `tools/__init__.py`
- ✅ `tools/data_tool.py`
- ✅ `tools/policy_tool.py`
- ✅ `tools/writer_tool.py`

### Use Cases Directory
- ✅ `use_cases/__init__.py`
- ✅ `use_cases/invoice_approval.py`

### Configuration Files
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Git ignore rules
- ✅ `.streamlit/config.toml` - Streamlit config

### Documentation Files
- ✅ `README.md` - Main documentation
- ✅ `DEPLOYMENT.md` - Deployment guide
- ✅ `INSTALL.md` - Installation guide
- ✅ `CODE_FLOW.md` - Code flow documentation
- ✅ `SUMMARY.md` - Project summary

## ❌ Files to EXCLUDE (Don't Push These)

### Sensitive Files
- ❌ `.streamlit/secrets.toml` - Contains API keys
- ❌ `.env` - Environment variables

### Generated Files
- ❌ `__pycache__/` - Python cache
- ❌ `*.pyc` - Compiled Python files
- ❌ `*.pdf` - Generated PDFs
- ❌ `*.csv` - Data files

### System Files
- ❌ `.DS_Store` - macOS system file
- ❌ `*.log` - Log files

### Virtual Environments
- ❌ `venv/`
- ❌ `env/`
- ❌ `.venv/`

## 🚀 Quick Push Command

```bash
# Make sure .gitignore is set up correctly
git add .
git commit -m "Initial commit: AI Agent Automation Pipeline"
git push origin main
```

The `.gitignore` file will automatically exclude sensitive and unnecessary files.

## ⚠️ Important Notes

1. **Never push secrets.toml** - Contains your API key
2. **Never push .env files** - May contain sensitive data
3. **Check before pushing**: `git status` to see what will be committed
4. **For Streamlit Cloud**: Add API key in Streamlit Cloud secrets, not in code

## 📋 Pre-Push Checklist

- [ ] All code files are included
- [ ] `requirements.txt` is up to date
- [ ] `README.md` is complete
- [ ] `.gitignore` excludes sensitive files
- [ ] No API keys in code
- [ ] No personal data in files
- [ ] Documentation is complete
