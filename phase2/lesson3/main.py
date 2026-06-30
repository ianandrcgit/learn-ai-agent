import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")
app = FastAPI()


# --- REQUEST FORMAT ---
class Question(BaseModel):
    question: str


# --- AI CALL FUNCTION ---
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
                {"role": "user", "content": question}
            ]
        }
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]


# --- ENDPOINTS ---
@app.get("/")
def home():
    return {"message": "AI Backend is running"}


@app.post("/ask")
def ask(payload: Question):
    answer = ask_ai(payload.question)
    return {"question": payload.question, "answer": answer}