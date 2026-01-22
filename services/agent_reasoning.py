def generate_agent_reasoning(medications, action_plan, care_type, reminders):
    """
    Generates a structured, human-readable explanation of how
    the agent planned the patient's care.
    """

    reasoning = []

    # 🔍 Detection
    reasoning.append("🔍 Detection")
    reasoning.append(f"• {len(medications)} medication(s) detected.")

    for med in medications:
        reasoning.append(
            f"• {med['name']}: {med['frequency']} for {med['days']} days."
        )

    # 🧠 Planning
    reasoning.append("")
    reasoning.append("🧠 Planning")

    total_days = max(m["days"] for m in medications) if medications else 0
    reasoning.append(f"• Action plan created for {total_days} days.")
    reasoning.append("• Medication schedules handled independently.")

    # ⏱ Scheduling
    reasoning.append("")
    reasoning.append("⏱ Scheduling")

    for med in medications:
        if med["days"] < total_days:
            reasoning.append(
                f"• {med['name']} stops after Day {med['days']}."
            )
        else:
            reasoning.append(
                f"• {med['name']} continues through Day {med['days']}."
            )

    # ⚠️ Safety
    reasoning.append("")
    reasoning.append("⚠️ Safety")

    if reminders:
        reasoning.append("• Follow-up appointment detected.")
    else:
        reasoning.append("• No follow-up appointment found.")

    reasoning.append("• Danger signs shown for patient awareness.")

    # Care type reasoning
    reasoning.append("")
    reasoning.append("🩺 Care Classification")
    reasoning.append(f"• Care classified as {care_type}.")

    return reasoning
