import streamlit as st
from services.simplifier import simplify_text
from services.action_plan import create_action_plan
from services.danger_alerts import detect_dangers
from services.reminders import create_reminders
from evaluation.readability import get_readability
from utils.disclaimers import medical_disclaimer
from utils.citations import get_citations
from services.care_type import is_chronic_care

st.set_page_config(page_title="Discharge Instruction Simplifier")

st.title("🏥 Discharge Instruction Simplifier & Follow-Up Agent")

input_text = st.text_area("Paste Discharge Instructions")

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Simplify Instructions"):
    st.session_state.submitted = True

if st.session_state.submitted:
    # ---------- Processing ----------
    simplified = simplify_text(input_text)
    plan = create_action_plan(input_text)
    alerts = detect_dangers(input_text)
    reminders = create_reminders(input_text)
    readability = get_readability(simplified)

    care_type = "Chronic Care" if is_chronic_care(input_text) else "Acute / Short-Term Care"

    # ---------- Care Classification ----------
    st.subheader("🩺 Care Classification")
    st.info(care_type)

    # ---------- Simplified Instructions ----------
    st.subheader("📄 Simplified Instructions")
    st.write(simplified)

    # ---------- Action Plan ----------
    st.subheader("📅 Action Plan")

    if care_type == "Chronic Care":
        st.json(plan)

    else:
        st.subheader("✅ Daily Checklist")

        total = 0
        completed = 0

    # ---- Sort days correctly ----
        day_keys = sorted(
            [k for k in plan.keys() if k.startswith("Day ")],
            key=lambda x: int(x.split(" ")[1])
        )

    # ---- Fixed time order ----
        time_order = ["Morning", "Afternoon", "Evening"]

        for day in day_keys:
            st.markdown(f"### {day}")

            tasks = plan[day]

            for time in time_order:
                if time not in tasks:
                    continue

                for idx, task in enumerate(tasks[time]):
                    checkbox_key = f"{day}-{time}-{idx}"

                    checked = st.checkbox(
                        f"{time}: {task}",
                        key=checkbox_key
                    )

                    total += 1
                    if checked:
                        completed += 1

            st.divider()

   

        if total > 0:
            st.progress(completed / total)

    # ---------- Danger Signs ----------
    st.subheader("⚠️ Danger Signs")
    st.write(alerts)

    # ---------- Follow-Up Reminders ----------
    st.subheader("⏰ Follow-Up Reminders")
    st.json(reminders)

    # ---------- Readability ----------
    st.subheader("📊 Readability Score")
    st.write(readability)

    # ---------- Footer ----------
    st.info(medical_disclaimer())
    st.caption(get_citations())
