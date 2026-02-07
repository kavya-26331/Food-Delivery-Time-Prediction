from sentence_transformers import SentenceTransformer
import faiss
import os
from app.utils.text_cleaning import clean_text

def load_documents():
    docs = []
    for file in ['faqs.txt', 'refund_policy.txt', 'delivery_rules.txt']:
        with open(f'app/llm/data/{file}', 'r') as f:
            docs.append(clean_text(f.read()))
    return docs

def create_vectorstore():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    docs = load_documents()
    embeddings = model.encode(docs)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, 'app/llm/vectorstore/index.faiss')
    with open('app/llm/vectorstore/docs.txt', 'w') as f:
        f.write('\n'.join(docs))

if __name__ == "__main__":
    create_vectorstore()
