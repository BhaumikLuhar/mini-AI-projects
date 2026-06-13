# Sales Ops Assistant

## Business Problem

Sales teams often spend significant time gathering information before responding to a lead inquiry.

A typical workflow requires:

- Looking up customer history in a CRM
- Checking product availability
- Identifying suitable products
- Calculating pricing and discounts
- Drafting a follow-up email

This process can take 10–15 minutes per lead and usually requires switching between multiple systems.

---

## Solution

Sales Ops Assistant is an AI-powered multi-tool agent that automates lead triage and quote preparation through a single conversational interface.

The agent can:

1. Look up lead history
2. Discover relevant products
3. Check inventory availability
4. Calculate pricing and discounts
5. Search the web for additional information
6. Draft professional follow-up emails

All within a single conversation.

---

## Business Impact

| Metric | Traditional Workflow | Sales Ops Assistant |
|----------|----------|----------|
| Lead Response Preparation | 10–15 minutes | ~90 seconds |
| Systems Accessed | 3–5 systems | 1 interface |
| Manual Copy/Paste | High | Minimal |
| Pricing Errors | Possible | Reduced |
| Follow-up Consistency | Varies by rep | Standardized |

---

# Example Workflow

### User Request

```text
Help me follow up with priya@example.com about laptop bulk pricing
```

### Agent Workflow

```text
CRM Lookup
↓
Product Discovery
↓
Inventory Check
↓
Quote Calculation
↓
Email Draft Generation
```

### Agent Response

The agent provides:

- Lead information
- Product availability
- Pricing estimate
- Draft follow-up email

---

# Features

## Multi-Tool Agent

The assistant supports multiple business tools:

### CRM Lookup

Retrieve lead history using email.

Example:

```text
crm_lookup(email)
```

Returns:

```json
{
  "name": "Priya Shah",
  "company": "Acme Corp",
  "last_contact": "2025-12-01"
}
```

---

### Product Discovery

Find products by keyword.

Example:

```text
find_product("laptop")
```

Returns matching inventory products.

---

### Inventory Lookup

Check inventory availability.

Example:

```text
check_inventory("LAPTOP001")
```

Returns:

- Quantity available
- Unit price
- Product details

---

### Quote Calculation

Calculate pricing using quantity and discount tiers.

Example:

```text
calculate_quote(items, discount_tier)
```

Returns:

- Subtotal
- Discount
- Final quote

---

### Web Search

Retrieve external information using a search API.

Example:

```text
web_search(query)
```

---

### Email Drafting

Generate professional follow-up emails.

Example:

```text
draft_email(context)
```

Important:

The agent NEVER sends emails.

It only creates drafts for human review.

---

# Safety Features

The project includes multiple safety controls.

## Iteration Cap

Maximum:

```text
10 tool iterations
```

Prevents infinite loops and runaway costs.

---

## Session Cost Cap

Maximum:

```text
₹20 per session
```

Prevents excessive API usage.

---

## Pydantic Validation

Every tool input is validated before execution.

Examples:

- Invalid email formats
- Missing required fields
- Incorrect data types

are rejected safely.

---

## Email Approval Gate

The email tool never sends messages automatically.

Instead it returns:

```text
DRAFT: ...
Requires human approval.
```

---

## File Access Restrictions

File operations are restricted through allowlist validation.

Path traversal attempts such as:

```text
../../etc/passwd
```

are blocked.

---

# Architecture

```text
User
 │
 ▼
Streamlit Chat Interface
 │
 ▼
Conversation Memory
 │
 ▼
OpenAI Agent
 │
 ▼
Agent Loop
 │
 ▼
Safety Layer
 │
 ├── Iteration Cap
 │
 ├── Cost Cap
 │
 └── Input Validation
 │
 ▼
Tool Executor
 │
 ├── CRM Lookup
 │
 ├── Product Discovery
 │
 ├── Inventory Lookup
 │
 ├── Quote Calculator
 │
 ├── Web Search
 │
 └── Email Drafting
 │
 ▼
Response Generation
 │
 ▼
User
```

---

# Project Structure

```text
sales-ops-agent/
│
├── .streamlit/
│
├── agent/
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── catalog.py
│   │   ├── crm.py
│   │   ├── init.py
│   │   ├── email_drafter.py
│   │   ├── find_product.py
│   │   ├── inventory.py
│   │   ├── pricing.py
│   │   └── search.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── executor.py
│   ├── logging_utils.py
│   ├── loop.py
│   ├── memory.py
│   ├── safety.py
│   ├── schemas.py
│   ├── tool_definitions.py
│   ├── tool_registry.py
│   └── validation.py
│
├── data/
│   ├── inventory.db
│   └── leads.json
│
├── logs/
│
├── tests/
│
├── app.py
└── README.md
```

---

# Technologies Used

## Backend

- Python 3.11+
- OpenAI API
- SQLite
- Pydantic

## Frontend

- Streamlit

## Data Storage

- SQLite Database
- JSON Files

## Agent Components

- OpenAI Function Calling
- Tool Execution Layer
- Validation Layer
- Safety Layer
- Audit Logging

---

# Conversation Memory

The assistant maintains conversation history during a session using Streamlit session state.

Benefits:

- Follow-up questions work naturally
- Less repetitive user input
- Better context awareness

Example:

```text
User:
Who is priya@example.com?

Assistant:
Lead from Acme Corp.

User:
Draft a follow-up email.

Assistant:
Uses previous context automatically.
```

---

# Tool Visibility

All tool executions are visible within the Streamlit interface.

For each tool call users can inspect:

- Tool name
- Inputs
- Outputs

This improves transparency and debugging.

---

# Audit Logging

Every tool execution is logged to JSONL files.

Example information captured:

```json
{
  "timestamp": "...",
  "tool_name": "crm_lookup",
  "input": {
    "email": "priya@example.com"
  },
  "output": {
    "success": true
  }
}
```

This provides traceability and debugging support.

---

# Evaluation Scenarios

The project includes test scenarios covering common business workflows.

Examples:

### CRM Lookup

```text
Tell me about priya@example.com
```

Expected Tool:

```text
crm_lookup
```

---

### Inventory Check

```text
Do we have LAPTOP001 in stock?
```

Expected Tool:

```text
check_inventory
```

---

### Bulk Pricing

```text
Need pricing for 20 laptops
```

Expected Tools:

```text
find_product
calculate_quote
```

---

### End-to-End Workflow

```text
Help me follow up with priya@example.com about laptop bulk pricing
```

Expected Tool Sequence:

```text
crm_lookup
↓
find_product
↓
check_inventory
↓
calculate_quote
↓
draft_email
```

---

# Future Improvements

Potential enhancements include:

- Real CRM integration (HubSpot API)
- Real inventory management system
- Email approval workflow
- Email sending integration
- Feedback collection system
- Automated evaluation dashboard
- Multi-user support
- Analytics and reporting
- LangSmith observability
- Tool schema generation from Pydantic models

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/BhaumikLuhar/mini-AI-projects.git
cd sales-ops-agent
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment Variables

Create a `.env` file:

```env
GITHUB_API_KEY=your_api_key_here
TAVILY_API_KEY=your_brave_api_key_here
```

---

## Run Application

```bash
streamlit run app.py
```

Application will be available locally at:

```text
http://localhost:8501
```

---

# Learning Outcomes

This project demonstrates practical implementation of:

- Agentic AI workflows
- OpenAI function calling
- Multi-tool orchestration
- Pydantic validation
- Session memory
- Safety controls
- Cost management
- Audit logging
- Streamlit application development
- Production-oriented software architecture

---

# License

This project is intended for educational and portfolio purposes.