import re

def extract_duration_days(text):
    """
    Extract number of days from phrases like:
    - in 10 days
    - after 2 weeks
    - within 1 week
    """
    text = text.lower()

    day_match = re.search(r'(\d+)\s*day', text)
    if day_match:
        return int(day_match.group(1))

    week_match = re.search(r'(\d+)\s*week', text)
    if week_match:
        return int(week_match.group(1)) * 7

    return None
