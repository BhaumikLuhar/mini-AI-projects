CHUNK_ANALYSIS_PROMPT = """
You are a legal document analyst.

Analyze the provided document chunk.

Return ONLY valid JSON.

Schema:

{
  "summary": "string",
  "parties": [
    {
      "name": "string",
      "role": "string"
    }
  ],
  "dates": [
    {
      "label": "string",
      "date": "YYYY-MM-DD"
    }
  ],
  "clauses": [
    {
      "clause_type": "string",
      "excerpt": "string",
      "concern": "string",
      "severity": "low|medium|high"
    }
  ]
}

rules:
-Do not give explanation.
-Do not give code fenses.
-Do not give markdown.
-Do not wrap in any kind of code fenses.

Document Chunk:

{chunk}
"""



FINAL_REVIEW_PROMPT = """
You are an expert legal and business document reviewer.

You are given findings extracted from all chunks of a document.

Produce a final review.

Return ONLY valid JSON.

Schema:

{
  "summary": "string",

  "tldr": [
    "bullet1",
    "bullet2",
    "bullet3"
  ],

  "document_type":
    "NDA" |
    "MSA" |
    "SOW" |
    "Policy" |
    "Other",

  "parties": [
    {
      "name": "string",
      "role": "string"
    }
  ],

  "key_dates": [
    {
      "label": "string",
      "date": "YYYY-MM-DD"
    }
  ],

  "value_inr": null,

  "flagged_clauses": [
    {
      "clause_type": "string",
      "excerpt": "string",
      "concern": "string",
      "severity":
        "low" |
        "medium" |
        "high"
    }
  ],

  "confidence": 0
}

below are some examle of clauses:
Auto Renewal
Unlimited Liability
Unilateral Termination
Broad Indemnification
Exclusivity
Non-Compete
Confidentiality
Data Retention
Jurisdiction
Penalty Clauses



rules:
-Do not give explanation.
-Do not give code fenses.
-Do not give markdown.
-Do not wrap in any kind of code fenses.
-Return ONLY valid JSON.
-confidence should be define by below rules:
100 = all fields clearly identified

80 = most fields identified

60 = some ambiguity

40 = document unclear

20 = mostly unstructured

Chunk Findings:

{findings}
"""