import streamlit as st
from agent import AgentOrchestrator

st.set_page_config(
    page_title="AI Agent Automation Pipeline",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    .decision-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .decision-pass {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .decision-fail {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .decision-needs-info {
        background-color: #fff3cd;
        color: #856404;
        border: 2px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">AI Agent Automation Pipeline</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Invoice Approval Decision System</p>', unsafe_allow_html=True)

if "agent" not in st.session_state:
    st.session_state.agent = AgentOrchestrator()

if "running" not in st.session_state:
    st.session_state.running = False

if "result" not in st.session_state:
    st.session_state.result = None

st.markdown("### User Request")
user_request = st.text_area(
    "Enter your task request",
    value="Please review this invoice and determine if it should be approved based on the policy.",
    height=80,
    help="Describe what you want the agent to do",
    label_visibility="collapsed"
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Invoice Details")
    
    input_method = st.radio(
        "Input method:",
        ["Text Input", "CSV Upload"],
        horizontal=True,
        key="input_method"
    )
    
    if input_method == "CSV Upload":
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV file with invoice data (columns: invoice_number, vendor, date, description, amount)"
        )
        
        if uploaded_file is not None:
            import pandas as pd
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✓ CSV loaded: {len(df)} row(s), {len(df.columns)} column(s)")
                
                if len(df) > 0:
                    row = df.iloc[0]
                    invoice_text = f"""Invoice #{row.get('invoice_number', row.get('Invoice Number', 'N/A'))}
Vendor: {row.get('vendor', row.get('Vendor', 'N/A'))}
Date: {row.get('date', row.get('Date', 'N/A'))}
Description: {row.get('description', row.get('Description', 'N/A'))}
Amount: ${row.get('amount', row.get('Amount', 0))}"""
                    st.session_state.csv_data = df
                    st.session_state.csv_uploaded = True
                    with st.expander("Preview CSV Data"):
                        st.dataframe(df.head())
                else:
                    st.warning("CSV file is empty")
                    invoice_text = ""
                    st.session_state.csv_uploaded = False
            except Exception as e:
                st.error(f"Error: {str(e)}")
                invoice_text = ""
                st.session_state.csv_uploaded = False
        else:
            invoice_text = ""
            st.session_state.csv_uploaded = False
    else:
        invoice_text = st.text_area(
            "Enter invoice information",
            value="""Invoice #INV-2024-001
Vendor: ABC Supplies Inc.
Date: 12/15/2024
Description: Office supplies and equipment
Amount: $1,500.00""",
            height=180,
            help="Enter the invoice details to be reviewed",
            label_visibility="collapsed"
        )
        st.session_state.csv_uploaded = False

with col2:
    st.markdown("### Approval Policy")
    policy_text = st.text_area(
        "Enter policy rules",
        value="""Invoice Approval Policy:
- Invoices over $1,000 require manager approval
- Maximum single invoice limit is $5,000
- All invoices must have valid vendor, date, and description
- Prohibited vendors: Test Company, Demo Vendor
- Expense categories must be clearly stated""",
        height=180,
        help="Enter the approval policy rules",
        label_visibility="collapsed"
    )

st.markdown("---")
submitted = st.button("Run Task", use_container_width=True, type="primary")

if submitted:
    st.session_state.running = True
    st.session_state.result = None

if st.session_state.running:
    st.markdown("### Execution Progress")
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        csv_data = st.session_state.get('csv_data', None)
        csv_uploaded = st.session_state.get('csv_uploaded', False)
        
        result = st.session_state.agent.run(
            user_request=user_request,
            invoice_text=invoice_text,
            policy_text=policy_text,
            csv_data=csv_data if csv_uploaded else None
        )
        
        if hasattr(st.session_state.agent, 'plan') and st.session_state.agent.plan:
            total_steps = len(st.session_state.agent.plan)
            steps_status = []
            
            for i, step in enumerate(st.session_state.agent.plan):
                log_entry = next((log for log in st.session_state.agent.execution_log if log['step'] == step['step']), None)
                status_icon = "✓" if log_entry and log_entry['status'] == 'success' else "⏳"
                steps_status.append(f"{status_icon} Step {step['step']}: {step['name']}")
            
            progress_placeholder.markdown("\n".join([f"- {s}" for s in steps_status]))
            status_placeholder.success("✓ All steps completed successfully!")
        
        st.session_state.result = result
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.result = {"status": "error", "message": str(e)}
    finally:
        st.session_state.running = False

if st.session_state.result:
    result = st.session_state.result
    
    if result.get("status") == "error":
        st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
    elif result.get("status") == "needs_info":
        st.warning(f"⚠️ {result.get('message', 'Missing information')}")
    else:
        st.markdown("---")
        
        if hasattr(st.session_state.agent, 'result') and st.session_state.agent.result:
            report_data = st.session_state.agent.result.get("report", {})
            json_data = st.session_state.agent.result.get("json", {})
            
            if json_data.get("json_output"):
                decision = json_data["json_output"].get("decision", "UNKNOWN")
                decision_class = {
                    "PASS": "decision-pass",
                    "FAIL": "decision-fail",
                    "NEEDS_INFO": "decision-needs-info"
                }.get(decision, "decision-needs-info")
                st.markdown(f'<div class="{decision_class} decision-box">Decision: {decision}</div>', unsafe_allow_html=True)
            
            st.markdown("### Results")
            tab1, tab2, tab3 = st.tabs(["📄 Report", "📦 JSON Output", "⚙️ Execution Details"])
            
            with tab1:
                if report_data.get("html_report"):
                    st.components.v1.html(report_data["html_report"], height=600, scrolling=True)
                    
                    pdf_data = st.session_state.agent.result.get("pdf", {})
                    if pdf_data.get("status") == "success" and pdf_data.get("pdf_bytes"):
                        st.download_button(
                            label="📄 Export PDF",
                            data=pdf_data.get("pdf_bytes"),
                            file_name="agent_report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    elif pdf_data:
                        error_msg = pdf_data.get("message", "PDF export not available")
                        st.warning(f"⚠️ {error_msg}")
                    else:
                        st.info("💡 PDF export will be available after running the task")
                else:
                    st.info("No report generated")
            
            with tab2:
                if json_data.get("json_output"):
                    st.json(json_data["json_output"])
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_data.get("json_string", ""),
                        file_name="agent_output.json",
                        mime="application/json",
                        use_container_width=True
                    )
                else:
                    st.info("No JSON output generated")
            
            with tab3:
                if hasattr(st.session_state.agent, 'plan') and st.session_state.agent.plan:
                    st.markdown("#### Execution Steps")
                    for step in st.session_state.agent.plan:
                        log_entry = next((log for log in st.session_state.agent.execution_log if log['step'] == step['step']), None)
                        if log_entry and log_entry['status'] == 'success':
                            st.success(f"✓ Step {step['step']}: {step['name']}")
                        else:
                            st.error(f"✗ Step {step['step']}: {step['name']}")
                else:
                    st.info("No execution details available")
