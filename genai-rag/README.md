# RAG System — Chat with Your Documents

A Retrieval Augmented Generation (RAG) system that lets you upload any PDF and ask questions about it.
Answers are grounded in the document context — no hallucination, with source citations included.

## How It Works

1. **Upload** — PDF is uploaded via the browser UI or API
2. **Chunk** — Document is split into overlapping chunks (500 chars, 50 char overlap)
3. **Embed** — Each chunk is converted into a vector using HuggingFace embeddings
4. **Store** — Vectors are stored in ChromaDB (local vector database)
5. **Query** — User question is embedded and matched against stored vectors
6. **Answer** — Top matching chunks are sent to Groq (Llama 3.3 70B) to generate a grounded answer

## Tech Stack
Python · FastAPI · LangChain · ChromaDB · HuggingFace Embeddings · Groq · Docker

## Features
- Upload any PDF via browser UI or API
- Automatic chunking and semantic indexing
- Answers grounded strictly in document context
- Source chunks shown per answer for verification
- REST API with auto-generated Swagger docs at /docs

## How to Run
```bash
cp .env.example .env    # add your GROQ_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run with Docker
```bash
docker build -t genai-rag-api .
docker run -p 8000:8000 --env-file .env genai-rag-api
```

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | /upload | Upload and ingest a PDF |
| POST | /chat | Ask a question about your document |
| GET | /health | Health check |
| GET | / | Browser chat UI |
