def generate_danger_signs(retrieved_docs):
    danger_signs = []

    for doc in retrieved_docs:
        text = doc["content"].lower()

        if "difficulty breathing" in text:
            danger_signs.append("Difficulty breathing")
        if "high fever" in text:
            danger_signs.append("High fever")
        if "chest pain" in text:
            danger_signs.append("Chest pain")

    return list(set(danger_signs))
