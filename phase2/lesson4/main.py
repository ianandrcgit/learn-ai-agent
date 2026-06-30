import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

app = FastAPI()

# --- MEMORY (stored while server runs) ---
conversation_history = []


class Question(BaseModel):
    question: str


def ask_ai_with_memory(question: str) -> str:
    # Add user message to history
    conversation_history.append({"role": "user", "content": question})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": conversation_history  # send FULL history, not just one question
        }
    )
    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    # Add AI response to history too
    conversation_history.append({"role": "assistant", "content": answer})

    return answer


@app.get("/")
def home():
    return {"message": "Chatbot with Memory is running"}


@app.post("/chat")
def chat(payload: Question):
    answer = ask_ai_with_memory(payload.question)
    return {
        "question": payload.question,
        "answer": answer,
        "total_messages_in_memory": len(conversation_history)
    }


@app.post("/reset")
def reset():
    conversation_history.clear()
    return {"message": "Conversation memory cleared"}


@app.get("/history")
def get_history():
    return {"history": conversation_history}