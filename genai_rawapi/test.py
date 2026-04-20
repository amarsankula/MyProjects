import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "session_id": "test1",
        "message": "ok, i will bear with you",
        "provider": "groq"
    }
)

print(response.status_code)
# print (response)
print(response.json())
