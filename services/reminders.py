import re
from datetime import datetime, timedelta

def extract_duration(text):
    text = text.lower()

    patterns = [
        (r'(\d+)\s*year[s]?', 'year'),
        (r'(\d+)\s*month[s]?', 'month'),
        (r'(\d+)\s*week[s]?', 'week'),
        (r'(\d+)\s*day[s]?', 'day'),
    ]

    for pattern, unit in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1)), unit

    return None, None


def create_reminders(text):
    value, unit = extract_duration(text)
    today = datetime.today()
    reminders = {}

    if unit == "day":
        reminders["Follow-Up"] = (today + timedelta(days=value)).strftime("%Y-%m-%d")

    elif unit == "week":
        reminders["Follow-Up"] = (today + timedelta(days=value * 7)).strftime("%Y-%m-%d")

    elif unit == "month":
        reminders["Medication Review"] = (today + timedelta(days=30)).strftime("%Y-%m-%d")
        reminders["Duration"] = f"{value} month(s)"

    elif unit == "year":
        reminders["Quarterly Review"] = (today + timedelta(days=90)).strftime("%Y-%m-%d")
        reminders["Duration"] = f"{value} year(s)"

    else:
        reminders["Follow-Up"] = "Not specified in instructions"

    return reminders
import re
from datetime import datetime, timedelta

def extract_duration(text):
    text = text.lower()

    patterns = [
        (r'(\d+)\s*year[s]?', 'year'),
        (r'(\d+)\s*month[s]?', 'month'),
        (r'(\d+)\s*week[s]?', 'week'),
        (r'(\d+)\s*day[s]?', 'day'),
    ]

    for pattern, unit in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1)), unit

    return None, None


def create_reminders(text):
    value, unit = extract_duration(text)
    today = datetime.today()
    reminders = {}

    if unit == "day":
        reminders["Follow-Up"] = (today + timedelta(days=value)).strftime("%Y-%m-%d")

    elif unit == "week":
        reminders["Follow-Up"] = (today + timedelta(days=value * 7)).strftime("%Y-%m-%d")

    elif unit == "month":
        reminders["Medication Review"] = (today + timedelta(days=30)).strftime("%Y-%m-%d")
        reminders["Duration"] = f"{value} month(s)"

    elif unit == "year":
        reminders["Quarterly Review"] = (today + timedelta(days=90)).strftime("%Y-%m-%d")
        reminders["Duration"] = f"{value} year(s)"

    else:
        reminders["Follow-Up"] = "Not specified in instructions"

    return reminders
