import os
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

# --- SETUP ---
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("rag_docs")
print("Ready!")


# --- STEP 1: LOAD DOCUMENT ---
def load_document(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()


# --- STEP 2: CHUNK BY PARAGRAPH ---
def chunk_document(text: str) -> list:
    paragraphs = text.strip().split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]


# --- STEP 3: EMBED AND STORE ---
def store_chunks(chunks: list) -> None:
    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"]
        )
    print(f"Stored {len(chunks)} chunks in ChromaDB")


# --- STEP 4: SEARCH RELEVANT CHUNKS ---
def search_chunks(query: str, top_k: int = 2) -> list:
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]


# --- STEP 5: GENERATE ANSWER WITH AI ---
def generate_answer(question: str, context_chunks: list) -> str:
    context = "\n\n".join(context_chunks)

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have that information."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]


# --- FULL RAG FUNCTION ---
def ask_rag(question: str) -> None:
    print(f"\n❓ Question: {question}")
    chunks = search_chunks(question)
    print(f"📄 Found {len(chunks)} relevant chunks")
    answer = generate_answer(question, chunks)
    print(f"🤖 Answer: {answer}")


# --- RUN PIPELINE ---
# Load and store document
text = load_document("document.txt")
chunks = chunk_document(text)
store_chunks(chunks)

# Ask questions
ask_rag("Who created Python and when?")
ask_rag("What is RAG and how does it work?")
ask_rag("What is the capital of France?")