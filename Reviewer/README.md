# AI Document Reviewer

AI-powered document review system that analyzes contracts, policies, agreements, and other business documents and produces both a structured JSON output and a human-readable Markdown report.

The system supports documents of any length through a chunking and map-reduce pipeline, validates all LLM outputs using Pydantic, and includes batch processing, retry logic, and cost tracking.

---

# Business Value

Manual review of contracts and policy documents is repetitive, time-consuming, and error-prone.

This project reduces a typical first-pass review from approximately:

**30 minutes → 30 seconds**

by automatically extracting:

* Executive summaries
* Key dates
* Parties involved
* Commercial values
* Potentially risky clauses
* Document classification

The output is designed to be useful for legal, operations, procurement, compliance, and business teams.

---

# Features

## Document Support

* PDF documents via `pypdf`
* Plain text (`.txt`) documents

## Long Document Handling

* Automatic chunking
* Configurable overlap
* Map-reduce summarization pipeline
* Works on both short and long documents

## Structured Extraction

Extracts:

* Summary
* TL;DR bullets
* Document type
* Parties
* Key dates
* Contract value
* Flagged clauses
* Confidence score

## Reliability

* Pydantic validation
* Automatic retry on malformed model outputs
* Defensive JSON handling
* Batch processing continues even if one document fails

## Reporting

Generates:

* `review.json`
* `review.md`

## Observability

Tracks:

* Estimated input tokens
* Estimated output tokens
* Estimated cost per document
* Batch summary statistics

---

# Architecture

```text
PDF / TXT
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Map Phase
(Chunk Analysis)
    │
    ▼
Reduce Phase
(Final Review)
    │
    ▼
Pydantic Validation
    │
    ▼
JSON Report
    │
    ▼
Markdown Report
```

---

# Project Structure

```text
Reviewer/

├── README.md
├── requirements.txt
├── .env

├── sample_docs/
│   ├── nda.txt
│   ├── msa.txt
│   ├── policy.txt

├── results/

├── reviewer/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── extract.py
│   ├── chunk.py
│   ├── pipeline.py
│   ├── prompts.py
│   ├── llm.py
│   ├── report.py
│   ├── models.py
│   ├── utils.py
│   ├── state.py
│   ├── metrics.py
│   └── cost_tracker.py
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/BhaumikLuhar/mini-AI-projects.git
cd Reviewer
```

## Create Virtual Environment

```bash
python -m venv .venv
```

### Linux / Mac

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file.

```env
GITHUB_TOKEN=your_token_here
MODEL_NAME=openai/gpt-4.1-mini
```

Update values according to the provider and model you are using.

---

# Usage

## Review Single Document

```bash
python -m reviewer.main contract.pdf
```

or

```bash
python -m reviewer.main contract.txt
```

Outputs:

```text
results/

contract.json
contract.md
```

---

## Batch Processing

Process all supported documents in a folder.

```bash
python -m reviewer.main contracts --batch
```

Example:

```text
contracts/
├── nda.txt
├── msa.txt
├── policy.txt
├── vendor_agreement.pdf
```

Results:

```text
results/
├── nda.json
├── nda.md
├── msa.json
├── msa.md
├── policy.json
├── policy.md
```

---

# Example JSON Output

```json
{
  "summary": "This is a Non-Disclosure Agreement (NDA) between Acme Technologies Pvt Ltd and Bright Solutions LLP, establishing confidentiality and liability terms for proprietary information with a 24-month initial term and automatic renewal unless terminated with written notice.",
  "tldr": [
    "NDA between Acme Technologies Pvt Ltd and Bright Solutions LLP.",
    "24-month term with automatic 12-month renewals unless terminated in writing.",
    "Strict confidentiality and liability clauses for unauthorized disclosure."
  ],
  "document_type": "NDA",
  "parties": [
    {
      "name": "Acme Technologies Pvt Ltd",
      "role": "Disclosing Party"
    },
    {
      "name": "Bright Solutions LLP",
      "role": "Receiving Party"
    }
  ],
  "key_dates": [
    {
      "label": "Effective Date",
      "date": "2026-01-15"
    },
    {
      "label": "Signed Date",
      "date": "2026-01-15"
    }
  ],
  "value_inr": null,
  "flagged_clauses": [
    {
      "clause_type": "Confidentiality Obligation",
      "excerpt": "The Receiving Party agrees to keep confidential all proprietary information disclosed under this Agreement.",
      "concern": "Ensures proprietary information remains confidential.",
      "severity": "high"
    },
    {
      "clause_type": "Non-Disclosure Requirement",
      "excerpt": "The Receiving Party shall not disclose confidential information to any third party without prior written consent.",
      "concern": "Prevents unauthorized third-party disclosures.",
      "severity": "high"
    },
    {
      "clause_type": "Term",
      "excerpt": "This Agreement shall remain in effect for 24 months from the Effective Date.",
      "concern": "Defines the agreement duration.",
      "severity": "medium"
    },
    {
      "clause_type": "Automatic Renewal",
      "excerpt": "This Agreement shall automatically renew for successive 12-month periods unless terminated in writing at least 30 days before expiration.",
      "concern": "Agreement continues unless timely termination notice is given.",
      "severity": "medium"
    },
    {
      "clause_type": "Liability",
      "excerpt": "The Receiving Party shall be liable for damages resulting from unauthorized disclosure.",
      "concern": "Holds Receiving Party responsible for harm caused by violation.",
      "severity": "high"
    }
  ],
  "confidence": 1
}
```

---

# Example Markdown Report

```text
# Document Review

## Summary

This is a Non-Disclosure Agreement (NDA) between Acme Technologies Pvt Ltd and Bright Solutions LLP, establishing confidentiality and liability terms for proprietary information with a 24-month initial term and automatic renewal unless terminated with written notice.

- NDA between Acme Technologies Pvt Ltd and Bright Solutions LLP.
- 24-month term with automatic 12-month renewals unless terminated in writing.
- Strict confidentiality and liability clauses for unauthorized disclosure.


## Document Type

NDA

## Parties

- Acme Technologies Pvt Ltd (Disclosing Party)
- Bright Solutions LLP (Receiving Party)


## Key Dates

- Effective Date: 2026-01-15
- Signed Date: 2026-01-15


## Value

None


## Flagged Clauses

### Confidentiality Obligation
- Severity: high
- Concern: Ensures proprietary information remains confidential.
- Excerpt: The Receiving Party agrees to keep confidential all proprietary information disclosed under this Agreement.

### Non-Disclosure Requirement
- Severity: high
- Concern: Prevents unauthorized third-party disclosures.
- Excerpt: The Receiving Party shall not disclose confidential information to any third party without prior written consent.

### Term
- Severity: medium
- Concern: Defines the agreement duration.
- Excerpt: This Agreement shall remain in effect for 24 months from the Effective Date.

### Automatic Renewal
- Severity: medium
- Concern: Agreement continues unless timely termination notice is given.
- Excerpt: This Agreement shall automatically renew for successive 12-month periods unless terminated in writing at least 30 days before expiration.

### Liability
- Severity: high
- Concern: Holds Receiving Party responsible for harm caused by violation.
- Excerpt: The Receiving Party shall be liable for damages resulting from unauthorized disclosure.



## Confidence

100%
```

---

# Cost Tracking

The system estimates:

* Input tokens
* Output tokens
* Total tokens
* Estimated document cost

Example:

```text
====================================================

DOCUMENT SUMMARY

====================================================

nda.txt

Input Tokens: 2,143
Output Tokens: 312

Cost: $0.0025

====================================================

TOTAL

====================================================

Documents: 5

Input Tokens: 12,321

Output Tokens: 1,744

Cost: $0.0141
```

---

# Error Handling

The system includes:

* JSON cleanup
* Pydantic validation
* Automatic retries
* Batch fault isolation
* Rate-limit handling

If one document fails, remaining documents continue processing.

---

# Technical Highlights

## Chunking

Large documents are split into manageable chunks.

Benefits:

* Lower token usage
* Better extraction quality
* Support for long documents

## Map-Reduce

### Map Phase

Each chunk is independently analyzed.

### Reduce Phase

Chunk findings are combined into a final review.

## Validation Layer

All model outputs are validated using Pydantic before entering the application.

Benefits:

* Strong typing
* Safer downstream processing
* Clear validation errors

---

# Acceptance Criteria

* PDF support
* TXT support
* Long-document support
* Chunking
* Map-reduce processing
* Pydantic validation
* Retry mechanism
* JSON report generation
* Markdown report generation
* Batch processing
* Cost tracking

---

# Future Improvements

## Streamlit UI

Upload documents through a browser interface.

## Industry Templates

Custom clause detection for:

* SaaS contracts
* Vendor agreements
* Employment contracts
* Procurement documents

## Evaluation Framework

Compare extracted clauses against manually annotated datasets.

Measure:

* Precision
* Recall
* F1 Score

## Structured Model Outputs

Adopt provider-native structured outputs to further reduce validation failures.

---

# Disclaimer

This tool provides AI-assisted document review and is intended for informational and operational support purposes only.

It does not constitute legal advice.

Human review is recommended before making legal, contractual, compliance, or commercial decisions.

---