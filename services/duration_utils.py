import re

def extract_medications(text):
    """
    Extract medication name, frequency, and duration from discharge instructions.
    Returns a list of dicts.
    """

    medications = []
    text = text.lower()

    # Split into sentences
    sentences = re.split(r'[.\n]', text)

    for sentence in sentences:
        if "take" not in sentence:
            continue

        # Frequency
        freq = None
        if "once daily" in sentence:
            freq = "Once Daily"
        elif "twice daily" in sentence:
            freq = "Twice Daily"
        elif "thrice daily" in sentence:
            freq = "Thrice Daily"

        # Duration
        duration_match = re.search(r'(\d+)\s*days', sentence)
        days = int(duration_match.group(1)) if duration_match else None

        # Medication name (simple but safe)
        med_match = re.search(r'take\s+(.*?)\s+(once|twice|thrice)', sentence)
        medication = med_match.group(1).strip() if med_match else "Medication"

        if freq and days:
            medications.append({
                "name": medication.title(),
                "frequency": freq,
                "days": days
            })

    return medications
