# 🤖 AI Agent Automation Pipeline

> An intelligent task automation system that processes invoices, analyzes policies, and makes evidence-based approval decisions with full transparency.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 What It Does

This AI Agent automates invoice approval workflows by:
- **Analyzing** invoice details against company policies
- **Making decisions** (PASS/FAIL/NEEDS_INFO) with confidence scores
- **Providing evidence** with policy citations for every decision
- **Generating reports** in HTML, JSON, and PDF formats
- **Self-validating** its own output quality

Perfect for finance teams, procurement departments, or any organization that needs automated, auditable decision-making.

## ✨ Key Features

- 🧠 **Intelligent Orchestration**: 5-state workflow (Intake → Plan → Execute → Evaluate → Deliver)
- 📊 **Three Specialized Tools**: Data analysis, policy retrieval, and report generation
- 📄 **Multiple Export Formats**: HTML reports, JSON data, and PDF downloads
- 🔍 **Evidence-Based Decisions**: Every decision includes policy citations
- ✅ **Self-Evaluation**: Automatic quality checks and confidence scoring
- 📁 **CSV Support**: Upload CSV files or enter data manually

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-agent-automation-pipeline.git
cd ai-agent-automation-pipeline

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 How to Use

1. **Enter Your Request**: Describe what you want the agent to do
2. **Provide Invoice Details**: 
   - Enter text manually, OR
   - Upload a CSV file with invoice data
3. **Add Policy Rules**: Paste your approval policy text
4. **Run Task**: Click the "Run Task" button
5. **Review Results**: 
   - View the decision (PASS/FAIL/NEEDS_INFO)
   - Read the detailed report
   - Download JSON or PDF exports
   - Check execution details

## 🏗️ Architecture

### 5-State Workflow

```
User Input → INTAKE → PLAN → EXECUTE → EVALUATE → DELIVER → Results
```

1. **INTAKE**: Validates inputs, stores policy, analyzes CSV
2. **PLAN**: Creates 5-step execution plan (AI-generated or template)
3. **EXECUTE**: Runs each step using specialized tools
4. **EVALUATE**: Self-checks output quality and confidence
5. **DELIVER**: Generates final reports and JSON

### Three Core Tools

1. **Data Tool** 📊
   - Analyzes CSV files
   - Calculates statistics (mean, min, max)
   - Identifies missing values and top categories

2. **Policy Tool** 📚
   - Stores policy/documentation text
   - Retrieves relevant chunks using keyword matching
   - Provides citations for evidence-based decisions

3. **Writer Tool** ✍️
   - Generates structured HTML reports
   - Creates machine-readable JSON output
   - Exports professional PDF documents

## 📋 Use Case: Invoice Approval

### Input
- Invoice details (text or CSV)
- Approval policy rules

### Output
- **Decision**: PASS | FAIL | NEEDS_INFO
- **Reasons**: Clear explanations for the decision
- **Evidence**: Policy citations supporting the decision
- **Confidence Score**: Quality assessment (0-100%)
- **Next Actions**: Recommended follow-up steps

### Example

**Invoice**: $1,500 from ABC Supplies Inc. for office equipment  
**Policy**: "Invoices over $1,000 require manager approval"  
**Result**: NEEDS_INFO - Requires manager approval with 85% confidence

## 🔍 Self-Evaluation System

The agent automatically validates its own output:

- **Completeness**: Checks all required fields are present
- **Consistency**: Ensures decision matches confidence score
- **Evidence Quality**: Verifies policy citations are provided
- **Confidence Scoring**: Returns NEEDS_INFO if confidence < 70%

## 📦 Project Structure

```
ai-agent-automation-pipeline/
├── app.py                    # Main Streamlit UI
├── agent.py                  # Agent orchestrator & state machine
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── tools/
│   ├── data_tool.py         # CSV analysis tool
│   ├── policy_tool.py       # Policy retrieval tool
│   └── writer_tool.py       # Report generation tool
└── use_cases/
    └── invoice_approval.py  # Invoice approval logic
```

## 🌐 Live Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/ai-agent-automation-pipeline.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Add API Key** (Optional):
   - In Streamlit Cloud, go to Settings → Secrets
   - Add: `OPENAI_API_KEY = "your-key-here"`
   - App will auto-restart with enhanced AI features

**Your live URL**: `https://your-app-name.streamlit.app`

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **AI/ML**: OpenAI API (optional, with fallback)
- **Data Processing**: Pandas
- **PDF Generation**: ReportLab
- **Deployment**: Streamlit Community Cloud

## 📝 Requirements Met

✅ Simple web UI with user request, progress view, and outputs  
✅ Complete 5-state agent orchestrator  
✅ Three specialized tools (Data, Policy, Writer)  
✅ Invoice approval use case end-to-end  
✅ Self-evaluation with confidence scoring  
✅ Evidence-based decisions with citations  
✅ Multiple export formats (HTML, JSON, PDF)  
✅ CSV file upload support  
✅ Live deployment ready  

## 🎁 Extra Features

- ✅ **PDF Export**: Download reports as PDF
- ✅ **CSV Upload**: Process invoices from CSV files
- ✅ **Progress Tracking**: Real-time execution step visibility
- ✅ **Error Handling**: Graceful fallbacks and clear error messages

## 📚 Documentation

- [CODE_FLOW.md](CODE_FLOW.md) - Detailed step-by-step code flow
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [INSTALL.md](INSTALL.md) - Installation troubleshooting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Your Name - [Your Email](mailto:your.email@example.com)

## 🙏 Acknowledgments

- Built for AI-Pass style automation pipeline
- Uses Streamlit for rapid web app development
- OpenAI API for enhanced planning capabilities

---

**⭐ If you find this project useful, please give it a star!**
