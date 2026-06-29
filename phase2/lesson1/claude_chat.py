import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found in environment. Check your .env file.")


def _openrouter_request(payload: dict) -> dict:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        raise RuntimeError(f"OpenRouter returned a non-JSON response: {response.text}")

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error {response.status_code}: {data}")
    if "choices" not in data or not data["choices"]:
        raise RuntimeError(f"OpenRouter response missing choices: {data}")

    return data


def ask_ai(question: str) -> str:
    data = _openrouter_request({
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": question}
        ]
    })
    return data["choices"][0]["message"]["content"]


def ask_ai_with_role(question: str) -> str:
    data = _openrouter_request({
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You explain things simply to beginner developers."},
            {"role": "user", "content": question}
        ]
    })
    return data["choices"][0]["message"]["content"]

# RUN
print("=== Basic Question ===")
answer = ask_ai("What is an API in simple terms?")
print(answer)

print("\n=== With System Prompt ===")
answer2 = ask_ai_with_role("What is a REST API?")
print(answer2)