# Installation Instructions

## Quick Install

```bash
pip install -r requirements.txt
```

Or if using pip3:

```bash
pip3 install -r requirements.txt
```

## If PDF Export Shows Error

If you see "PDF export not available" message:

1. **Install reportlab**:
   ```bash
   pip install reportlab
   ```
   or
   ```bash
   pip3 install reportlab
   ```

2. **Restart Streamlit**:
   - Stop the Streamlit app (Ctrl+C)
   - Restart with: `streamlit run app.py`

3. **Verify installation**:
   ```bash
   python -c "import reportlab; print('ReportLab installed')"
   ```

## For Streamlit Cloud Deployment

The `requirements.txt` file already includes reportlab, so it will be installed automatically when you deploy to Streamlit Cloud.

## Troubleshooting

- **ModuleNotFoundError**: Make sure you're using the same Python environment where you installed the packages
- **PDF button not showing**: Run a task first, then check the Report tab
- **Still not working**: Try `pip install --upgrade reportlab`
