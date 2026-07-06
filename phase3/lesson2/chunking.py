# --- SAMPLE LONG DOCUMENT ---
document = """
Python is a high-level programming language known for its simplicity.
It was created by Guido van Rossum and released in 1991.
Python is widely used in web development, data science, and artificial intelligence.

FastAPI is a modern web framework for building APIs with Python.
It is based on standard Python type hints and is very fast.
FastAPI automatically generates documentation for your API endpoints.

RAG stands for Retrieval Augmented Generation.
It is a technique that combines search with AI generation.
RAG allows AI to answer questions based on your own documents.
It first retrieves relevant chunks then passes them to an AI model.

ChromaDB is a vector database used to store embeddings.
It allows semantic search which finds meaning not just keywords.
ChromaDB runs locally and requires no external account or API key.
"""


# --- STRATEGY 1: Fixed Size Chunking ---
def fixed_size_chunks(text: str, chunk_size: int = 200) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]


# --- STRATEGY 2: Chunking with Overlap ---
def overlap_chunks(text: str, chunk_size: int = 200, overlap: int = 50) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]


# --- STRATEGY 3: Paragraph Chunking ---
def paragraph_chunks(text: str) -> list:
    paragraphs = text.strip().split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]


# --- SHOW RESULTS ---
def show_chunks(title: str, chunks: list) -> None:
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"Total chunks: {len(chunks)}")
    print(f"{'='*50}")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({len(chunk)} chars):")
        print(chunk)


# RUN
chunks1 = fixed_size_chunks(document)
chunks2 = overlap_chunks(document)
chunks3 = paragraph_chunks(document)

show_chunks("STRATEGY 1: Fixed Size", chunks1)
show_chunks("STRATEGY 2: With Overlap", chunks2)
show_chunks("STRATEGY 3: Paragraph", chunks3)

print(f"\n--- SUMMARY ---")
print(f"Fixed size  : {len(chunks1)} chunks")
print(f"With overlap: {len(chunks2)} chunks")
print(f"Paragraph   : {len(chunks3)} chunks")