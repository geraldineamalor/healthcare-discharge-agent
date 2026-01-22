import streamlit as st

from services.simplifier import simplify_text
from services.action_plan import create_action_plan
from services.reminders import create_reminders
from evaluation.readability import get_readability
from utils.disclaimers import medical_disclaimer
from utils.citations import get_citations
from services.care_type import is_chronic_care
from services.sms_scheduler import schedule_medication_sms
from services.duration_utils import extract_medications
from services.agent_reasoning import generate_agent_reasoning


# RAG imports (NOTE: no loader, no vector_store here)
from services.rag.loader import load_knowledge_base
from services.rag.retriever import retrieve_relevant_docs
from services.rag.danger_generator import generate_danger_signs
from services.rag.guidance_generator import generate_guidance

# --- Session state for scheduled SMS preview ---
if "scheduled_sms" not in st.session_state:
    st.session_state.scheduled_sms = []

st.set_page_config(page_title="Discharge Instruction Simplifier")
st.markdown("""
    <style>

    /* App background */
    body {
        background-color: #F7FAFC;
    }

    /* Main title */
    h1 {
        color: #0F766E;
        font-weight: 700;
    }

    /* Section headings */
    h2, h3 {
        color: #115E59;
    }

    /* Button styling */
    .stButton > button {
        background-color: #0F766E;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1.5em;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        background-color: #134E4A;
    }

    /* Info / Success / Warning boxes */
    .stAlert-success {
        background-color: #ECFDF5;
        border-left: 6px solid #10B981;
    }

    .stAlert-warning {
        background-color: #FFFBEB;
        border-left: 6px solid #F59E0B;
    }

    .stAlert-error {
        background-color: #FEF2F2;
        border-left: 6px solid #EF4444;
    }

    /* Expander styling */
    details summary {
        font-weight: 600;
        color: #0F766E;
    }

    </style>
    """, unsafe_allow_html=True)


st.markdown("## 🏥 Your Discharge Care Assistant")
st.caption(
    "We help you understand your discharge instructions, track daily care, and stay safe during recovery."
)

with st.container(border=True):
    st.markdown("### 📋 Paste Your Discharge Instructions")
    st.caption("You can copy this from your hospital discharge summary.")
    input_text = st.text_area(
        label="",
        placeholder="Paste discharge instructions here...",
        height=180
    )

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Simplify Instructions"):
    st.session_state.submitted = True

if st.session_state.submitted:

    # ---------- Core Processing ----------
    simplified = simplify_text(input_text)
    plan = create_action_plan(input_text)
    reminders = create_reminders(input_text)
    readability = get_readability(simplified)


    care_classification = (
        "Chronic Care" if is_chronic_care(input_text) else "Acute Care"
    )

    # ---------- Load & Retrieve RAG Context ----------
    retrieved_docs = retrieve_relevant_docs(input_text)

    danger_signs = generate_danger_signs(retrieved_docs)
    care_guidance, lifestyle_guidance = generate_guidance(retrieved_docs)


    # ---------- Care Classification ----------
    st.subheader("🩺 Your Care Type")
    if care_classification == "Chronic Care":
        st.success("🟢 Chronic Care: Long-term management")
    else:
        st.warning("🟡 Acute Care: Short-term recovery")

    # ---------- Simplified Instructions ----------
    with st.container(border=True):
        st.subheader("📄 Simplified Instructions")
        st.write(simplified)
    medications = extract_medications(input_text)

    if medications:
        with st.container(border=True):
            st.subheader("💊 Detected Medications")

            for med in medications:
                st.markdown(
                    f"- **{med['name']}**: {med['frequency']} for {med['days']} days"
                )
    agent_reasoning = generate_agent_reasoning(
        medications=medications,
        action_plan=plan,
        care_type=care_classification,
        reminders=reminders
    )

 

    # ---------- RAG-Based Guidance ----------
    with st.container(border=True):
        st.subheader("🧠 Condition-Specific Care Guidance")

        if care_guidance:
            st.markdown("**Care Instructions:**")
            for item in care_guidance:
                st.markdown(f"- {item}")

        if lifestyle_guidance:
            st.markdown("**Lifestyle & Activity Advice:**")
            for item in lifestyle_guidance:
                st.markdown(f"- {item}")

    # ---------- Action Plan ----------
    st.subheader("📅 Your Daily Care Plan")
    st.caption(
        "Complete tasks as recommended. Your care plan adjusts automatically based on duration."
    )


    if care_classification == "Chronic Care":
        for task in plan.get("Daily Routine", []):
            st.checkbox(task, disabled=True)

    else:
        with st.expander("📅 View Your Daily Care Plan", expanded=True):
            total, completed = 0, 0

            day_keys = sorted(
                [k for k in plan.keys() if k.startswith("Day ")],
                key=lambda x: int(x.split(" ")[1])
            )

            time_order = ["Morning", "Afternoon", "Evening"]

            for day in day_keys:
                st.markdown(f"### {day}")
                tasks = plan[day]

                for time in time_order:
                    if time not in tasks:
                        continue

                    for idx, task in enumerate(tasks[time]):
                        key = f"{day}-{time}-{idx}"
                        checked = st.checkbox(f"{time}: {task}", key=key)

                        total += 1
                        if checked:
                            completed += 1

                st.divider()

            if total > 0:
                st.progress(completed / total)
            if completed == total and total > 0:
                st.success("✅ All prescribed tasks are completed. Great job!")
    with st.expander("🧠 How Your Care Was Planned"):
        for line in agent_reasoning:
            if line == "":
                st.markdown("---")
            else:
                st.markdown(line)


    # ---------- RAG-Based Danger Signs ----------
    with st.container(border=True):
        st.subheader("⚠️ When to Seek Medical Help")
        st.caption(
            "Most patients recover smoothly. These signs are listed so you know when to seek help."
        )

        if danger_signs:
            for sign in danger_signs:
                st.markdown(f"- {sign}")
        else:
            st.markdown(
                "- Seek medical attention if symptoms worsen or new symptoms appear."
            )


    # ---------- Follow-Up Reminders ----------
    with st.container(border=True):
        st.subheader("⏰ Follow-Up Reminders")
        st.json(reminders)

    # ---------- SMS Reminders ----------
    phone = st.text_input("Enter phone number for SMS reminders")

    if st.button("Enable SMS Reminders"):
        scheduled = schedule_medication_sms(plan, phone)
        st.session_state.scheduled_sms = scheduled
        st.success("SMS reminders scheduled!")

    if st.session_state.scheduled_sms:
        with st.container(border=True):
            st.subheader("📨 Scheduled SMS Reminders")

            for sms in st.session_state.scheduled_sms:
                st.markdown(
                    f"**{sms['day']} ({sms['date']}) – {sms['time']}**  \n"
                    f"{sms['task']}"
                )


    # ---------- Readability ----------
    st.subheader("📊 Readability Score")
    st.write(readability)
    st.caption("This tool assists patients in understanding discharge instructions. It does not replace medical advice.")
    # ---------- Footer ----------
    st.info(medical_disclaimer())
    st.caption(get_citations())
