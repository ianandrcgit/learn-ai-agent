import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found. Check your .env file.")

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are a senior AI developer mentor.
You explain concepts clearly and simply.
You always use short sentences.
You always give one practical example after explaining.
Never use jargon without explaining it first.
"""

# --- NON-STREAMING (waits for full response) ---
def ask_ai(question: str) -> str:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        }
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]


# --- STREAMING (word by word) ---
def ask_ai_streaming(question: str) -> None:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "stream": True,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        },
        stream=True
    )

    print("\n--- Streaming Response ---")
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                line = line[6:]
            if line == "[DONE]":
                break
            try:
                chunk = json.loads(line)
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    print(delta["content"], end="", flush=True)
            except json.JSONDecodeError:
                continue
    print("\n")


# RUN
print("=== Non-Streaming (waits for full response) ===")
answer = ask_ai("What is a system prompt in AI?")
print(answer)

print("\n=== Streaming (word by word) ===")
ask_ai_streaming("What is a system prompt in AI?")