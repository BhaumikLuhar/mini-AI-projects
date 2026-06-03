# Anya for AcmeCo

AI-powered customer support assistant for a refurbished laptop retailer.

Anya handles routine customer support questions, maintains conversation history, streams responses in real time, tracks operational costs, logs every interaction, and escalates sensitive conversations to human agents when required.

---

## Business Value

AcmeCo currently receives approximately 800 customer support tickets per day.

Typical support cost:

- 800 tickets/day
- ₹15 average human handling cost per ticket

Current monthly support cost:

- 800 × ₹15 × 30
- ≈ ₹360,000/month

If Anya successfully handles 50% of support requests without human intervention:

- 400 tickets/day deflected
- ~12,000 tickets/month

Estimated AI operating cost:

- ~₹10,000/month (depending on model and usage)

Estimated monthly savings:

- ~₹170,000–₹350,000/month

In addition to cost reduction, Anya provides:

- 24/7 support availability
- Consistent responses
- Full conversation audit logs
- Escalation workflows
- Cost visibility

---

# Features

## Customer Support Persona

Persona definitions are stored as text files.

Non-engineering teams can modify:

- Tone
- Scope
- Escalation behavior
- Allowed topics

without changing code.

Example:

```text
personas/anya.txt
personas/agent.txt
```

---

## Streaming Responses

Responses stream token-by-token.

Benefits:

- Faster perceived response time
- Better user experience
- Reduced waiting frustration

---

## Conversation Memory

Maintains conversation history across turns.

Example:

User:

```text
My name is John.
```

Later:

```text
What is my name?
```

Anya remembers previous context.

---

## Context Window Management

Automatic history trimming prevents context-window overflow.

When conversation size exceeds the configured token budget:

- Oldest messages are removed
- System prompt is preserved
- Recent context remains available

---

## Escalation System

Supports configurable escalation rules.

Triggers include:

- Legal threats
- Refund disputes
- Abusive language
- Low-confidence AI responses

Example:

```text
I want to sue your company.
```

Results in:

```text
Escalated for human review.
```

---

## Cost Tracking

Tracks:

- Estimated input tokens
- Estimated output tokens
- Estimated API cost

Displayed throughout the session and summarized at exit.

Example:

```text
Messages: 12
Tokens: 4,812
Cost: ₹1.43
```

---

## Audit Logging

Every interaction is stored as JSONL.

Captured fields:

- Timestamp
- User message
- Assistant reply
- Escalation status
- Token counts

Example log location:

```text
logs/2026-06-01-103015.jsonl
```

---

## Evaluation Framework

Automated evaluation suite verifies expected behavior.

Examples:

- Return policy questions
- Warranty questions
- Order status requests
- Off-topic requests

Results:

```text
PASS  Return Policy
PASS  Warranty
PASS  Poem Redirect
```

---

# Architecture

```text
User
 │
 ▼
Command Router
 │
 ├── /reset
 ├── /save
 ├── /load
 ├── /persona
 └── /agent
 │
 ▼
Chat Session
 │
 ▼
Escalation Layer
 │
 ├── Keyword Rules
 ├── Abuse Detection
 └── Confidence Review
 │
 ▼
LLM Client
 │
 ▼
Streaming Response
 │
 ▼
Logging + Cost Tracking
```

---

# Project Structure

```text
AI-Assistant/
│
├── .env
├── requirements.txt
├── README.md
│
├── personas/
│   ├── anya.txt
│   └── agent.txt
│
├── logs/
│
├── tests/
│   └── eval_questions.json
│
└── anya/
    ├── __init__.py
    ├── main.py
    ├── chat.py
    ├── client.py
    ├── Commands.py
    ├── persona.py
    ├── escalation.py
    ├── logging_utils.py
    ├── pricing.py
    ├── session_stats.py
    ├── run_eval.py
    └── evaluator.py
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/BhaumikLuhar/mini-AI-projects.git
cd AI-Assistant
```

---

## Create Virtual Environment

### Linux / Mac

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create:

```text
.env
```

Example:

```env
GROQ_API_KEY=your_key_here
```

Never commit secrets to Git.

---

# Running the Application

```bash
python -m anya.main
```

---

# Available Commands

## Reset Conversation

```text
/reset
```

Clears conversation history.

---

## Save Conversation

```text
/save
```

Stores chat transcript as JSON.

---

## Load Conversation

```text
/load filename.json
```

Restores a previous conversation.

---

## Change Persona

```text
/persona anya
```

Switches to selected persona.

---

## Agent Mode

```text
/agent
```

Switches to the cautious support-agent persona.

---

## Exit

```text
/quit
```

Ends session and displays summary.

---

# Example Session

```text
You: Where is my order?

Anya:
I'd be happy to help.
Please provide your order number.

[Messages: 2 | Tokens: 143 | Cost: ₹0.03]
```

---

# Evaluation

Run automated tests:

```bash
python run_eval.py
```

Example:

```text
PASS  Return Policy
PASS  Warranty
PASS  Order Status
PASS  Poem Redirect

Passed: 4/4
Accuracy: 100%
```

---

# Future Improvements

Planned enhancements:

- Web UI
- Multi-agent routing
- RAG knowledge base
- Human handoff dashboard
- Ticket creation integration
- Vector database memory
- Conversation summarization
- Analytics dashboard

---

# Key Technical Concepts Demonstrated

- LLM API Integration
- Prompt Engineering
- Persona Design
- Streaming Responses
- Conversation State Management
- Context Window Management
- Escalation Workflows
- Cost Tracking
- Audit Logging
- Automated Evaluations

---

# License

Educational project built as part of an Agentic AI and Automation learning program.