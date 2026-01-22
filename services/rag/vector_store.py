# services/rag/vector_store.py

import os
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
KB_PATH = "services/rag/knowledge_base"

_model = SentenceTransformer(MODEL_NAME)
_documents = []
_embeddings = []
_sources = []


def load_vector_store():
    global _documents, _embeddings, _sources

    if _documents:
        return _documents, _embeddings, _sources

    for file in os.listdir(KB_PATH):
        if file.endswith(".txt"):
            path = os.path.join(KB_PATH, file)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                _documents.append(text)
                _sources.append(file.replace(".txt", ""))

    _embeddings = _model.encode(_documents)
    return _documents, _embeddings, _sources
