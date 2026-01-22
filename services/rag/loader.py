import os
import streamlit as st
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_knowledge_base():
    base_path = "services/rag/knowledge_base"
    documents = []
    sources = []

    for file in os.listdir(base_path):
        if file.endswith(".txt"):
            with open(os.path.join(base_path, file), "r", encoding="utf-8") as f:
                documents.append(f.read())
                sources.append(file)

    model = load_embedding_model()
    embeddings = model.encode(documents)

    return documents, embeddings, sources
