from services.frequency_utils import parse_frequency
from services.duration_utils import extract_medications

def create_action_plan(text):
    medications = extract_medications(text)
    plan = {}

    if not medications:
        return plan

    max_days = max(med["days"] for med in medications)

    for day in range(1, max_days + 1):
        plan[f"Day {day}"] = {
            "Morning": [],
            "Afternoon": [],
            "Evening": []
        }

        for med in medications:
            if day > med["days"]:
                continue

            if med["frequency"] == "Once Daily":
                plan[f"Day {day}"]["Morning"].append(
                    f"Take {med['name']}"
                )

            elif med["frequency"] == "Twice Daily":
                plan[f"Day {day}"]["Morning"].append(
                    f"Take {med['name']}"
                )
                plan[f"Day {day}"]["Evening"].append(
                    f"Take {med['name']}"
                )

            elif med["frequency"] == "Thrice Daily":
                plan[f"Day {day}"]["Morning"].append(
                    f"Take {med['name']}"
                )
                plan[f"Day {day}"]["Afternoon"].append(
                    f"Take {med['name']}"
                )
                plan[f"Day {day}"]["Evening"].append(
                    f"Take {med['name']}"
                )

    return plan
