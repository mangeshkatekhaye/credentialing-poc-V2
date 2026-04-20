# app.py

import streamlit as st

# Imports
from models.schema import get_empty_form
from services.scenario_loader import load_scenario
from services.rule_engine import evaluate_rules, calculate_readiness
from services.progress_tracker import calculate_progress
from services.ai_validator import ai_validate


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Credentialing Workflow V2", layout="wide")
st.title("🧠 AI Credentialing Workflow (V2)")


# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "form_data" not in st.session_state:
    st.session_state.form_data = get_empty_form()

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None


# -------------------------------
# PROGRESS TRACKER (TOP)
# -------------------------------
progress = calculate_progress(st.session_state)

st.subheader("📈 Form Completion")
st.progress(progress / 100)
st.write(f"Completion: {progress}%")

st.info("📌 Completion shows how much data is filled. Submission readiness depends on mandatory credentials.")


# -------------------------------
# SIDEBAR — SCENARIO LOADER
# -------------------------------
st.sidebar.header("📂 Load Scenario")

scenario = st.sidebar.selectbox(
    "Select Scenario",
    ["None", "Complete", "Partial", "Incomplete"]
)

if st.sidebar.button("Load Scenario"):
    if scenario != "None":
        st.session_state.form_data = load_scenario(scenario.lower())

        for key, value in st.session_state.form_data.items():
            st.session_state[key] = value

        st.session_state.pdf_processed = True  # prevent unwanted reprocessing
        st.sidebar.success(f"{scenario} scenario loaded")
        st.rerun()


# -------------------------------
# SIDEBAR — PDF UPLOAD
# -------------------------------
st.sidebar.header("📄 Upload PDF")

uploaded_file = st.sidebar.file_uploader("Upload Credentialing PDF", type=["pdf"])


# 🔹 Detect new file upload
if uploaded_file:
    if uploaded_file != st.session_state.last_uploaded_file:
        st.session_state.pdf_processed = False
        st.session_state.last_uploaded_file = uploaded_file


# 🔹 Process PDF ONLY ONCE
if uploaded_file and not st.session_state.pdf_processed:

    from services.pdf_extractor import extract_text_from_pdf, extract_structured_data

    st.sidebar.info("Processing PDF...")

    with st.spinner("Extracting data from PDF..."):

        text = extract_text_from_pdf(uploaded_file)
        extracted_data = extract_structured_data(text)

        # Merge into form_data
        st.session_state.form_data.update(extracted_data)

        # Sync into UI fields
        for key, value in extracted_data.items():
            st.session_state[key] = value

    st.session_state.pdf_processed = True

    st.sidebar.success("Data extracted and form pre-filled!")
    st.warning("⚠️ Extracted data may not be 100% accurate. Please review before submission.")

    st.rerun()


# -------------------------------
# FORM UI (CAQH STYLE)
# -------------------------------
tabs = st.tabs([
    "SECTION 1 — Personal Info",
    "SECTION 2 — License",
    "SECTION 4 — Certification",
    "SECTION 6 — Practice",
    "SECTION 7 — Malpractice"
])


# SECTION 1
with tabs[0]:
    st.markdown("### SECTION 1 — PERSONAL & DEMOGRAPHIC INFORMATION")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("First Name", value=st.session_state.get("first_name", ""), key="first_name")
        st.text_input("Date of Birth", value=st.session_state.get("dob", ""), key="dob")
        st.text_input("Phone", value=st.session_state.get("phone", ""), key="phone")
        st.text_input("NPI", value=st.session_state.get("npi", ""), key="npi")

    with col2:
        st.text_input("Last Name", value=st.session_state.get("last_name", ""), key="last_name")
        st.text_input("Gender", value=st.session_state.get("gender", ""), key="gender")
        st.text_input("Email", value=st.session_state.get("email", ""), key="email")
        st.text_input("Specialty", value=st.session_state.get("specialty", ""), key="specialty")

    st.text_area("Address", value=st.session_state.get("address", ""), key="address")


# SECTION 2
with tabs[1]:
    st.markdown("### SECTION 2 — PROFESSIONAL IDENTIFIERS & LICENSES")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("License Number", value=st.session_state.get("license_number", ""), key="license_number")
        st.text_input("DEA Number", value=st.session_state.get("dea_number", ""), key="dea_number")

    with col2:
        st.text_input("License Expiry", value=st.session_state.get("license_expiry", ""), key="license_expiry")
        st.text_input("DEA Expiry", value=st.session_state.get("dea_expiry", ""), key="dea_expiry")


# SECTION 4
with tabs[2]:
    st.markdown("### SECTION 4 — BOARD CERTIFICATIONS")

    st.checkbox("Board Certified",
                value=st.session_state.get("board_certified", False),
                key="board_certified")

    if st.session_state.get("board_certified"):
        st.text_input("Board Certification Expiry",
                      value=st.session_state.get("board_expiry", ""),
                      key="board_expiry")


# SECTION 6
with tabs[3]:
    st.markdown("### SECTION 6 — PRACTICE INFORMATION")

    st.text_input("Practice Name",
                  value=st.session_state.get("practice_name", ""),
                  key="practice_name")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("TIN", value=st.session_state.get("tin", ""), key="tin")

    with col2:
        st.text_input("Medicaid ID", value=st.session_state.get("medicaid_id", ""), key="medicaid_id")


# SECTION 7
with tabs[4]:
    st.markdown("### SECTION 7 — MALPRACTICE INSURANCE")

    st.checkbox("Malpractice Insurance Available",
                value=st.session_state.get("malpractice_insurance", False),
                key="malpractice_insurance")

    if st.session_state.get("malpractice_insurance"):
        st.text_input("Policy Expiry",
                      value=st.session_state.get("malpractice_expiry", ""),
                      key="malpractice_expiry")


# -------------------------------
# SYNC SESSION → FORM DATA
# -------------------------------
for field in get_empty_form().keys():
    if field in st.session_state:
        st.session_state.form_data[field] = st.session_state[field]


# -------------------------------
# VALIDATION
# -------------------------------
st.divider()

if st.button("🚀 Validate Submission"):

    st.write("DEBUG DATA:", st.session_state.form_data)
    
    mandatory, high_risk = evaluate_rules(st.session_state.form_data)
    readiness = calculate_readiness(mandatory, high_risk)

    st.subheader("📊 Validation Results")
    st.metric("Submission Readiness", f"{readiness}%")

    if mandatory:
        st.error("🔴 Not Eligible for Submission (Mandatory fields missing)")
        for item in mandatory:
            st.write(f"- {item}")
    else:
        st.success("No Mandatory Issues")

    if high_risk:
        st.warning("⚠️ High-Risk Gaps")
        for item in high_risk:
            st.write(f"- {item}")
    else:
        st.success("No High-Risk Issues")

    st.divider()
    st.subheader("🤖 AI Validation Insights")

    if mandatory or high_risk:
        ai_feedback = ai_validate(
            text="Form Input Data",
            doc_type="Clinical Document",
            mandatory_missing=mandatory,
            high_risk_missing=high_risk
        )
        st.markdown(ai_feedback)
    else:
        st.success("No issues detected. Profile is ready for submission.")