from datetime import datetime, timedelta

def create_reminders():
    return {
        "Doctor Follow-Up": str(datetime.today() + timedelta(days=7)),
        "Medication Review": str(datetime.today() + timedelta(days=3))
    }
