import streamlit as st
from io import BytesIO
from docx import Document
from datetime import datetime

st.set_page_config(page_title="Therapy Feedback — Persistent", layout="centered")

# -------------------------------------------------------------------
# Helper function: Generate Word document
# -------------------------------------------------------------------
def make_docx(responses, title="Therapy Feedback Summary"):
    doc = Document()
    
    # Title + generated time
    doc.add_heading(title, level=1)
    doc.add_paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')} (UTC)")
    doc.add_paragraph()
    
    # Therapist summary intro
    doc.add_paragraph("Summary for Therapists:", style="Intense Quote")
    doc.add_paragraph(
        "This document compiles client feedback collected through the Therapy Feedback App. "
        "Responses are grouped by topic. Likert scale values (1–5) reflect the client’s selected ratings, "
        "while written comments provide context or examples. Blank responses indicate questions the client "
        "chose to skip."
    )
    doc.add_paragraph()
    
    # Add responses by section
    for section, qas in responses.items():
        if not qas:
            continue
        doc.add_heading(section, level=2)
        for q, a in qas.items():
            if not a or str(a).strip() == "":
                continue
            p = doc.add_paragraph()
            p.add_run(f"{q}: ").bold = True
            p.add_run(str(a))
        doc.add_paragraph()
    
    # Footer note
    doc.add_paragraph(
        "Note: This summary includes only answered questions "
        "and sections the user chose to include."
    )
    
    f = BytesIO()
    doc.save(f)
    f.seek(0)
    return f.read()


# -------------------------------------------------------------------
# Initialize session state for responses
# -------------------------------------------------------------------
if "responses" not in st.session_state:
    st.session_state["responses"] = {
        "Therapy Harm & Boundaries": {},
        "Relational Approach": {}
    }

responses = st.session_state["responses"]

# -------------------------------------------------------------------
# App layout
# -------------------------------------------------------------------
st.title("Therapy Feedback — Persistent App")
st.caption("You can skip any question; blank responses won’t appear in the summary.")
st.markdown("---")

# Focus
focus = st.radio(
    "Which feedback area would you like to focus on today?",
    ("Therapy Harm & Boundaries", "Relational Approach", "Both"),
    key="focus"
)

# Feedback style
style = st.radio(
    "Preferred feedback style:",
    ("Broader prompts (2 open-ended questions)", "Specific (Likert + text)"),
    key="style"
)

st.divider()

# -------------------------------------------------------------------
# Section 1 — Therapy Harm & Boundaries
# -------------------------------------------------------------------
if focus in ["Therapy Harm & Boundaries", "Both"]:
    st.header("1 — Therapy Harm & Boundaries")
    
    if style.startswith("Broader"):
        with st.form(key="harm_form_broad"):
            harm_reflection = st.text_area(
                "What aspects of therapy have felt uncomfortable or potentially harmful, if any?",
                height=120
            )
            repair_reflection = st.text_area(
                "Have there been any moments of repair or improvement following discomfort?",
                height=120
            )
            submitted = st.form_submit_button("Save Section")
            if submitted:
                st.session_state["responses"]["Therapy Harm & Boundaries"] = {
                    "Potentially harmful aspects": harm_reflection,
                    "Repair or improvement moments": repair_reflection
                }
                st.success("Section saved.")
    else:
        with st.form(key="harm_form_specific"):
            harm_rating = st.selectbox(
                "I felt safe and respected during sessions (1–5, optional)",
                options=["", 1, 2, 3, 4, 5],
                index=0
            )
            feedback_rating = st.selectbox(
                "Therapist welcomed feedback about harm/discomfort (1–5, optional)",
                options=["", 1, 2, 3, 4, 5],
                index=0
            )
            harm_comments = st.text_area(
                "Describe any situations that felt unsafe, or where repair was needed (optional)",
                height=120
            )
            submitted = st.form_submit_button("Save Section")
            if submitted:
                st.session_state["responses"]["Therapy Harm & Boundaries"] = {
                    "Felt safe and respected (1–5)": harm_rating,
                    "Therapist welcomed feedback (1–5)": feedback_rating,
                    "Comments": harm_comments
                }
                st.success("Section saved.")

st.divider()

# -------------------------------------------------------------------
# Section 2 — Relational Approach
# -------------------------------------------------------------------
if focus in ["Relational Approach", "Both"]:
    st.header("2 — Relational Approach")
    
    if style.startswith("Broader"):
        with st.form(key="rel_form_broad"):
            connection_reflection = st.text_area(
                "How would you describe your connection with your therapist?",
                height=120
            )
            improvement_reflection = st.text_area(
                "What, if anything, might improve the sense of understanding or trust?",
                height=120
            )
            submitted = st.form_submit_button("Save Section")
            if submitted:
                st.session_state["responses"]["Relational Approach"] = {
                    "Connection with therapist": connection_reflection,
                    "Improvements for understanding/trust": improvement_reflection
                }
                st.success("Section saved.")
    else:
        with st.form(key="rel_form_specific"):
            warmth_rating = st.selectbox(
                "Therapist warmth and empathy (1–5, optional)",
                options=["", 1, 2, 3, 4, 5],
                index=0
            )
            honesty_rating = st.selectbox(
                "Comfort being honest with therapist (1–5, optional)",
                options=["", 1, 2, 3, 4, 5],
                index=0
            )
            rel_comments = st.text_area(
                "Any comments about how the relational approach feels?",
                height=120
            )
            submitted = st.form_submit_button("Save Section")
            if submitted:
                st.session_state["responses"]["Relational Approach"] = {
                    "Warmth and empathy (1–5)": warmth_rating,
                    "Comfort with honesty (1–5)": honesty_rating,
                    "Comments": rel_comments
                }
                st.success("Section saved.")

st.markdown("---")

# -------------------------------------------------------------------
# Download summary
# -------------------------------------------------------------------
st.header("Create and Download Summary")

include_sections = st.multiselect(
    "Select which sections to include in the summary:",
    list(st.session_state["responses"].keys()),
    default=list(st.session_state["responses"].keys())
)

filtered = {sec: st.session_state["responses"][sec] for sec in include_sections if st.session_state["responses"][sec]}

if st.button("Generate Word Summary"):
    if not any(filtered.values()):
        st.warning("No responses yet! Please save at least one section.")
    else:
        docx_bytes = make_docx(filtered)
        st.session_state["docx_bytes"] = docx_bytes
        st.success("Summary generated successfully!")

if "docx_bytes" in st.session_state:
    st.download_button(
        "Download .docx",
        data=st.session_state["docx_bytes"],
        file_name="therapy_feedback_summary.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.caption("This app can be expanded with additional sections or features as needed.")
