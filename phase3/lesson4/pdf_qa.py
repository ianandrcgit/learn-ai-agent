import os
import requests
import chromadb
import fitz  # pymupdf
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("pdf_docs")
print("Ready!")


# --- STEP 1: EXTRACT TEXT FROM PDF WITH PAGE NUMBERS ---
def extract_pdf(filepath: str) -> list:
    doc = fitz.open(filepath)
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append({
                "page": page_num,
                "text": text
            })
    print(f"Extracted {len(pages)} pages from PDF")
    return pages


# --- STEP 2: CHUNK EACH PAGE ---
def chunk_pages(pages: list) -> list:
    chunks = []
    for page in pages:
        paragraphs = page["text"].split("\n\n")
        for para in paragraphs:
            para = para.strip()
            if len(para) > 20:  # skip tiny fragments
                chunks.append({
                    "text": para,
                    "page": page["page"]
                })
    print(f"Created {len(chunks)} chunks")
    return chunks


# --- STEP 3: EMBED AND STORE WITH METADATA ---
def store_chunks(chunks: list) -> None:
    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk["text"]).tolist()
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{"page": chunk["page"]}],
            ids=[f"chunk_{i}"]
        )
    print(f"Stored {len(chunks)} chunks in ChromaDB")


# --- STEP 4: SEARCH WITH CITATIONS ---
def search_chunks(query: str, top_k: int = 3) -> list:
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"]
    )
    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({
            "text": doc,
            "page": meta["page"]
        })
    return chunks


# --- STEP 5: GENERATE ANSWER WITH CITATIONS ---
def generate_answer(question: str, chunks: list) -> None:
    context = ""
    for chunk in chunks:
        context += f"[Page {chunk['page']}]: {chunk['text']}\n\n"

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context below.
Always mention the page number when referencing information.
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
    answer = data["choices"][0]["message"]["content"]

    print(f"\n❓ Question: {question}")
    print(f"🤖 Answer: {answer}")
    print(f"📄 Sources: Pages {set(c['page'] for c in chunks)}")


# --- RUN ---
pages = extract_pdf("sample.pdf")
for p in pages:
    print(f"Page {p['page']}: {p['text'][:100]}")
chunks = chunk_pages(pages)
store_chunks(chunks)

# Ask your questions here
generate_answer("What is artificial intelligence?", search_chunks("artificial intelligence", top_k=4))
generate_answer("What is RAG?", search_chunks("RAG retrieval augmented generation", top_k=4))
generate_answer("What is machine learning?", search_chunks("machine learning", top_k=4))