import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from ingest import ingest_pdf
from query import query_rag

load_dotenv()

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ── Models ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str
    k: int = 3  # number of chunks to retrieve

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


# ── Routes ──────────────────────────────────────────────

@app.get("/")
async def serve_ui():
    return FileResponse("chat_ui.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Accept a PDF, save it, ingest it into ChromaDB."""

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Save uploaded file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ingest into ChromaDB
    try:
        chunk_count = ingest_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    return {
        "filename": file.filename,
        "chunks_stored": chunk_count,
        "status": "ready to query"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Ask a question — get an answer from your uploaded documents."""

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = query_rag(request.question, k=request.k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"]
    )