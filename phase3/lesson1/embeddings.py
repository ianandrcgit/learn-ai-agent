import chromadb
from sentence_transformers import SentenceTransformer

# --- LOAD EMBEDDING MODEL ---
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded!")

# --- SETUP CHROMADB ---
client = chromadb.Client()
collection = client.create_collection("knowledge_base")

# --- OUR DOCUMENTS (facts to store) ---
documents = [
    "Python is a programming language used for AI and web development.",
    "FastAPI is a modern Python framework for building APIs quickly.",
    "ChromaDB is a vector database for storing and searching embeddings.",
    "RAG stands for Retrieval Augmented Generation.",
    "Embeddings convert text into numbers that capture meaning.",
    "LangChain is a framework for building AI agent applications.",
    "OpenRouter provides access to multiple AI models with one API key.",
    "Git is a version control system for tracking code changes.",
]

# --- STORE DOCUMENTS WITH EMBEDDINGS ---
print("\nStoring documents...")
for i, doc in enumerate(documents):
    embedding = model.encode(doc).tolist()
    collection.add(
        documents=[doc],
        embeddings=[embedding],
        ids=[f"doc_{i}"]
    )
print(f"Stored {len(documents)} documents!")

# --- SEARCH BY MEANING ---
def search(query: str, top_k: int = 4) -> None:
    print(f"\n🔍 Query: {query}")
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    print("Top results:")
    for i, doc in enumerate(results["documents"][0]):
        print(f"  {i+1}. {doc}")

# --- RUN SEARCHES ---
search("What is used for building APIs?")
search("How do I store vectors?")
search("Tell me about AI frameworks")
search("What is RAG?")