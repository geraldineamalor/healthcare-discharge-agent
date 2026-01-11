import streamlit as st
from services.simplifier import simplify_text
from services.action_plan import create_action_plan
from services.danger_alerts import detect_dangers
from services.reminders import create_reminders
from evaluation.readability import get_readability
from utils.disclaimers import medical_disclaimer
from utils.citations import get_citations
from services.care_type import is_chronic_care
from services.sms_scheduler import schedule_medication_sms
from services import care_type
from services.context_retriever import retrieve_context


st.set_page_config(page_title="Discharge Instruction Simplifier")

st.title("Discharge Instruction Simplifier & Follow-Up Agent")

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


    # ---------- Care Classification ----------
    st.subheader("Care Classification")
    if care_type == "Chronic Care":
        st.success("🟢 Chronic Care: Long-term management")
    else:
        st.warning("🟡 Acute Care: Short-term recovery")
        
    # ---------- Simplified Instructions ----------
    with st.container(border=True):
        st.subheader("Simplified Instructions")
        st.write(simplified)
    context = retrieve_context(input_text)

    if context:
        st.subheader("🧠 Condition-Specific Guidance")
        st.write(context["care"])

        st.subheader("⚠️ Condition-Specific Danger Signs")
        for sign in context["danger"]:
            st.markdown(f"- {sign}")



    # ---------- Action Plan ----------
    st.subheader("Action Plan")

    if care_type == "Chronic Care":
        st.markdown("### Ongoing Care Plan")
        for item in plan["Daily Routine"]:
            st.checkbox(item, disabled=True)

    else:
        with st.container(border=True):
            st.subheader("Daily Checklist")

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
    with st.container(border=True):
        st.subheader("⚠️ Danger Signs")
        st.error("Seek medical help if you notice:")

        alerts = detect_dangers(input_text)

        if alerts:
            for alert in alerts:
                st.markdown(f"- {alert}")
        else:
            st.markdown("- Contact your doctor if symptoms worsen or new symptoms appear.")

    # ---------- Follow-Up Reminders ----------
    with st.container(border=True):
            st.subheader("Follow-Up Reminders")
            st.json(reminders)

    phone = st.text_input("Enter phone number for SMS reminders")

    if st.button("Enable SMS Reminders"):
        schedule_medication_sms(plan, phone)
        st.success("SMS reminders scheduled!")


    # ---------- Readability ----------
    st.subheader("Readability Score")
    st.write(readability)

    # ---------- Footer ----------
    st.info(medical_disclaimer())
    st.caption(get_citations())
