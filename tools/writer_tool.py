from typing import Dict, Any, List
import json
from io import BytesIO

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class WriterTool:
    def __init__(self):
        pass

    def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        summary = data.get("summary", "No summary provided")
        findings = data.get("findings", [])
        risks = data.get("risks", [])
        recommendations = data.get("recommendations", [])
        evidence = data.get("evidence", [])

        html_report = f"""
        <html>
        <head>
            <title>AI Agent Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; margin-top: 20px; }}
                .section {{ margin: 15px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }}
                .finding, .risk, .recommendation {{ margin: 10px 0; padding: 8px; background: white; border-left: 3px solid #007bff; }}
                .evidence {{ margin: 10px 0; padding: 8px; background: #e7f3ff; border-left: 3px solid #0056b3; }}
                ul {{ margin: 10px 0; }}
                li {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            <h1>AI Agent Task Report</h1>
            
            <div class="section">
                <h2>Summary</h2>
                <p>{summary}</p>
            </div>
            
            <div class="section">
                <h2>Findings</h2>
                <ul>
        """
        
        for finding in findings:
            html_report += f"<li class='finding'>{finding}</li>\n"
        
        html_report += """
                </ul>
            </div>
            
            <div class="section">
                <h2>Risks</h2>
                <ul>
        """
        
        for risk in risks:
            html_report += f"<li class='risk'>{risk}</li>\n"
        
        html_report += """
                </ul>
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                <ul>
        """
        
        for rec in recommendations:
            html_report += f"<li class='recommendation'>{rec}</li>\n"
        
        html_report += """
                </ul>
            </div>
            
            <div class="section">
                <h2>Evidence / Citations</h2>
                <ul>
        """
        
        for ev in evidence:
            html_report += f"<li class='evidence'>{ev}</li>\n"
        
        html_report += """
                </ul>
            </div>
        </body>
        </html>
        """
        
        return {
            "status": "success",
            "html_report": html_report,
            "message": "Report generated successfully"
        }

    def generate_json(self, decision: str, reasons: List[str], evidence: List[str], next_actions: List[str]) -> Dict[str, Any]:
        json_output = {
            "decision": decision,
            "reasons": reasons,
            "evidence": evidence,
            "next_actions": next_actions
        }
        
        return {
            "status": "success",
            "json_output": json_output,
            "json_string": json.dumps(json_output, indent=2),
            "message": "JSON generated successfully"
        }

    def generate_pdf(self, data: Dict[str, Any], decision: str) -> Dict[str, Any]:
        if not REPORTLAB_AVAILABLE:
            return {
                "status": "error",
                "message": "ReportLab library not available. Install with: pip install reportlab"
            }
        
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
            story = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#1f77b4',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor='#333',
                spaceAfter=12,
                spaceBefore=20
            )
            
            normal_style = styles['Normal']
            normal_style.fontSize = 11
            normal_style.leading = 14
            
            story.append(Paragraph("AI Agent Task Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            summary = data.get("summary", "No summary provided")
            story.append(Paragraph("Summary", heading_style))
            story.append(Paragraph(summary, normal_style))
            story.append(Spacer(1, 0.1*inch))
            
            findings = data.get("findings", [])
            if findings:
                story.append(Paragraph("Findings", heading_style))
                for finding in findings:
                    story.append(Paragraph(f"• {finding}", normal_style))
                story.append(Spacer(1, 0.1*inch))
            
            risks = data.get("risks", [])
            if risks:
                story.append(Paragraph("Risks", heading_style))
                for risk in risks:
                    story.append(Paragraph(f"• {risk}", normal_style))
                story.append(Spacer(1, 0.1*inch))
            
            recommendations = data.get("recommendations", [])
            if recommendations:
                story.append(Paragraph("Recommendations", heading_style))
                for rec in recommendations:
                    story.append(Paragraph(f"• {rec}", normal_style))
                story.append(Spacer(1, 0.1*inch))
            
            evidence = data.get("evidence", [])
            if evidence:
                story.append(Paragraph("Evidence / Citations", heading_style))
                for ev in evidence:
                    ev_text = ev[:200] + "..." if len(ev) > 200 else ev
                    story.append(Paragraph(f"• {ev_text}", normal_style))
                story.append(Spacer(1, 0.1*inch))
            
            decision_style = ParagraphStyle(
                'Decision',
                parent=styles['Normal'],
                fontSize=14,
                textColor='#155724' if decision == 'PASS' else '#721c24' if decision == 'FAIL' else '#856404',
                spaceBefore=20,
                spaceAfter=10,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(f"Decision: {decision}", decision_style))
            
            doc.build(story)
            buffer.seek(0)
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            return {
                "status": "success",
                "pdf_bytes": pdf_bytes,
                "message": "PDF generated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating PDF: {str(e)}"
            }
