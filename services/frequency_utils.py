import re

def parse_frequency(text):
    text = text.lower()

    if "thrice" in text or "three times" in text:
        return ["Morning", "Afternoon", "Evening"]

    if "twice" in text or "two times" in text:
        return ["Morning", "Evening"]

    if "once" in text or "daily" in text:
        return ["Morning"]

    if "every 8 hours" in text:
        return ["Morning", "Afternoon", "Evening"]

    return []
