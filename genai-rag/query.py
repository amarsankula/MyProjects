import os
from groq import Groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_vectorstore():
    """Load ChromaDB vectorstore."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )


def query_rag(question: str, k: int = 3) -> dict:
    """Search ChromaDB, build prompt, call Groq, return answer + sources."""

    client = Groq()
    vectorstore = get_vectorstore()

    # Step 1 — Retrieve relevant chunks
    results = vectorstore.similarity_search(question, k=k)

    if not results:
        return {
            "answer": "No relevant documents found. Please upload a PDF first.",
            "sources": []
        }

    context = "\n\n".join([doc.page_content for doc in results])

    # Step 2 — Build RAG prompt
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the context below.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}
Answer:"""

    # Step 3 — Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": [doc.page_content[:200] for doc in results]
    }