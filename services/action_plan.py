import re

def extract_days(text):
    """
    Extract number of days from discharge instructions.
    Example matches: '5 days', '7 day'
    """
    match = re.search(r'(\d+)\s*day[s]?', text.lower())
    if match:
        return int(match.group(1))
    return 2  # sensible default if duration not found


def create_action_plan(text):
    days = extract_days(text)
    plan = {}

    for day in range(1, days + 1):
        plan[f"Day {day}"] = {
            "Morning": "Take prescribed medication",
            "Evening": "Rest and follow wound care instructions"
        }

    return plan
