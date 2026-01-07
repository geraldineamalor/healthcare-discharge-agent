import re

def extract_duration_days(text):
    """
    Extracts duration from text and returns number of days.
    Supports days, weeks, and months.
    """
    text = text.lower()

    match = re.search(r'(\d+)\s*(day|days|week|weeks|month|months)', text)
    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if "week" in unit:
        return value * 7
    if "month" in unit:
        return value * 30

    return value  # days
