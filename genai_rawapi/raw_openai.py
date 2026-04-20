from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "Explain RAG in 3 sentences."}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
print(f"\nTokens used: {response.usage.total_tokens}")