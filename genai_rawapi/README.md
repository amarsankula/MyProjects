# GenAI Chat API

A multi-provider LLM chat API with session-based conversation memory and a browser UI.
Supports OpenAI, Anthropic, and Groq — switch providers via a single parameter.

## Why Groq?
Groq provides free credits and extremely fast inference using Llama 3.3 70B —
ideal for development without API costs.

## Tech Stack
Python · FastAPI · Groq · OpenAI · Anthropic · Docker

## Features
- Multi-provider support (Groq, OpenAI, Anthropic)
- Session-based conversation memory
- Browser chat UI served from FastAPI
- REST API with Swagger docs at /docs

## How to Run
cp .env.example .env   # add your API keys
uvicorn main:app --reload

## Run with Docker
docker build -t genai-chat-api .
docker run -p 8000:8000 --env-file .env genai-chat-api

## API Endpoints
POST /chat           — send a message
GET  /history/{id}  — get conversation history
GET  /health         — health check
GET  /              — chat UI
