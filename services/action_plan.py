from services.duration_utils import extract_duration_days
from services.frequency_utils import parse_frequency

def create_action_plan(text):
    plan = {}

    duration = extract_duration_days(text) or 1
    frequency_slots = parse_frequency(text)

    for day in range(1, duration + 1):
        day_key = f"Day {day}"
        plan[day_key] = {}

        # Medication tasks
        if frequency_slots:
            for slot in frequency_slots:
                plan[day_key].setdefault(slot, []).append(
                    "Take prescribed medication"
                )

        # Always add rest instruction in evening
        plan[day_key].setdefault("Evening", []).append(
            "Rest and follow care instructions"
        )

    return plan
