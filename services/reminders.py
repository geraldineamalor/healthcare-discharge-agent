import re
from datetime import datetime, timedelta
from dateutil import parser

def extract_followup_date(text):
    """
    Extract explicit calendar dates like:
    '25 January 2026', 'Jan 25, 2026', '25/01/2026'
    """
    try:
        return parser.parse(text, fuzzy=True).date()
    except:
        return None


def extract_followup_sentence(text):
    sentences = re.split(r"[.\n]", text.lower())
    for s in sentences:
        if any(k in s for k in [
            "follow up",
            "follow-up",
            "appointment",
            "review",
            "orthopedic",
            "clinic"
        ]):
            return s
    return None


def extract_duration_days(text):
    match = re.search(r"(\d+)\s*day", text)
    return int(match.group(1)) if match else None


def create_reminders(text):
    reminders = {}

    followup_sentence = extract_followup_sentence(text)
    if not followup_sentence:
        reminders["Follow-Up Appointment"] = "Not specified"
        return reminders

    # 1️⃣ Try explicit date first
    explicit_date = extract_followup_date(followup_sentence)
    if explicit_date:
        reminders["Follow-Up Appointment"] = explicit_date.isoformat()
        return reminders

    # 2️⃣ Else fallback to duration
    days = extract_duration_days(followup_sentence)
    if days:
        follow_up_date = datetime.now().date() + timedelta(days=days)
        reminders["Follow-Up Appointment"] = follow_up_date.isoformat()
    else:
        reminders["Follow-Up Appointment"] = "Not specified"

    return reminders
