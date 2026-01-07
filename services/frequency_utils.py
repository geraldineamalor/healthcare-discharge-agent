def extract_frequency(text):
    text = text.lower()

    if "thrice daily" in text or "three times daily" in text:
        return "thrice"
    if "twice daily" in text or "two times daily" in text:
        return "twice"
    if "once daily" in text or "daily" in text:
        return "once"

    return "once"
