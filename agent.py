from typing import Dict, Any, List, Optional
from enum import Enum
import tempfile
import os
from tools.data_tool import DataTool
from tools.policy_tool import PolicyTool
from tools.writer_tool import WriterTool
from use_cases.invoice_approval import InvoiceApproval
from config import get_openai_api_key

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AgentState(Enum):
    INTAKE = "intake"
    PLAN = "plan"
    EXECUTE = "execute"
    EVALUATE = "evaluate"
    DELIVER = "deliver"

class AgentOrchestrator:
    def __init__(self):
        self.state = AgentState.INTAKE
        self.data_tool = DataTool()
        self.policy_tool = PolicyTool()
        self.writer_tool = WriterTool()
        self.invoice_approval = InvoiceApproval()
        self.execution_log: List[Dict[str, Any]] = []
        self.plan: List[Dict[str, Any]] = []
        self.result: Optional[Dict[str, Any]] = None
        self.api_key = get_openai_api_key()

    def reset(self):
        self.state = AgentState.INTAKE
        self.execution_log = []
        self.plan = []
        self.result = None

    def intake(self, user_request: str, invoice_text: Optional[str] = None, policy_text: Optional[str] = None, csv_data: Optional[Any] = None) -> Dict[str, Any]:
        self.state = AgentState.INTAKE
        
        missing = []
        if not user_request:
            missing.append("user request")
        if not invoice_text and not csv_data:
            missing.append("invoice text or CSV file")
        if not policy_text:
            missing.append("policy text")

        if missing:
            return {
                "status": "needs_info",
                "missing": missing,
                "message": f"Please provide: {', '.join(missing)}"
            }

        if policy_text:
            self.policy_tool.store_policy(policy_text)
        
        if csv_data is not None:
            try:
                temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
                csv_data.to_csv(temp_file.name, index=False)
                temp_file.close()
                
                upload_result = self.data_tool.upload_csv(temp_file.name)
                if upload_result["status"] == "success":
                    analysis = self.data_tool.analyze()
                    self.execution_log.append({
                        "step": 0,
                        "name": "CSV Data Analysis",
                        "status": "success",
                        "output": {"upload": upload_result, "analysis": analysis}
                    })
                os.unlink(temp_file.name)
            except:
                pass

        return {
            "status": "success",
            "message": "Intake completed",
            "has_invoice": bool(invoice_text),
            "has_policy": bool(policy_text),
            "has_csv": csv_data is not None
        }

    def create_plan(self, invoice_text: str, user_request: str = "") -> Dict[str, Any]:
        self.state = AgentState.PLAN
        
        try:
            if self.api_key and OPENAI_AVAILABLE:
                client = openai.OpenAI(api_key=self.api_key)
                prompt = f"""Create a step-by-step plan for reviewing an invoice for approval. 
The task is: {user_request or 'Review invoice and determine approval based on policy'}

Available tools:
1. invoice_approval - Extract fields and check compliance
2. policy_tool - Retrieve policy citations
3. writer_tool - Generate reports

Return a JSON array with 3-7 steps. Each step should have: step (number), name, tool, description.
Keep it focused on invoice approval workflow."""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a task planning assistant. Return only valid JSON arrays."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                import json
                plan_text = response.choices[0].message.content.strip()
                if plan_text.startswith("```"):
                    plan_text = plan_text.split("```")[1]
                    if plan_text.startswith("json"):
                        plan_text = plan_text[4:]
                plan_data = json.loads(plan_text)
                
                if isinstance(plan_data, list) and len(plan_data) > 0:
                    self.plan = plan_data
                    for i, step in enumerate(self.plan, 1):
                        step["step"] = i
                    return {"status": "success", "plan": self.plan, "message": f"Created AI-generated plan with {len(self.plan)} steps"}
        except:
            pass
        
        self.plan = [
            {
                "step": 1,
                "name": "Extract Invoice Fields",
                "tool": "invoice_approval",
                "description": "Extract amount, vendor, date, and description from invoice text"
            },
            {
                "step": 2,
                "name": "Retrieve Policy Citations",
                "tool": "policy_tool",
                "description": "Find relevant policy chunks for invoice approval rules"
            },
            {
                "step": 3,
                "name": "Check Compliance",
                "tool": "invoice_approval",
                "description": "Evaluate invoice against policy rules and make decision"
            },
            {
                "step": 4,
                "name": "Evaluate Output",
                "tool": "agent",
                "description": "Self-check output quality and completeness"
            },
            {
                "step": 5,
                "name": "Generate Report",
                "tool": "writer_tool",
                "description": "Create structured report and JSON output"
            }
        ]

        return {
            "status": "success",
            "plan": self.plan,
            "message": f"Created plan with {len(self.plan)} steps"
        }

    def execute_step(self, step: Dict[str, Any], invoice_text: str) -> Dict[str, Any]:
        step_num = step["step"]
        step_name = step["name"]
        tool = step["tool"]

        log_entry = {
            "step": step_num,
            "name": step_name,
            "status": "running",
            "output": None
        }

        try:
            if tool == "invoice_approval":
                if step_num == 1:
                    fields = self.invoice_approval.extract_invoice_fields(invoice_text)
                    log_entry["output"] = fields
                    log_entry["status"] = "success"
                elif step_num == 3:
                    invoice_fields = self.execution_log[0]["output"] if self.execution_log else {}
                    policy_output = self.execution_log[1].get("output", {}) if len(self.execution_log) > 1 else {}
                    policy_citations = policy_output.get("results", [])
                    result = self.invoice_approval.check_policy_compliance(invoice_fields, policy_citations)
                    log_entry["output"] = result
                    log_entry["status"] = "success"

            elif tool == "policy_tool":
                if step_num == 2:
                    invoice_fields = self.execution_log[0]["output"] if self.execution_log else {}
                    amount = invoice_fields.get("amount", 0)
                    vendor = invoice_fields.get("vendor", "")
                    query = f"invoice approval amount {amount} vendor {vendor} policy limit"
                    result = self.policy_tool.retrieve(query, top_k=3)
                    log_entry["output"] = result
                    log_entry["status"] = "success"

            elif tool == "agent" and step_num == 4:
                compliance_result = self.execution_log[2].get("output", {}) if len(self.execution_log) > 2 else {}
                evaluation = self.evaluate(compliance_result)
                log_entry["output"] = evaluation
                log_entry["status"] = "success"

            elif tool == "writer_tool" and step_num == 5:
                compliance_result = self.execution_log[2].get("output", {}) if len(self.execution_log) > 2 else {}
                evaluation = self.execution_log[3].get("output", {}) if len(self.execution_log) > 3 else {}
                
                summary = f"Invoice approval decision: {compliance_result.get('decision', 'UNKNOWN')}"
                if self.api_key and OPENAI_AVAILABLE:
                    try:
                        client = openai.OpenAI(api_key=self.api_key)
                        prompt = f"Decision: {compliance_result.get('decision', 'UNKNOWN')}\nReasons: {', '.join(compliance_result.get('reasons', []))}\nGenerate a 2-3 sentence summary."
                        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], temperature=0.5, max_tokens=150)
                        summary = response.choices[0].message.content.strip()
                    except:
                        pass
                
                report_data = {
                    "summary": summary,
                    "findings": compliance_result.get("reasons", []),
                    "risks": [f"Confidence: {compliance_result.get('confidence', 0)}%"] if compliance_result.get('confidence', 0) < 70 else [],
                    "recommendations": evaluation.get("recommendations", []),
                    "evidence": compliance_result.get("evidence", [])
                }
                
                report = self.writer_tool.generate_report(report_data)
                json_output = self.writer_tool.generate_json(
                    decision=compliance_result.get("decision", "NEEDS_INFO"),
                    reasons=compliance_result.get("reasons", []),
                    evidence=compliance_result.get("evidence", []),
                    next_actions=evaluation.get("next_actions", [])
                )
                pdf_output = self.writer_tool.generate_pdf(report_data, compliance_result.get("decision", "NEEDS_INFO"))
                
                log_entry["output"] = {"report": report, "json": json_output, "pdf": pdf_output}
                log_entry["status"] = "success"
                self.result = log_entry["output"]

        except Exception as e:
            log_entry["status"] = "error"
            log_entry["output"] = {"error": str(e)}

        self.execution_log.append(log_entry)
        return log_entry

    def evaluate(self, compliance_result: Dict[str, Any]) -> Dict[str, Any]:
        self.state = AgentState.EVALUATE

        decision = compliance_result.get("decision", "NEEDS_INFO")
        confidence = compliance_result.get("confidence", 0)
        reasons = compliance_result.get("reasons", [])
        evidence = compliance_result.get("evidence", [])

        completeness_score = 0
        if decision in ["PASS", "FAIL", "NEEDS_INFO"]:
            completeness_score += 25
        if reasons:
            completeness_score += 25
        if evidence:
            completeness_score += 25
        if confidence is not None:
            completeness_score += 25

        is_consistent = (decision == "PASS" and confidence >= 70) or (decision == "FAIL" and confidence < 50) or (decision == "NEEDS_INFO" and 50 <= confidence < 70)
        consistency_score = 100 if is_consistent else 70

        evidence_quality = len(evidence) > 0
        overall_confidence = (completeness_score + consistency_score) / 2

        recommendations = []
        next_actions = []

        if completeness_score < 100:
            recommendations.append("Ensure all required fields are present in output")
        if not evidence_quality:
            recommendations.append("Add more policy citations to support decision")
        if overall_confidence < 70:
            recommendations.append("Review decision logic and policy matching")
            next_actions.append("Request additional information from user")

        if decision == "NEEDS_INFO":
            next_actions.append("Collect missing invoice details")
        elif decision == "PASS":
            next_actions.append("Proceed with invoice approval")
        elif decision == "FAIL":
            next_actions.append("Reject invoice and notify requester")

        return {
            "completeness_score": completeness_score,
            "consistency_score": consistency_score,
            "evidence_quality": evidence_quality,
            "overall_confidence": round(overall_confidence, 2),
            "recommendations": recommendations,
            "next_actions": next_actions,
            "final_decision": decision if overall_confidence >= 70 else "NEEDS_INFO"
        }

    def run(self, user_request: str, invoice_text: str, policy_text: str, csv_data: Optional[Any] = None) -> Dict[str, Any]:
        self.reset()

        intake_result = self.intake(user_request, invoice_text, policy_text, csv_data)
        if intake_result["status"] != "success":
            return intake_result

        plan_result = self.create_plan(invoice_text, user_request)
        if plan_result["status"] != "success":
            return plan_result

        self.state = AgentState.EXECUTE
        for step in self.plan:
            self.execute_step(step, invoice_text)

        self.state = AgentState.DELIVER

        return {
            "status": "success",
            "plan": self.plan,
            "execution_log": self.execution_log,
            "result": self.result,
            "final_state": self.state.value
        }
