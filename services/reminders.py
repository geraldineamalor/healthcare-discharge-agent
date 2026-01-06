import re
from datetime import datetime, timedelta


def extract_followup_days(text):
    """
    Extract follow-up duration from text.
    Supports:
    - 'in 7 days'
    - 'in 1 week'
    - 'within 2 weeks'
    """

    text = text.lower()

    # Match days
    day_match = re.search(r'(\d+)\s*day[s]?', text)
    if day_match:
        return int(day_match.group(1))

    # Match weeks
    week_match = re.search(r'(\d+)\s*week[s]?', text)
    if week_match:
        return int(week_match.group(1)) * 7

    return None  # No follow-up mentioned


def create_reminders(text):
    followup_days = extract_followup_days(text)
    reminders = {}

    if followup_days:
        followup_date = datetime.today() + timedelta(days=followup_days)
        reminders["Doctor Follow-Up"] = followup_date.strftime("%Y-%m-%d")
    else:
        reminders["Doctor Follow-Up"] = "Not specified in instructions"

    return reminders
