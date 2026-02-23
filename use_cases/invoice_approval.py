from typing import Dict, Any, List
import re

class InvoiceApproval:
    def __init__(self):
        pass

    def extract_invoice_fields(self, invoice_text: str) -> Dict[str, Any]:
        fields = {
            "amount": None,
            "vendor": None,
            "date": None,
            "description": None,
            "invoice_number": None
        }

        amount_pattern = r'\$?([\d,]+\.?\d*)'
        amounts = re.findall(amount_pattern, invoice_text)
        if amounts:
            try:
                fields["amount"] = float(amounts[-1].replace(',', ''))
            except:
                pass

        vendor_patterns = [
            r'vendor[:\s]+([A-Za-z\s]+)',
            r'from[:\s]+([A-Za-z\s]+)',
            r'supplier[:\s]+([A-Za-z\s]+)'
        ]
        for pattern in vendor_patterns:
            match = re.search(pattern, invoice_text, re.IGNORECASE)
            if match:
                fields["vendor"] = match.group(1).strip()
                break

        date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        dates = re.findall(date_pattern, invoice_text)
        if dates:
            fields["date"] = dates[0]

        inv_pattern = r'invoice[#\s:]+([A-Z0-9-]+)'
        match = re.search(inv_pattern, invoice_text, re.IGNORECASE)
        if match:
            fields["invoice_number"] = match.group(1)

        desc_match = re.search(r'description[:\s]+(.+?)(?:\n|$)', invoice_text, re.IGNORECASE)
        if desc_match:
            fields["description"] = desc_match.group(1).strip()
        else:
            fields["description"] = invoice_text[:100]

        return fields

    def check_policy_compliance(self, invoice_fields: Dict[str, Any], policy_citations: List[Dict[str, Any]]) -> Dict[str, Any]:
        decision = "NEEDS_INFO"
        reasons = []
        confidence = 0
        missing_info = []

        if not invoice_fields.get("amount"):
            missing_info.append("Invoice amount")
        if not invoice_fields.get("vendor"):
            missing_info.append("Vendor name")
        if not invoice_fields.get("date"):
            missing_info.append("Invoice date")

        if missing_info:
            return {
                "decision": "NEEDS_INFO",
                "reasons": [f"Missing required information: {', '.join(missing_info)}"],
                "confidence": 0,
                "evidence": []
            }

        amount = invoice_fields.get("amount", 0)
        vendor = invoice_fields.get("vendor", "").lower()
        description = invoice_fields.get("description", "").lower()

        policy_text = " ".join([c.get("text", "").lower() for c in policy_citations])

        checks = []

        if "limit" in policy_text or "maximum" in policy_text:
            limit_match = re.search(r'(\$?[\d,]+\.?\d*)', policy_text)
            if limit_match:
                try:
                    limit = float(limit_match.group(1).replace(',', '').replace('$', ''))
                    if amount > limit:
                        checks.append(("Amount exceeds policy limit", amount > limit))
                    else:
                        checks.append(("Amount within policy limit", True))
                except:
                    pass

        if "approval" in policy_text and "required" in policy_text:
            if amount > 1000:
                checks.append(("High-value invoice requires approval", True))
            else:
                checks.append(("Amount below approval threshold", True))

        if "vendor" in policy_text:
            if "blacklist" in policy_text or "prohibited" in policy_text:
                if "test" in vendor or "demo" in vendor:
                    checks.append(("Vendor may be on prohibited list", True))
                else:
                    checks.append(("Vendor check passed", True))

        if "description" in policy_text or "category" in policy_text:
            if "expense" in description or "service" in description:
                checks.append(("Description matches expense category", True))

        pass_count = sum(1 for _, passed in checks if passed)
        total_checks = len(checks) if checks else 1
        confidence = (pass_count / total_checks) * 100

        if confidence >= 80:
            decision = "PASS"
        elif confidence >= 50:
            decision = "NEEDS_INFO"
        else:
            decision = "FAIL"

        reasons = [check[0] for check in checks]
        if not reasons:
            reasons = ["Basic invoice information present"]

        evidence = [c.get("text", "")[:100] + "..." for c in policy_citations[:3]]

        return {
            "decision": decision,
            "reasons": reasons,
            "confidence": round(confidence, 2),
            "evidence": evidence,
            "invoice_fields": invoice_fields
        }
