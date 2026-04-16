🚀 AI Staffing Platform — Multi-Agent CV & Job Matching Platform

 Overview
TalentMatch AI is an intelligent multi-agent system designed to automate:

📄 CV parsing and analysis

📑 Job description (AO) understanding

🤝 Candidate-job matching

📊 Candidate ranking and scoring

The system leverages:

Multi-agent architecture (ADK / LangChain style)
RAG (Retrieval-Augmented Generation)
Vector search
LLM reasoning (Gemini)
Workflow automation (n8n)

🏗️ Architecture
Sources (Upload )
        ↓
   FastAPI Gateway
        ↓
   Orchestrator Agent
        ↓
 ┌─────────────────────────────┐
 │ Document Processing Agent   │
 │ Extraction Agent (skills)   │
 │ Matching Agent              │
 │ Scoring Agent               │
 │ Ranking Agent               │
 │ Reporting Agent             │
 └─────────────────────────────┘
        ↓
     Results (JSON / UI / API)
     
⚙️ Features
 Core Capabilities
CV & AO parsing (PDF, DOCX, XLSX)
Skill & task extraction
Semantic matching (LLM + similarity)
Candidate scoring & ranking
Batch processing
RAG-powered document understanding

 Advanced Features
Intelligent caching (file hashing)
Duplicate detection
Vector database search
Async multi-agent orchestration

LLM-as-Judge (future)

Tech Stack
Layer

Tech

API

FastAPI

Agents

Google ADK / Python

LLM

Gemini

RAG

Custom + vector store

Embeddings

Sentence Transformers

Storage

Local / Oracle (optional)

Orchestration

n8n

Container

Docker

CI/CD

GitHub Actions

Deployment

Kubernetes / Helm

📁 Project Structure
TalentMatch/
├── app/
│   ├── agents/
│   │   ├── orchestrator_agent.py
│   │   ├── batch_orchestrator_agent.py
│   │   ├── matching_agent.py
│   │   ├── scoring_agent.py
│   │   └── ...
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   ├── utils/
│   │   ├── file_hash.py
│   │   ├── chunker.py
│   ├── api/
│   │   ├── matching_api.py
│   └── main.py
│
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md

 Installation
1. Clone repo
git clone https://github.com/your-repo/talentmatch-ai.git
cd talentmatch-ai
2. Create virtual env
python -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Setup environment variables
Create .env:
GEMINI_API_KEY=your_key_here
5. Run API
uvicorn app.main:app --reload
👉 API available at:
http://localhost:8000
🧪 Run Tests
pytest -v
🐳 Docker
Build image
docker build -t talentmatch-ai .
Run container
docker run -p 8000:8000 talentmatch-ai
🐳 Docker Compose
docker compose up --build
🔁 CI/CD (GitHub Actions)
Pipeline includes:
✅ Linting (flake8, black, isort)
✅ Unit tests (pytest)
✅ Docker build
Optional: push image

Workflow file:
.github/workflows/ci-cd.yml
API Endpoints
🔹 Analyze (Single CV + AO)
POST /analyze
Form-data:

cv_file

ao_file

question

🔹 Rank Candidates (Batch)
POST /rank_candidates
Form-data:

ao_file

cv_files (multiple)

 RAG Pipeline
Steps
Chunk documents
Generate embeddings
Store vectors
Search via similarity
Inject into LLM context

Optimization
File hashing (avoid reprocessing)
Cache layer
Chunk-level indexing
📈 Scaling & Production

Kubernetes
Horizontal scaling (pods)
Load balancing
High availability

Helm
Packaging deployment
Config management

Observability
Prometheus

Grafana


