# Step-by-Step Code Flow

## Overview
This AI Agent automates invoice approval decisions by following a 5-state workflow.

---

## Complete Flow

### STEP 1: User Input (app.py)
**Location**: `app.py` lines 74-166

**What happens**:
1. User enters task request (e.g., "Review invoice for approval")
2. User provides invoice details (text or CSV upload)
3. User provides policy text (approval rules)
4. User clicks "Run Task" button

**Output**: All inputs collected and ready

---

### STEP 2: Agent Initialization (agent.py)
**Location**: `agent.py` lines 346-351

**What happens**:
1. `agent.run()` is called with all inputs
2. Agent resets its state (clears previous execution)
3. Agent moves to INTAKE state

---

### STEP 3: INTAKE State (agent.py)
**Location**: `agent.py` lines 44-94

**What happens**:
1. Validates all required inputs are provided
2. Stores policy text in Policy Tool
3. If CSV uploaded:
   - Saves CSV to temporary file
   - Uses Data Tool to analyze CSV
   - Logs analysis results
4. Returns success or requests missing info

**Output**: Validated inputs, policy stored, CSV analyzed (if provided)

---

### STEP 4: PLAN State (agent.py)
**Location**: `agent.py` lines 96-180

**What happens**:
1. Tries to generate plan using OpenAI API (if available)
2. If API fails or unavailable, uses default 5-step plan:
   - Step 1: Extract Invoice Fields
   - Step 2: Retrieve Policy Citations
   - Step 3: Check Compliance
   - Step 4: Evaluate Output
   - Step 5: Generate Report

**Output**: Execution plan with 5 steps

---

### STEP 5: EXECUTE State (agent.py)
**Location**: `agent.py` lines 357-359

**What happens**: For each step in plan, calls `execute_step()`

#### Step 1: Extract Invoice Fields
**Location**: `agent.py` lines 208-212
- Uses `InvoiceApproval.extract_invoice_fields()`
- Extracts: amount, vendor, date, description, invoice_number
- Uses regex patterns to find data in text

#### Step 2: Retrieve Policy Citations
**Location**: `agent.py` lines 220-228
- Uses `PolicyTool.retrieve()`
- Searches policy text for relevant chunks
- Returns top 3 matching policy sections

#### Step 3: Check Compliance
**Location**: `agent.py` lines 213-218
- Uses `InvoiceApproval.check_policy_compliance()`
- Compares invoice against policy rules
- Calculates confidence score
- Makes decision: PASS / FAIL / NEEDS_INFO

#### Step 4: Evaluate Output
**Location**: `agent.py` lines 230-235
- Calls `evaluate()` method
- Checks completeness, consistency, evidence quality
- Calculates overall confidence
- Provides recommendations

#### Step 5: Generate Report
**Location**: `agent.py` lines 237-286
- Uses `WriterTool.generate_report()` for HTML
- Uses `WriterTool.generate_json()` for JSON
- Optionally uses OpenAI for summary (if available)
- Creates final output

**Output**: All steps executed, results logged

---

### STEP 6: EVALUATE State (agent.py)
**Location**: `agent.py` lines 295-344

**What happens**:
1. Checks completeness (all fields present?) - Score 0-100
2. Checks consistency (decision matches confidence?) - Score 0-100
3. Validates evidence quality (citations provided?)
4. Calculates overall confidence
5. Generates recommendations and next actions

**Output**: Evaluation scores, recommendations, next actions

---

### STEP 7: DELIVER State (agent.py)
**Location**: `agent.py` lines 361-369

**What happens**:
1. Agent state set to DELIVER
2. Returns complete result with:
   - Execution plan
   - Execution log (all step outputs)
   - Final report and JSON

**Output**: Complete result dictionary

---

### STEP 8: Display Results (app.py)
**Location**: `app.py` lines 207-262

**What happens**:
1. Shows decision (PASS/FAIL/NEEDS_INFO) with color coding
2. Displays HTML report in tab
3. Displays JSON output in tab
4. Shows execution details in tab
5. Provides download button for JSON

**Output**: User sees complete results

---

## Data Flow Diagram

```
User Input
    ↓
[INTAKE] → Validate & Store
    ↓
[PLAN] → Create 5 Steps
    ↓
[EXECUTE] → Run Each Step
    ├─ Step 1: Extract Fields
    ├─ Step 2: Get Policy Citations
    ├─ Step 3: Check Compliance
    ├─ Step 4: Evaluate Quality
    └─ Step 5: Generate Report
    ↓
[EVALUATE] → Self-Check Output
    ↓
[DELIVER] → Return Results
    ↓
Display to User
```

---

## Key Functions

### `agent.run()` - Main Entry Point
- Orchestrates entire workflow
- Calls all states in sequence
- Returns final result

### `intake()` - Input Validation
- Validates all inputs
- Stores policy
- Analyzes CSV if provided

### `create_plan()` - Planning
- Generates execution plan
- Uses AI if available, else template

### `execute_step()` - Step Execution
- Runs individual step
- Calls appropriate tool
- Logs output

### `evaluate()` - Quality Check
- Self-validates output
- Calculates confidence
- Provides recommendations

---

## Tools Used

1. **Data Tool**: Analyzes CSV files
2. **Policy Tool**: Retrieves policy citations
3. **Writer Tool**: Generates reports and JSON
4. **Invoice Approval**: Extracts fields and checks compliance

---

## Error Handling

- Missing inputs → Returns NEEDS_INFO
- API failures → Falls back to templates
- Step errors → Logged in execution log
- All errors → Caught and displayed to user
