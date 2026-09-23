# AegisOps 2.0

## Autonomous IT Incident Resolution Agent

AegisOps 2.0 is a production-oriented agentic AI platform for IT incident triage and controlled incident resolution.

It combines machine-learning classification, hybrid knowledge retrieval, LLM-based reasoning, policy enforcement, role-based access control, prompt-injection detection, human-in-the-loop safeguards, controlled ServiceNow actions, post-action verification, and persistent audit records.

> **Current development configuration:** mock LLM + mock ServiceNow + SQLite.
> The architecture is designed so these components can be replaced with real providers without changing the core agent workflow.

---

## 1. Problem Statement

Traditional IT support workflows often require multiple manual steps:

1. Read and understand the incident.
2. Determine the incident category.
3. Assign priority.
4. Search knowledge-base documentation.
5. Identify a likely resolution.
6. Decide whether an action is safe.
7. Execute the action in the ITSM platform.
8. Verify that the action actually worked.
9. Record the execution and outcome.

AegisOps combines these stages into a controlled agentic workflow while keeping authorization and high-risk automation outside the LLM.

---

## 2. Solution

AegisOps processes an incident through the following workflow:

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
FastAPI
 │
 ├── JWT Authentication
 └── RBAC
 │
 ▼
LangGraph Agent Orchestrator
 │
 ├── Incident Validation
 ├── Prompt-Injection Detection
 ├── ML Classification
 ├── Priority Assessment
 ├── Hybrid RAG
 │    ├── BM25
 │    ├── Dense Retrieval
 │    ├── RRF Fusion
 │    └── Cross-Encoder Reranking
 │
 ├── LLM Reasoning
 ├── Policy / Risk Evaluation
 │
 ├── Human Approval
 │
 └── Controlled ServiceNow Tools
       │
       ▼
   Verification
       │
       ▼
   Final Response
       │
       ▼
   Persistence / Audit
```

---

## 3. Core Architecture

```text
┌───────────────────────────────────────────────┐
│                 Streamlit UI                  │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│                  FastAPI                      │
│       Authentication • RBAC • API Layer      │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│              LangGraph Agent                  │
├───────────────────────────────────────────────┤
│ Validation                                    │
│ Prompt Injection Detection                    │
│ Classification                                │
│ Priority                                      │
│ Hybrid Retrieval                              │
│ Reasoning                                     │
│ Policy / Risk                                 │
│ Human-in-the-Loop                             │
│ Controlled Action                             │
│ Verification                                  │
│ Final Response                                │
└──────────────────────┬────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌────────────────────┐   ┌────────────────────┐
│ Knowledge Base     │   │ ServiceNow         │
│ BM25 + Qdrant      │   │ Controlled Tools   │
└────────────────────┘   └────────────────────┘
                                   │
                                   ▼
                           Verification Layer
                                   │
                                   ▼
                           Audit / Persistence
```

---

## 4. Agent Workflow

### Step 1 — Validation

The incident description is validated before entering the agent workflow.

### Step 2 — Prompt-Injection Detection

User-provided incident text is treated as untrusted input.

The security layer checks for patterns associated with:

* instruction override
* system-prompt extraction
* privilege escalation
* tool manipulation
* attempts to ignore previous instructions

Detected prompt injection can force the workflow into the human-approval path.

### Step 3 — Incident Classification

A supervised machine-learning classifier predicts the incident category.

The final classifier combines:

* Word-level TF-IDF
* Character-level TF-IDF
* Feature Union
* Linear SVM

### Step 4 — Priority Assessment

Incidents are assigned:

```text
P1
P2
P3
```

based on the configured incident-priority rules.

### Step 5 — Hybrid RAG

Knowledge retrieval combines:

```text
BM25 sparse retrieval
        +
Qdrant dense retrieval
        ↓
RRF fusion
        ↓
Cross-encoder reranking
```

This allows lexical and semantic matches to contribute to the final retrieved evidence.

### Step 6 — Reasoning

The reasoning component produces:

* incident summary
* likely root cause
* resolution recommendation
* recommended action
* confidence
* risk level
* human-approval requirement

The current local development configuration uses a mock LLM provider for deterministic execution without paid API access.

### Step 7 — Policy Enforcement

The policy layer evaluates:

* classification confidence
* reasoning confidence
* incident priority
* risk level
* retrieved evidence
* prompt-injection status
* proposed action

The LLM does not directly authorize ServiceNow operations.

### Step 8 — Human-in-the-Loop

High-risk or policy-sensitive operations can be stopped before external execution.

```text
Risky action
    ↓
Human approval required
    ↓
No external action
```

### Step 9 — Controlled ServiceNow Action

Only explicitly supported actions can reach the ServiceNow layer.

Current controlled actions include:

```text
get_incident
create_incident
add_work_note
update_incident
resolve_incident
```

Each action is protected by RBAC.

### Step 10 — Verification

AegisOps follows:

```text
Act → Observe → Verify
```

For example, after resolving an incident, the system retrieves the incident again and verifies the expected state.

### Step 11 — Persistence

Agent runs and policy decisions are persisted for traceability and audit purposes.

---

## 5. Security Model

AegisOps follows a defense-in-depth approach.

### LLM is not an authorization mechanism

The architecture deliberately separates reasoning from authorization:

```text
LLM
 │
 │ proposes
 ▼
Application Policy
 │
 │ validates
 ▼
RBAC
 │
 │ authorizes
 ▼
Controlled Tool
 │
 ▼
ServiceNow
```

### Role-Based Access Control

Roles:

```text
viewer
analyst
operator
admin
```

Action permissions include:

```text
incident:view
incident:create
incident:add_work_note
incident:update
incident:resolve
admin
```

Unauthorized actions are rejected before the ServiceNow client is invoked.

### Prompt Injection Defense

Retrieved documents and incident text are treated as untrusted data rather than executable instructions.

### Human Approval

High-risk actions cannot automatically bypass the policy boundary.

### JWT Authentication

The API uses JWT access tokens with:

* expiration
* signed claims
* username validation
* role validation
* active-user verification

### Secret Handling

Development secrets are stored in `.env` and excluded from Git.

`.env.example` contains placeholders only.

---

## 6. Machine-Learning Classifier

### Dataset

The external IT support dataset contains manually classified IT support tickets.

The processed AegisOps training/test split contains:

```text
Training samples: 1572
Test samples:      530
```

### Model

Final model:

```text
Word TF-IDF
      +
Character TF-IDF
      ↓
Feature Union
      ↓
Linear SVM
```

### Test Results

Measured on the final 530-ticket test set:

| Metric      | Result |
| ----------- | -----: |
| Accuracy    | 81.13% |
| Macro F1    | 76.81% |
| Weighted F1 | 80.73% |

The model is persisted as:

```text
models/incident_classifier_final.joblib
```

---

## 7. Hybrid RAG Evaluation

The local knowledge base is indexed using:

```text
BM25
+
Dense Embeddings
+
Qdrant
+
Reciprocal Rank Fusion
+
Cross-Encoder Reranking
```

The retrieval evaluation achieved:

```text
Recall@1 = 100%
Recall@3 = 100%
Recall@5 = 100%
MRR      = 1.0
```

The evaluation was performed against the project's knowledge-base query set.

---

## 8. Technology Stack

### Backend

```text
Python 3.12
FastAPI
Uvicorn
Pydantic
SQLAlchemy
Alembic
SQLite
Redis
```

### Agentic AI

```text
LangGraph
LLM reasoning layer
Hybrid RAG
Qdrant
BM25
Sentence Transformers
Cross-Encoder Reranking
```

### Machine Learning

```text
scikit-learn
Pandas
NumPy
Joblib
TF-IDF
Linear SVM
```

### Security

```text
JWT
RBAC
Password hashing
Prompt-injection detection
Human-in-the-loop policy
Controlled tool authorization
```

### Frontend

```text
Streamlit
```

### Testing / Quality

```text
Pytest
Integration tests
Unit tests
RAG evaluation
Ragas
```

### DevOps

```text
Docker
GitHub Actions
```

---

## 9. Project Structure

```text
aegisops/
│
├── app/
│   ├── agents/
│   │   ├── nodes/
│   │   ├── tools/
│   │   ├── graph.py
│   │   └── state.py
│   │
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies.py
│   │
│   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   │
│   ├── ml/
│   │   ├── classification
│   │   └── data_quality
│   │
│   ├── llm/
│   │
│   ├── security/
│   │   ├── auth.py
│   │   └── rbac.py
│   │
│   ├── servicenow/
│   │   ├── client.py
│   │   ├── factory.py
│   │   ├── incidents.py
│   │   └── mock_client.py
│   │
│   ├── config.py
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── knowledge_base/
│
├── models/
│   └── incident_classifier_final.joblib
│
├── scripts/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── .env.example
├── pyproject.toml
├── requirements.txt
├── streamlit_app.py
└── README.md
```

---

## 10. Running Locally

### Create environment

```powershell
python -m venv .venv
```

### Activate

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Configure environment

Copy `.env.example` to `.env` and configure the development values.

The local demo uses:

```env
LLM_PROVIDER=mock
SERVICENOW_MODE=mock
DATABASE_URL=sqlite:///./aegisops.db
```

### Seed users

```powershell
python -m scripts.seed_users
```

### Run the API

```powershell
uvicorn app.main:app --reload
```

### Run the Streamlit UI

```powershell
python -m streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

## 11. Development Users

The seeded development environment contains:

| Username | Role     |
| -------- | -------- |
| viewer   | viewer   |
| analyst  | analyst  |
| operator | operator |
| admin    | admin    |

Development passwords are intentionally not documented in the repository README.

---

## 12. Docker

Build the image:

```powershell
docker build -t aegisops:latest .
```

Run:

```powershell
docker run --rm -p 8501:8501 aegisops:latest
```

Open:

```text
http://localhost:8501
```

---

## 13. Testing

Run the complete test suite:

```powershell
pytest -q
```

The current project test suite is passing with **151 tests**.

The suite covers:

* API endpoints
* authentication
* RBAC
* agent state
* classification
* retrieval
* policy decisions
* prompt-injection detection
* ServiceNow client behavior
* ServiceNow factory
* controlled ServiceNow tools
* action execution
* human approval
* verification
* persistence
* final-response generation
* integration workflows

---

## 14. CI/CD

GitHub Actions runs the test suite automatically for pushes and pull requests.

Workflow:

```text
GitHub
   ↓
Checkout
   ↓
Python 3.12
   ↓
Install dependencies
   ↓
Create CI environment
   ↓
pytest
   ↓
Pass / Fail
```

Workflow file:

```text
.github/workflows/ci.yml
```

---

## 15. Example End-to-End Execution

Example incident:

```text
VPN connection fails when working from home.
```

Example workflow:

```text
Incident
   ↓
Category: Support general
   ↓
Classification confidence: ~76.7%
   ↓
Priority: P3
   ↓
Retrieved documents: 3
   ↓
Reasoning
   ↓
Risk: LOW
   ↓
Policy: ALLOWED
   ↓
Controlled action
   ↓
Mock ServiceNow
   ↓
Verification
   ↓
VERIFIED
```

The Streamlit interface displays the classification, retrieved evidence, policy decision, selected action, verification result, and final response.

---

## 16. Human Approval Example

For a risky operation:

```text
Incident
   ↓
Reasoning
   ↓
High-risk proposed action
   ↓
Policy
   ↓
Human approval required
   ↓
Action status: PENDING
   ↓
ServiceNow action: NOT EXECUTED
```

This provides a safety boundary between agent reasoning and external automation.

---

## 17. Design Principles

### Controlled Autonomy

AegisOps is designed for controlled automation rather than unrestricted agent execution.

### Evidence-Based Reasoning

Resolution recommendations are grounded in retrieved knowledge-base evidence.

### Defense in Depth

Authentication, RBAC, prompt-injection detection, policy evaluation, human approval, and verification operate as separate controls.

### Verify External State

Successful execution is not assumed to mean successful resolution.

```text
Act → Observe → Verify
```

### Reproducible Development

The local application can run using mock providers, allowing development and demonstrations without paid external APIs.

---

## 18. Future Enhancements

Potential extensions include:

```text
Real LLM provider integration
Production ServiceNow integration
Approval-resume workflow
Advanced OpenTelemetry tracing
Phoenix observability
Redis-backed distributed state
Expanded knowledge base
Additional ITSM actions
Cloud deployment
Kubernetes deployment
Advanced cost and latency monitoring
```

---

## 19. Project Summary

AegisOps 2.0 demonstrates how machine learning, retrieval-augmented generation, agent orchestration, security controls, ITSM tooling, and verification can be combined into a controlled autonomous incident-resolution system.

The key architectural principle is:

```text
The agent can reason,
but application policy decides,
RBAC authorizes,
controlled tools execute,
and verification confirms the result.
```
