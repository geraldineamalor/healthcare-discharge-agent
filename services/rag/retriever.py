# services/rag/retriever.py

import numpy as np
from services.rag.loader import load_knowledge_base
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_docs(query, top_k=2):
    documents, embeddings, sources = load_knowledge_base()

    query_embedding = model.encode([query])[0]
    scores = embeddings @ query_embedding

    top_indices = scores.argsort()[-top_k:][::-1]

    return [
        {
            "source": sources[i],
            "content": documents[i]
        }
        for i in top_indices
    ]
