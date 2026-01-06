from datetime import datetime, timedelta

def create_action_plan(text):
    today = datetime.today()
    return {
        "Day 1": {
            "Morning": "Take prescribed medicine",
            "Evening": "Clean wound"
        },
        "Day 2": {
            "Morning": "Light walking",
            "Night": "Medication"
        }
    }
