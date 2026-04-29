import os
import sys
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def extract_text(pdf_path: str) -> str:
    """Extract raw text from a PDF file."""
    print(f"[1/3] Reading {pdf_path}...")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    print(f"Extracted {len(text)} characters from {len(reader.pages)} pages")
    return text


def chunk_text(text: str) -> list[str]:
    """Split text into overlapping chunks for embedding."""
    print(f"[2/3] Splitting into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_text(text)
    print(f"      Created {len(chunks)} chunks")
    return chunks


def store_chunks(chunks: list[str]) -> None:
    """Embed chunks and store in ChromaDB."""
    print(f"[3/3] Embedding and storing in ChromaDB...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"      Stored {len(chunks)} chunks at '{CHROMA_PATH}'")


def ingest_pdf(pdf_path: str) -> int:
    """Full pipeline: PDF → chunks → ChromaDB."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    text = extract_text(pdf_path)
    chunks = chunk_text(text)
    store_chunks(chunks)

    print(f"\nDone. {len(chunks)} chunks ready to query.")
    return len(chunks)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest.py yourfile.pdf")
        sys.exit(1)

    ingest_pdf(sys.argv[1])