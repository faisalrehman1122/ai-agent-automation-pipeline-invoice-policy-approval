# Quick Start Guide

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser:**
   - The app will automatically open at `http://localhost:8501`

## Testing the Invoice Approval Flow

1. **Use the default example:**
   - The form comes pre-filled with example invoice and policy text
   - Click "Run Task" to see the full flow

2. **Try your own invoice:**
   - Replace the invoice text with your own
   - Update the policy text with your rules
   - Click "Run Task"

3. **View results:**
   - Check the execution plan steps
   - Review the HTML report
   - Download the JSON output

## Example Invoice Format

```
Invoice #INV-2024-001
Vendor: ABC Supplies Inc.
Date: 12/15/2024
Description: Office supplies and equipment
Amount: $1,500.00
```

## Example Policy Format

```
Invoice Approval Policy:
- Invoices over $1,000 require manager approval
- Maximum single invoice limit is $5,000
- All invoices must have valid vendor, date, and description
- Prohibited vendors: Test Company, Demo Vendor
- Expense categories must be clearly stated
```

## Deployment to Streamlit Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
