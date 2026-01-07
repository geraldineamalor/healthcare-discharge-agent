def is_chronic_care(text):
    text = text.lower()

    # 🚨 HARD OVERRIDE: surgical / acute procedures
    acute_keywords = [
        "appendectomy", "surgery", "surgical", "post-operative",
        "procedure", "incision", "wound", "stitches"
    ]

    if any(word in text for word in acute_keywords):
        return False  # ALWAYS acute care

    signals = 0

    duration_signals = [
        "long-term", "ongoing", "indefinitely", "maintenance"
    ]

    monitoring_signals = [
        "monitor", "check", "record", "track", "log"
    ]

    lifestyle_signals = [
        "diet", "exercise", "physical activity", "low sodium", "weight"
    ]

    chronic_conditions = [
        "diabetes", "hypertension", "asthma", "copd",
        "arthritis", "epilepsy", "hypothyroidism", "ckd"
    ]

    for group in [
        duration_signals,
        monitoring_signals,
        lifestyle_signals,
        chronic_conditions
    ]:
        if any(word in text for word in group):
            signals += 1

    return signals >= 2
