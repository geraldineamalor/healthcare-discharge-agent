from services.duration_utils import extract_duration_days
from services.frequency_utils import extract_frequency

def create_action_plan(text):
    days = extract_duration_days(text) or 1
    frequency = extract_frequency(text)  # once | twice | thrice

    plan = {}

    for day in range(1, days + 1):
        plan[f"Day {day}"] = {}

        if frequency == "once":
            plan[f"Day {day}"]["Morning"] = [
                "Take prescribed medication"
            ]

        elif frequency == "twice":
            plan[f"Day {day}"]["Morning"] = [
                "Take prescribed medication"
            ]
            plan[f"Day {day}"]["Evening"] = [
                "Take prescribed medication"
            ]

        elif frequency == "thrice":
            plan[f"Day {day}"]["Morning"] = [
                "Take prescribed medication"
            ]
            plan[f"Day {day}"]["Afternoon"] = [
                "Take prescribed medication"
            ]
            plan[f"Day {day}"]["Evening"] = [
                "Take prescribed medication"
            ]

        # Care instruction always included
        plan[f"Day {day}"].setdefault("Evening", []).append(
            "Rest and follow care instructions"
        )

    return plan
