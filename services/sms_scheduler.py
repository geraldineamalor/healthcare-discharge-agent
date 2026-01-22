from datetime import datetime, timedelta

def schedule_medication_sms(plan, phone):
    scheduled = []
    start_date = datetime.today()

    day_count = 0
    for day, tasks in plan.items():
        if not day.startswith("Day"):
            continue

        date = start_date + timedelta(days=day_count)
        day_count += 1

        for time, task_list in tasks.items():
            for task in task_list:
                message = f"{time} Reminder ({date.date()}): {task}"

                # Mock SMS print
                print(f"[MOCK SMS] To {phone}: {message}")

                scheduled.append({
                    "day": day,
                    "date": date.strftime("%d %b %Y"),
                    "time": time,
                    "task": task
                })

    return scheduled
