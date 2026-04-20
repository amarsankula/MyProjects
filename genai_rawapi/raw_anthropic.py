import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "Explain RAG in 3 sentences."}
    ]
)

print(message.content[0].text)
print(f"\nInput tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")