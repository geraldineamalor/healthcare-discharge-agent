from services.duration_utils import extract_duration_days

MAX_DAILY_PLAN_DAYS = 14  # UI limit

def create_action_plan(text):
    total_days = extract_duration_days(text) or 2
    plan = {}

    if total_days > MAX_DAILY_PLAN_DAYS:
        return {
            "Medication Duration": f"{total_days} days",
            "Note": (
                "This medication is prescribed for a long duration. "
                "Follow daily medication schedule as advised by your doctor."
            )
        }

    for day in range(1, total_days + 1):
        plan[f"Day {day}"] = {
            "Morning": "Take prescribed medication",
            "Evening": "Rest and follow care instructions"
        }

    return plan
