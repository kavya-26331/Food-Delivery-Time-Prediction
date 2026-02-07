import os
import faiss
import numpy as np
from langchain_ollama import OllamaLLM, OllamaEmbeddings

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "llm", "data", "vectorstore", "faq.txt")
INDEX_DIR = os.path.join(BASE_DIR, "llm", "data", "vectorstore")
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")

# Ensure directories exist
os.makedirs(INDEX_DIR, exist_ok=True)

# ---------------- LLM & EMBEDDINGS ----------------
llm = OllamaLLM(model="llama3.1")
embedder = OllamaEmbeddings(model="llama3.1")

# ---------------- BUILD VECTOR STORE ----------------
def build_faiss_index():
    print("Building FAISS index...")

    if not os.path.exists(DATA_FILE):
        # Create sample FAQ if missing
        sample_faq = [
            "Q: How to place an order?\nA: Select a restaurant, choose items, and confirm checkout.\n",
            "Q: Can I track my order?\nA: Yes, use the tracking feature in the app.\n",
            "Q: What payment methods are available?\nA: Credit card, debit card, and digital wallets.\n"
        ]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.writelines(sample_faq)
        print(f"Sample FAQ created at {DATA_FILE}")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        docs = f.readlines()

    embeddings = [embedder.embed_query(doc) for doc in docs]
    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, INDEX_FILE)
    return index, docs

# ---------------- LOAD VECTOR STORE ----------------
if not os.path.exists(INDEX_FILE):
    index, docs = build_faiss_index()
else:
    index = faiss.read_index(INDEX_FILE)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        docs = f.readlines()

# ---------------- SEARCH ----------------
def search_docs(query, k=3):
    query_vec = embedder.embed_query(query)
    query_vec = np.array([query_vec]).astype("float32")

    D, I = index.search(query_vec, k)
    return [docs[i] for i in I[0]]

# ---------------- CHAT FUNCTION ----------------
def chat(query):
    retrieved = search_docs(query, k=3)
    context = "\n".join(retrieved)

    prompt = f"""
You are a helpful food delivery assistant.
Use the context below to answer.

Context:
{context}

User question: {query}

Answer:
"""

    response = llm.invoke(prompt)
    return str(response)








