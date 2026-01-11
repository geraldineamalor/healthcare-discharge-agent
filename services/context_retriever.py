import json

with open("services/knowledge/conditions.json") as f:
    KNOWLEDGE = json.load(f)

def retrieve_context(text):
    text = text.lower()
    for condition, info in KNOWLEDGE.items():
        if condition in text:
            return info
    return None
