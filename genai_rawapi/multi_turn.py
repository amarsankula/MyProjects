# multi_turn.py — works with either API, shown here with OpenAI
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def chat(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
        temperature=0.7
    )

    assistant_message = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

# CLI loop
print("Chat started. Type 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = chat(user_input)
    print(f"AI: {response}\n")