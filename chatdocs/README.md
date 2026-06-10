# ChatDocs AI – Enterprise RAG Knowledge Assistant

## Overview

ChatDocs AI is a Retrieval-Augmented Generation (RAG) assistant that allows users to chat with a collection of company documents including PDFs and Word documents.

The system indexes organizational knowledge, performs semantic and keyword-based retrieval, re-ranks relevant content, and generates grounded answers with source citations.

Instead of manually searching through hundreds of pages of documentation, employees can ask natural language questions and receive answers backed by the original documents.

---

## Business Value

Organizations store critical information across:

* Employee handbooks
* HR policies
* Technical documentation
* SOPs
* Compliance documents
* Annual reports
* Internal knowledge bases

Finding information often requires significant manual effort.

ChatDocs AI transforms static documents into a searchable conversational knowledge assistant that:

* Reduces time spent searching for information
* Improves knowledge accessibility
* Provides source-backed answers
* Minimizes duplicate questions to support teams
* Enables self-service information retrieval

---

## Features

### Document Ingestion

Supports indexing:

* PDF documents (`.pdf`)
* Microsoft Word documents (`.docx`)

Text is automatically extracted and prepared for retrieval.

---

### Intelligent Chunking

Documents are split into manageable chunks using:

* Recursive character splitting
* Chunk overlap preservation
* Metadata retention

Each chunk stores:

* Source filename
* Page number
* Chunk index

---

### Semantic Search

Uses Sentence Transformers embeddings:

```text
all-MiniLM-L6-v2
```

to understand semantic meaning rather than relying only on keyword matches.

Example:

```text
"remote work"

≈

"work from home"
```

---

### Chroma Vector Database

Stores:

* Embeddings
* Document chunks
* Metadata

using a persistent ChromaDB collection.

Benefits:

* Fast retrieval
* Local storage
* Survives application restarts
* Scales to thousands of document chunks

---

### Incremental Indexing

Re-indexing only processes files that changed.

Uses:

* File modification timestamps
* Content hashes

Benefits:

* Faster indexing
* Lower embedding costs
* Efficient updates

---

### Hybrid Retrieval

Combines:

#### Dense Retrieval

Embedding similarity via ChromaDB.

#### Sparse Retrieval

BM25 keyword search.

Implemented using:

```text
rank-bm25
```

Hybrid retrieval improves performance on:

* Acronyms
* Policy IDs
* Version numbers
* Exact terminology
* Semantic questions

---

### LLM Re-ranking

Retrieval pipeline:

```text
Question
    ↓
Hybrid Retrieval
    ↓
Top 20 Chunks
    ↓
LLM Re-ranker
    ↓
Best 5 Chunks
```

The re-ranker improves context quality before answer generation, reducing retrieval noise and increasing citation accuracy.

---

### Source Citations

Every answer includes document references.

Example:

```text
Employees may carry over up to 40 hours of PTO.

Source:
employee_handbook.pdf (Page 12)
```

This enables answer verification and improves trustworthiness.

---

### Hallucination Prevention

The assistant is instructed to answer only using retrieved document context.

If information is unavailable:

```text
I don't see that in our documents.
```

This prevents unsupported or fabricated responses.

---

### Conversation Memory

The chat assistant maintains conversation history while retrieving fresh context for every new question.

Benefits:

* Natural multi-turn conversations
* Context retention
* Improved user experience

---

## System Architecture

```text
Documents
    ↓
Extraction
    ↓
Chunking
    ↓
Embedding
    ↓
ChromaDB
    ↓

User Question
    ↓

Hybrid Retrieval
(Dense + BM25)

    ↓

Top 20 Chunks

    ↓

LLM Re-ranker

    ↓

Best 5 Chunks

    ↓

Prompt Construction

    ↓

LLM Answer

    ↓

Citations
```

---

## Project Structure

```text
chatdocs/

├── .venv/
├── .env
├── README.md
├── requirements.txt

├── docs/
│   └── source documents

├── chroma_data/
│   └── vector database

├── index_state.json

├── evals/
│   ├── qa_pairs.json
│   ├── retrieval_eval.py
│   ├── answer_eval.py
│   ├── hallucination_eval.py
│   └── eval_report.json

├── chatdocs/
│   ├── __init__.py
│   ├── config.py
    ├── constants.py
│   ├── extract.py
│   ├── chunk.py
│   ├── indexer.py
    ├── indexing_state.py
│   ├── retriever.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   ├── rag.py
│   ├── llm.py
    ├── logger.py
    ├── memory.py
    ├── prompts.py
    ├── utils.py
│   └── chat.py

├── index.py
└── chat.py
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/BhaumikLuhar/mini-AI-projects.git
cd chatdocs
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create:

```text
.env
```

Example:

```env
GITHUB_TOKEN=your_token_here

TOP_K=5

DENSE_WEIGHT=0.7
BM25_WEIGHT=0.3

ENABLE_RERANK=true
RERANK_TOP_N=20
FINAL_CONTEXT_K=5
```

---

## Index Documents

Place PDFs and DOCX files inside:

```text
docs/
```

Run:

```bash
python index.py docs/
```

Expected:

```text
Indexing documents...
Embedding chunks...
Saving to ChromaDB...
Done.
```

---

## Start Chat Assistant

```bash
python chat.py
```

Example:

```text
You:
What is the work from home policy?

Assistant:
Employees may work remotely up to three days per week with manager approval.

Source:
employee_handbook.pdf (Page 1)
```

---

## Commands

### Show Indexed Sources

```text
/sources
```

Displays:

* Document names
* Last indexed timestamps

---

### Exit Chat

```text
/exit
```

or

```text
quit
```

---

## Evaluation

The project includes automated evaluation for:

### Retrieval Recall

Measures:

* Recall@1
* Recall@3
* Recall@5

### Answer Accuracy

Verifies:

* Expected keywords
* Grounded responses

### Citation Accuracy

Checks:

* Correct document references
* Correct metadata usage

### Hallucination Resistance

Tests out-of-domain questions and ensures the system refuses unsupported answers.

Run:

```bash
python evals/retrieval_eval.py

python evals/answer_eval.py

python evals/hallucination_eval.py
```

---

## Sample Results

| Metric                   | Score |
| ------------------------ | ----- |
| Recall@1                 | 75%   |
| Recall@3                 | 90%   |
| Recall@5                 | 100%  |
| Answer Accuracy          | 90%   |
| Citation Accuracy        | 95%   |
| Hallucination Resistance | 100%  |

---

## Technologies Used

### AI / NLP

* Sentence Transformers
* all-MiniLM-L6-v2
* Retrieval-Augmented Generation (RAG)

### Vector Database

* ChromaDB

### Retrieval

* Dense Retrieval
* BM25
* Hybrid Search

### Re-ranking

* LLM-based Context Selection

### Document Processing

* pypdf
* python-docx

### Python Ecosystem

* numpy
* rank-bm25
* python-dotenv

---

## Future Improvements

* Streamlit Web Interface
* Authentication & User Roles
* Multi-user Chat Sessions
* Hybrid Retrieval Weight Tuning
* Advanced Re-ranking Models
* Evaluation Dashboard
* Document Upload UI
* OCR Support for Scanned PDFs
* Distributed Vector Storage

---

## Key Learnings

This project demonstrates the complete lifecycle of building a production-style Retrieval-Augmented Generation system:

* Document ingestion
* Chunking strategies
* Embeddings
* Vector databases
* Hybrid retrieval
* Re-ranking
* Prompt engineering
* Citation grounding
* Hallucination prevention
* Retrieval evaluation

The architecture closely mirrors internal enterprise knowledge assistants used to search organizational documentation at scale.
