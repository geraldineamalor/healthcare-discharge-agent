import re

def extract_duration_days(text):
    text = text.lower()

    # Years
    year_match = re.search(r'(\d+)\s*year[s]?', text)
    if year_match:
        return int(year_match.group(1)) * 365

    # Months
    month_match = re.search(r'(\d+)\s*month[s]?', text)
    if month_match:
        return int(month_match.group(1)) * 30

    # Weeks
    week_match = re.search(r'(\d+)\s*week[s]?', text)
    if week_match:
        return int(week_match.group(1)) * 7

    # Days
    day_match = re.search(r'(\d+)\s*day[s]?', text)
    if day_match:
        return int(day_match.group(1))

    return None
