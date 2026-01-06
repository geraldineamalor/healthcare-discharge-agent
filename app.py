import streamlit as st
from services.simplifier import simplify_text
from services.action_plan import create_action_plan
from services.danger_alerts import detect_dangers
from services.reminders import create_reminders
from evaluation.readability import get_readability
from utils.disclaimers import medical_disclaimer
from utils.citations import get_citations

st.set_page_config(page_title="Discharge Instruction Simplifier")

st.title("🏥 Discharge Instruction Simplifier & Follow-Up Agent")

input_text = st.text_area("Paste Discharge Instructions")

if st.button("Simplify Instructions"):
    simplified = simplify_text(input_text)
    plan = create_action_plan(input_text)
    alerts = detect_dangers(input_text)
    reminders = create_reminders(input_text)
    readability = get_readability(simplified)

    st.subheader("📄 Simplified Instructions")
    st.write(simplified)

    st.subheader("📅 Action Plan")
    st.json(plan)

    st.subheader("⚠️ Danger Signs")
    st.write(alerts)

    st.subheader("⏰ Follow-Up Reminders")
    st.json(reminders)

    st.subheader("📊 Readability Score")
    st.write(readability)

    st.info(medical_disclaimer())
    st.caption(get_citations())
