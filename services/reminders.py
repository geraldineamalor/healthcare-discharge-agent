import re
from datetime import datetime, timedelta
from services.duration_utils import extract_duration_days


def extract_followup_sentence(text):
    """
    Extract only the sentence that mentions follow-up.
    Prevents medication duration from interfering.
    """
    sentences = re.split(r'[.\n]', text.lower())
    for s in sentences:
        if any(k in s for k in [
            "follow up",
            "follow-up",
            "review",
            "appointment",
            "clinic",
            "see doctor"
        ]):
            return s
    return None


def create_reminders(text):
    reminders = {}

    followup_sentence = extract_followup_sentence(text)
    if not followup_sentence:
        reminders["Follow-Up"] = "Follow-up recommended (date not specified)"
        return reminders


    days = extract_duration_days(followup_sentence)

    if days:
        follow_up_date = datetime.now().date() + timedelta(days=days)
        reminders["Follow-Up Appointment"] = follow_up_date.isoformat()
    else:
        reminders["Follow-Up Appointment"] = "Not specified"

    return reminders
