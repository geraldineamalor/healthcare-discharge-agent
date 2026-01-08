from datetime import datetime, timedelta
from services.sms_reminders import send_sms_mock

def schedule_medication_sms(plan, phone_number):
    today = datetime.now()

    for day, tasks in plan.items():
        day_num = int(day.split(" ")[1])
        date = today + timedelta(days=day_num - 1)

        for time, task_list in tasks.items():
            for task in task_list:
                message = f"{time} Reminder ({date.date()}): {task}"
                send_sms_mock(phone_number, message)
