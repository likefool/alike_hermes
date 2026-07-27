# Project Gamma: Simple RAG System

A lightweight, modular Retrieval-Augmented Generation (RAG) system built with Python and SQLite. Designed for rapid prototyping, it allows for local vector storage and similarity-based retrieval using OpenAI-compatible APIs.

## 🚀 Features

- **Vector Store**: SQLite-backed storage for document content and high-dimensional embeddings.
- **RAG Engine**: Core logic handles document chunking, embedding generation, and similarity-based retrieval.
- **Dual Modes**:
    - **Production Mode**: Uses real OpenAI-compatible APIs for high-quality embeddings.
    - **Mock Mode**: Uses deterministic pseudo-random vectors for testing the pipeline without API costs or credentials.
- **Document Support**: Handles `.txt` and `.pdf` files.
- **CLI-First**: Simple command-line interface for ingestion and querying.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Database**: SQLite
- **Libraries**: 
    - `openai`: For embedding generation.
    - `langchain-text-splitters`: For intelligent document chunking.
    - `pypdf`: For PDF parsing.
    - `uv`: Recommended for environment management.

## 📂 Project Structure

```text
projects/projectGamma/
├── src/
│   ├── rag_engine.py      # Core RAG logic and VectorStore class
│   ├── ingest.py          # CLI tool for document ingestion
│   ├── query.py           # CLI tool for similarity search
│   ├── sample_history.txt # Test data (history)
│   └── sample_tech_spec.txt # Test data (technical specs)
├── environments/
│   └── .venv/             # Python virtual environment
└── test_pipeline.sh       # Automated test runner
```

## ⚙️ Setup & Installation

### 1. Environment Setup
It is recommended to use `uv` for managing the environment.

```bash
cd projects/projectGamma/environments
uv init --no-workspace
uv add openai pypdf langchain-text-splitters
```

### 2. Configuration
Set your OpenAI-compatible API credentials in your environment:

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_BASE_URL="https://api.openai.com/v1"
# Optional: specify a custom database path
export DB_PATH="projects/projectGamma/src/vector_store.db"
```

## 🚀 Usage

### Mode 1: Production (Real Embeddings)
Ensure your environment variables are set as shown above.

**Ingest Documents:**
```bash
python src/ingest.py path/to/document.pdf path/to/notes.txt
```

**Query the System:**
```bash
python src/query.py "What information is in the document?"
```

### Mode 2: Mock Mode (Testing Only)
Use this mode to verify the logic of the system without needing an API key.

**Ingest Documents (Mock):**
```bash
python src/ingest.py --mock path/to/document.txt
```

**Query the System (Mock):**
```bash
python src/query.py --mock "Your test query"
```

## 🧪 Automated Testing
To run the full pipeline (ingestion + multiple queries) in mock mode, use the provided test script:

```bash
chmod +x test_pipeline.sh
./test_pipeline.sh
```

## 📝 License
This project is provided for educational and prototyping purposes.
