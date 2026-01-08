def simplify_text(text):
    instructions = []

    rules = [
        ("take", "Take medicines as prescribed."),
        ("avoid", "Avoid heavy lifting and strenuous activity."),
        ("drink", "Drink plenty of fluids."),
        ("walk", "Walk short distances daily."),
        ("keep", "Keep the wound clean and dry."),
    ]

    lower = text.lower()

    for keyword, sentence in rules:
        if keyword in lower:
            instructions.append(sentence)

    return " ".join(instructions)