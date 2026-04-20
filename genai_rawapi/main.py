from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
from groq import Groq
import anthropic
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="GenAI Chat API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


openai_client = OpenAI()
anthropic_client = anthropic.Anthropic()
groq_client = Groq()

# In-memory store (per session) — you'll replace with Redis in Phase 2
conversation_store: dict[str, list] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str
    provider: str = "openai"  # "openai" or "anthropic"

class ChatResponse(BaseModel):
    session_id: str
    response: str
    provider: str

@app.get("/")
async def serve_ui():
    return FileResponse("chat_ui.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id

    # Init history if new session
    if session_id not in conversation_store:
        conversation_store[session_id] = []

    history = conversation_store[session_id]
    history.append({"role": "user", "content": request.message})

    if request.provider == "openai":
        messages = [{"role": "system", "content": "You are a helpful assistant."}] + history
        res = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        reply = res.choices[0].message.content

    elif request.provider == "anthropic":
        res = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="You are a helpful assistant.",
            messages=history
        )
        reply = res.content[0].text
    
    elif request.provider == "groq":
        messages = [{"role": "system", "content": "You are a helpful assistant."}] + history
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        reply = res.choices[0].message.content

    else:
        raise HTTPException(status_code=400, detail="Invalid provider")

    history.append({"role": "assistant", "content": "reply"})

    return ChatResponse(
        session_id=session_id,
        response=reply,
        provider=request.provider
    )

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    return conversation_store.get(session_id, [])

@app.delete("/history/{session_id}")
async def clear_history(session_id: str):
    conversation_store.pop(session_id, None)
    return {"status": "cleared"}

@app.get("/health")
async def health():
    return {"status": "ok"}