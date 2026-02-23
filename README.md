# 🤖 AI Agent Automation Pipeline

> Intelligent invoice approval automation system with evidence-based decision making and policy compliance checking.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

## 🎯 Overview

Automates invoice approval workflows by analyzing invoices against company policies, making evidence-based decisions (PASS/FAIL/NEEDS_INFO), and generating comprehensive reports in HTML, JSON, and PDF formats.

## ✨ Features

- 🧠 **5-State Workflow**: Intake → Plan → Execute → Evaluate → Deliver
- 📊 **Three Tools**: Data analysis, policy retrieval, report generation
- 📄 **Multiple Exports**: HTML reports, JSON data, PDF downloads
- 🔍 **Evidence-Based**: Every decision includes policy citations
- ✅ **Self-Evaluation**: Automatic quality checks and confidence scoring
- 📁 **CSV Support**: Upload CSV files or enter data manually

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/faisalrehman1122/ai-agent-automation-pipeline-invoice-policy-approval.git
cd ai-agent-automation-pipeline-invoice-policy-approval
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

## 📖 Usage

1. Enter your task request
2. Provide invoice details (text or CSV upload)
3. Add policy rules
4. Click "Run Task"
5. Review decision, report, and download exports

## 🏗️ Architecture

### Workflow

```
User Input → INTAKE → PLAN → EXECUTE → EVALUATE → DELIVER → Results
```

### Tools

1. **Data Tool**: CSV analysis (statistics, missing values, categories)
2. **Policy Tool**: Policy retrieval with keyword matching and citations
3. **Writer Tool**: Report generation (HTML, JSON, PDF)

## 📋 Use Case: Invoice Approval

**Input**: Invoice details + Policy rules  
**Output**: Decision (PASS/FAIL/NEEDS_INFO) with reasons, evidence, and confidence score

## 🌐 Live Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect repository and deploy
4. Add API key in Settings → Secrets (optional)

## 📦 Project Structure

```
├── app.py                    # Main Streamlit UI
├── agent.py                  # Agent orchestrator
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── tools/                    # Three specialized tools
└── use_cases/                # Invoice approval logic
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **AI**: OpenAI API (optional, with fallback)
- **Data**: Pandas
- **PDF**: ReportLab

## 📝 Requirements Met

✅ Web UI with user request, progress view, outputs  
✅ 5-state agent orchestrator  
✅ Three tools (Data, Policy, Writer)  
✅ Invoice approval use case  
✅ Self-evaluation system  
✅ Evidence-based decisions  
✅ Multiple export formats  
✅ CSV upload support  

## 🎁 Extra Features

- ✅ PDF Export
- ✅ CSV Upload
- ✅ Progress Tracking
- ✅ Error Handling


MIT License

---

**⭐ Star this repo if you find it useful!**
