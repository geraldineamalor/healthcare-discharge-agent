def detect_dangers(text):
    text = text.lower()
    dangers = []

    danger_map = {
        "fever": "High fever",
        "bleeding": "Excessive bleeding",
        "pain": "Severe or worsening pain",
        "vomiting": "Persistent nausea or vomiting",
        "difficulty breathing": "Difficulty breathing",
        "chest pain": "Chest pain",
        "redness": "Redness or discharge from wound",
        "swelling": "Swelling at surgical site",
        "infection": "Signs of infection",
    }

    for keyword, message in danger_map.items():
        if keyword in text:
            dangers.append(message)

    # Fallback only if nothing matched
    if not dangers:
        dangers.append("Seek medical help if symptoms worsen")

    return dangers
