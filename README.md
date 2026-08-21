# Nexus AI

### Evidence-Driven AI Investigation & Root-Cause Reasoning

> **Don't just answer the question. Investigate it.**

Nexus AI is an AI-native investigation platform designed to analyze business questions by decomposing them into structured investigation tasks, examining available evidence, validating the original claim, evaluating potential root causes, and synthesizing the findings into an evidence-grounded report.

Unlike a conventional question-answering workflow, Nexus does not automatically assume that the premise of a question is correct.

For example:

> **"Why did customer churn increase by 18% this quarter?"**

Rather than accepting the 18% increase as fact, Nexus first checks the evidence.

In one investigation:

Claimed increase:   18.0%
Observed increase:  22.12%


The discrepancy is surfaced before the system proceeds with the investigation.

The goal is simple:

> **Evidence should matter more than assumptions.**

---

## Why Nexus?

Many AI systems follow this pattern:

```text
Question
   ↓
LLM
   ↓
Answer
```

This works well for general question answering, but analytical investigations often require something different.

Business questions can contain:

* Incorrect assumptions
* Incomplete information
* Misleading statistics
* Correlations presented as causes
* Claims that are not supported by the underlying evidence

Nexus therefore follows an investigation-oriented workflow:

```text
Business Question
       ↓
Investigation Planning
       ↓
Evidence Analysis
       ↓
Claim Validation
       ↓
Root-Cause Evaluation
       ↓
Evidence Synthesis
       ↓
Investigation Report
```

The system is designed not only to produce an explanation, but also to determine whether that explanation is supported by the available evidence.

---

# Core Capabilities

## 1. Investigation Planning

Nexus decomposes a high-level business question into structured investigation tasks.

Example:

```text
Business Question
       ↓
What changed?
       ↓
Which segments changed?
       ↓
When did the change occur?
       ↓
What product or behavioral factors are associated?
       ↓
Does the original claim hold?
```

---

## 2. Evidence Analysis

The investigation workers analyze the available data and produce structured findings rather than relying exclusively on free-form LLM generation.

Findings can include:

* Observed rates
* Segment differences
* Temporal patterns
* Product-related changes
* Satisfaction relationships
* Supporting evidence
* Confidence estimates

---

## 3. Claim Validation

Nexus explicitly evaluates whether the original claim is supported by the evidence.

For example:

```text
Original claim
18.0% increase

Observed
22.12% increase

Assessment
Claim does not exactly match observed data
```

This prevents the investigation from blindly inheriting assumptions from the original question.

---

## 4. Root-Cause Analysis

Nexus evaluates potential drivers of the observed outcome.

Importantly, the system distinguishes between:

```text
Observed association
        ≠
Proven causation
```

Potential root causes are therefore presented with supporting evidence, confidence, and causal limitations.

---

## 5. Evidence-Grounded Synthesis

The final investigation combines:

* Investigation tasks
* Individual findings
* Claim assessment
* Root-cause candidates
* Confidence
* Limitations

into a structured report.

---

## 6. Investigation Persistence

Every investigation is persisted in PostgreSQL.

This allows Nexus to maintain investigation history and retrieve previously completed investigations.

Example:

```text
POST /investigations
        ↓
Investigation created
        ↓
Investigation executed
        ↓
Result serialized
        ↓
PostgreSQL
        ↓
GET /investigations/{id}
```

The UI also provides access to recent investigations.

---

# Agentic Investigation Architecture

Nexus uses specialized reasoning stages rather than treating the entire investigation as a single LLM call.

```text
                    ┌──────────────────────┐
                    │   Business Question  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Investigation Planner│
                    │       Agent          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Investigation      │
                    │       Workers        │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
             Temporal      Satisfaction   Product
              Analysis       Analysis      Analysis
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Claim Validation   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Root-Cause         │
                    │     Analysis         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Aggregation &     │
                    │      Synthesis       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Investigation Report │
                    └──────────────────────┘
```

The architecture separates analytical responsibilities so individual reasoning components can be developed and evaluated independently.

---

# Technical Architecture

```text
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      API Layer      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Investigation       │
                    │ Service             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Investigation Graph │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
         Planning          Analysis          Validation
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                       Root-Cause Analysis
                               │
                               ▼
                           Synthesis
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PostgreSQL       │
                    │   Investigation DB  │
                    └─────────────────────┘
```

---

# Technology Stack

## Application

* **Python**
* **FastAPI**
* **Streamlit**
* **Pydantic**

## AI / Reasoning

* **LangChain**
* **Ollama**
* **Qwen3 8B**
* Structured investigation graph
* Specialized reasoning workers

## Data / Persistence

* **PostgreSQL**
* **SQLAlchemy**

## Architecture

* Modular Python package structure
* REST API
* Persistent investigation state
* Structured serialization
* Investigation graph orchestration

---

# Project Structure

```text
nexus-ai/
│
├── apps/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── investigations.py
│   │   └── services/
│   │       └── investigations.py
│   │
│   └── ui/
│       ├── app.py
│       └── config.py
│
├── nexus_core/
│   │
│   ├── analysis/
│   │   ├── churn.py
│   │   ├── product_changes.py
│   │   ├── router.py
│   │   ├── satisfaction.py
│   │   └── temporal.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── config.py
│   │   └── session.py
│   │
│   ├── investigation/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   └── serialization.py
│   │
│   ├── reasoning/
│   │   ├── aggregator.py
│   │   ├── claim_validation.py
│   │   ├── evidence.py
│   │   ├── executor.py
│   │   ├── graph.py
│   │   ├── planner.py
│   │   ├── report.py
│   │   ├── root_cause.py
│   │   ├── router.py
│   │   ├── state.py
│   │   ├── synthesis.py
│   │   └── workers.py
│   │
│   └── llm.py
│
├── pyproject.toml
└── README.md
```

---

# API

Nexus exposes a FastAPI backend.

### Health

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "Nexus AI",
  "version": "0.1.0"
}
```

### Create Investigation

```http
POST /investigations
```

Example:

```json
{
  "question": "Why did customer churn increase this quarter?",
  "priority": "high"
}
```

### List Investigations

```http
GET /investigations
```

Returns recent persisted investigations.

### Retrieve Investigation

```http
GET /investigations/{investigation_id}
```

Returns the persisted investigation and its generated result.

---

# Running Locally

## Prerequisites

You will need:

* Python 3.14+
* `uv`
* PostgreSQL
* Ollama
* Qwen3 8B

---

## 1. Clone the repository

```bash
git clone <your-private-repository>
cd nexus-ai
```

> The repository is currently private.

---

## 2. Install dependencies

```bash
uv sync
```

---

## 3. Install and run Ollama

Install Ollama and pull the model:

```bash
ollama pull qwen3:8b
```

Verify that the model is available:

```bash
ollama list
```

---

## 4. Configure the database

Configure the PostgreSQL connection using your environment configuration.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/nexus
```

Do not commit credentials or environment files to the repository.

---

## 5. Start the API

```bash
uv run uvicorn apps.api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 6. Start the UI

In another terminal:

```bash
uv run streamlit run apps/ui/app.py
```

The Nexus interface will open in your browser.

---

# Example Investigation

### Input

```text
Why did customer churn increase this quarter?
```

### Investigation

Nexus decomposes the question and analyzes available evidence.

### Claim validation

```text
Claimed:
18.0%

Observed:
22.12%
```

### Findings

The investigation can surface patterns across:

* Customer satisfaction
* Customer segments
* Product changes
* Time periods

### Root-cause analysis

Potential drivers are evaluated using observed evidence and confidence.

### Final report

The final result contains:

```text
Investigation Tasks
        +
Findings
        +
Claim Assessment
        +
Root-Cause Analysis
        +
Conclusion
        +
Limitations
```

---

# Responsible Reasoning

Nexus intentionally avoids presenting statistical association as proven causality.

For example:

```text
Segment A has higher churn
            ↓
       Association
            ≠
         Causation
```

The system therefore reports limitations when the evidence does not support a causal conclusion.

This is an important design principle:

> **A useful AI system should communicate uncertainty instead of hiding it.**

---

# Current Status

### Working

* [x] Investigation planning
* [x] Investigation graph
* [x] Analysis workers
* [x] Evidence aggregation
* [x] Claim validation
* [x] Root-cause analysis
* [x] Report synthesis
* [x] Structured serialization
* [x] Database persistence
* [x] FastAPI API
* [x] Investigation history
* [x] Streamlit UI
* [x] Local Qwen3 8B inference

### In Progress

* [ ] Production LLM deployment
* [ ] Public deployment
* [ ] Automated evaluation suite
* [ ] Expanded observability
* [ ] Robust asynchronous investigation execution
* [ ] Production authentication
* [ ] Investigation lifecycle hardening

---

# Design Philosophy

Nexus is built around three principles:

### 1. Question the premise

The question may be wrong.

### 2. Follow the evidence

The explanation should be grounded in observed evidence.

### 3. Respect uncertainty

The system should clearly communicate what the evidence cannot establish.

In short:

> **Don't just generate an answer. Investigate what the evidence supports.**

---

# Project Vision

The long-term goal of Nexus is to explore a different paradigm for AI-assisted analytical work.

Instead of:

```text
Human → Question → AI → Answer
```

Nexus aims toward:

```text
Human
  ↓
Question
  ↓
Investigation
  ↓
Evidence
  ↓
Validation
  ↓
Reasoning
  ↓
Conclusion
  ↓
Uncertainty
```

The objective isn't to make AI sound more confident.

It's to make AI **more disciplined about what it can actually conclude.**

---

## Author

**Leerish Arvind**

MSc Data Science & Analytics
AI / Machine Learning / Data Science



## License

This project is currently maintained as a private project and is not licensed for redistribution.

The source code is intentionally kept private while the system is being developed.
