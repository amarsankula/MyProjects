### Gen AI chat API
Built a small chatbot kind of application using multiple providers (OPENAI, ANTHROPIC, GROQ)
Used Groq , it has free credits which we can use for building these chat applications

### Tech Stack Used

Python,  FastApi, Docker , AI models (Groq,Anthropic , Open AI)

### How to run

uvicorn main:app --reload


### Docker 
docker build -t genai-chat-api .


docker run -p 8000:8000 --env-file .env genai-chat-api
