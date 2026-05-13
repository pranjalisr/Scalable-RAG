# 🔍 Scalable RAG with Async Queues

A production-ready **Retrieval-Augmented Generation (RAG)** system built with **FastAPI** and **async task queues**, enabling high-throughput, non-blocking document ingestion and question-answering at scale.

---

## 📌 Overview

This project implements a scalable RAG pipeline that decouples document ingestion from query serving using asynchronous queues. Instead of processing documents synchronously in the request cycle, heavy embedding and indexing work is offloaded to background workers — keeping the API fast and responsive under load.

```
User Query ──► FastAPI ──► Vector Store ──► LLM ──► Answer
                  │
Document Upload ──► Async Queue ──► Worker ──► Embeddings ──► Vector Store
```

---

## ✨ Features

- **Async Queue Architecture** — Document ingestion is decoupled from the API via message queues, preventing bottlenecks during large uploads
- **FastAPI Backend** — High-performance, async-native REST API with automatic OpenAPI docs
- **Scalable by Design** — Workers can be scaled horizontally to handle ingestion load independently of query traffic
- **RAG Pipeline** — Combines vector retrieval with an LLM to produce grounded, context-aware answers
- **Non-blocking Uploads** — File/document upload endpoints return immediately; processing happens in the background

---

## 🗂️ Project Structure

```
Scalable-RAG/
└── RAG/
    └── Fastapi/
        ├── main.py             # FastAPI app entrypoint
        ├── routes/             # API route handlers (upload, query)
        ├── queue/              # Async queue producer & consumer logic
        ├── embeddings/         # Embedding model integration
        ├── vector_store/       # Vector DB client (e.g. FAISS / Qdrant / Chroma)
        ├── llm/                # LLM integration for generation
        ├── models.py           # Pydantic request/response schemas
        └── requirements.txt    # Python dependencies
```

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Async Queue | asyncio / Celery / Redis (or similar) |
| Embeddings | OpenAI / HuggingFace Sentence Transformers |
| Vector Store | FAISS / Qdrant / Chroma |
| LLM | OpenAI GPT / Ollama |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A running instance of your chosen vector store (e.g. Qdrant, Chroma)
- A queue broker if using Celery (e.g. Redis)
- An LLM API key (e.g. OpenAI) or a local Ollama setup

### Installation

```bash
# Clone the repository
git clone https://github.com/pranjalisr/Scalable-RAG.git
cd Scalable-RAG/RAG/Fastapi

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in `RAG/Fastapi/`:

```env
OPENAI_API_KEY=your_openai_api_key
VECTOR_STORE_URL=http://localhost:6333   # e.g. Qdrant
REDIS_URL=redis://localhost:6379         # if using Celery
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
```

### Running the App

```bash
# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# (If using Celery) Start the worker in a separate terminal
celery -A queue.worker worker --loglevel=info
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## 📡 API Endpoints

### Upload a Document
```http
POST /upload
Content-Type: multipart/form-data

file: <your_document.pdf>
```
Returns a job ID immediately. The document is queued for async processing.

### Check Ingestion Status
```http
GET /status/{job_id}
```

### Query the RAG System
```http
POST /query
Content-Type: application/json

{
  "question": "What are the key findings in the document?"
}
```

**Response:**
```json
{
  "answer": "The key findings include ...",
  "sources": ["chunk_1", "chunk_2"]
}
```

---

## 🔄 How It Works

1. **Document Upload** — A document is received by the FastAPI endpoint and its processing task is pushed onto the async queue. The API responds immediately with a job ID.
2. **Background Processing** — A worker picks up the task, loads and chunks the document, generates embeddings, and stores them in the vector store.
3. **Query Time** — When a user submits a question, the API embeds the query, retrieves the top-k relevant chunks from the vector store, and passes them as context to the LLM.
4. **Answer Generation** — The LLM generates a grounded response using only the retrieved context, minimizing hallucinations.

---

## 📈 Scalability

The async queue pattern means the ingestion pipeline scales independently of query serving:

- Add more **workers** to handle high document upload volume
- Scale the **API** horizontally for more concurrent queries
- The **vector store** and **queue broker** are the only shared state, both of which support clustering

---


## 📄 License

This project is open-source. See [LICENSE](LICENSE) for details.


