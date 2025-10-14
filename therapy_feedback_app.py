import streamlit as st
from io import BytesIO
from docx import Document
from datetime import datetime

st.set_page_config(page_title="Therapy Feedback Form", layout="centered")

# -------------------------------
# Helper: Generate Word doc
# -------------------------------
def make_docx(responses, title="Therapy Feedback Summary"):
    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')} (UTC)\n")

    doc.add_paragraph("Summary for Therapists:", style="Intense Quote")
    doc.add_paragraph(
        "This document compiles client feedback. Likert values (1–5) reflect selected ratings. "
        "Blank answers indicate skipped questions."
    )
    doc.add_paragraph()

    for section, qas in responses.items():
        if not qas:
            continue
        doc.add_heading(section, level=2)
        for q, a in qas.items():
            if a is None or str(a).strip() == "":
                continue
            p = doc.add_paragraph()
            p.add_run(f"{q}: ").bold = True
            p.add_run(str(a))
        doc.add_paragraph()

    doc.add_paragraph("Note: Only answered questions and selected sections are included.")
    f = BytesIO()
    doc.save(f)
    f.seek(0)
    return f.read()

# -------------------------------
# Initialize session state
# -------------------------------
if "responses" not in st.session_state:
    st.session_state["responses"] = {
        "Overall Experience": {},
        "Topics & Comfort": {},
        "Structure & Style": {},
        "Relational Climate": {},
        "Therapy Harm & Boundaries": {},
        "Feedback & Follow-Up Preferences": {},
        "Wrap-Up — Safety & Options": {}
    }

responses = st.session_state["responses"]

# -------------------------------
# Introduction
# -------------------------------
st.title("Therapy Feedback Form")
st.markdown(
    "This form is designed to help you reflect on your therapy experiences and think about feedback you might want to share with your therapist. "
    "All questions are optional, and at the end you can choose to download a summary of your responses to some or all of the form sections.\n\n"
    "If you have questions or feedback about this form, please contact sambrandsen7@gmail.com.\n\n"
    "**Note:** Each section must be saved individually before generating your summary."
)
st.markdown("---")

# -------------------------------
# Section 0: Entry Point
# -------------------------------
st.header("Section 0 — Entry Point")

focus = st.radio(
    "Which areas would you like this form to focus on today?",
    ("General Feedback", "Concerns, Discomfort, or Harm", "Both"),
    key="entry_focus"
)

style = st.radio(
    "Preferred style of questions/prompts:",
    options=["Structured", "Unstructured"],
    format_func=lambda s: "Includes Likert scales and structured prompts"
        if s == "Structured" else "Focuses on open-ended reflection",
    key="entry_style"
)

st.markdown("---")

super_optional = focus == "Concerns, Discomfort, or Harm"

# -------------------------------
# Section 1: Overall Experience
# -------------------------------
st.header("Section 1 — Overall Experience")
st.subheader("General Feedback")

if focus in ["General Feedback", "Both"]:
    with st.form("overall_form"):
        if style == "Structured":
            rating = st.selectbox(
                "Overall, how well is therapy meeting your needs? (1–5)",
                options=["", 1, 2, 3, 4, 5],
                index=0
            )
            enjoy = st.text_area("Anything you especially enjoy or hope continues?", height=100)
            stress = st.text_area("Anything stressful, uncomfortable, or less effective?", height=100)
        else:  # Unstructured
            rating = None
            enjoy = st.text_area("What are areas of therapy that feel especially helpful?")
            stress = st.text_area("What is something that feels difficult or could be improved?")
        additional_comments_oe = st.text_area("Additional comments / clarifications for this section")
        submitted = st.form_submit_button("Save Section")
        if submitted:
            responses["Overall Experience"] = {
                "Overall rating (1–5)": rating,
                "What to continue/what is going well": enjoy,
                "Stressful / less effective": stress,
                "Overall Experience — Additional comments": additional_comments_oe
            }
            st.success("Saved Overall Experience.")

# -------------------------------
# Section 2: Topics & Comfort
# -------------------------------
with st.expander("Section 2 — Topics & Comfort"):
    with st.form("topics_form"):
        easy = st.text_area("What topics are easy to discuss with your therapist?")
        hard = st.text_area("What topics are more challenging to discuss with your therapist?")
        hesitant = st.text_area("Are there any topics you’ve been hesitant to bring up?")
        training = st.text_area("Are there any trainings or resources you wish your therapist would become familiar with?")
        additional_comments_tc = st.text_area("Additional comments / clarifications for this section")
        submitted = st.form_submit_button("Save Section")
        if submitted:
            responses["Topics & Comfort"] = {
                "Topics that are easy to discuss": easy,
                "Topics that are harder to discuss in therapy": hard,
                "Topics I have been hesitant to bring up": hesitant,
                "Trainings or resources I wish my therapist would consider": training,
                "Topics & Comfort — Additional comments": additional_comments_tc
            }
            st.success("Saved Topics & Comfort.")

# -------------------------------
# Section 3: Structure & Style
# -------------------------------
with st.expander("Section 3 — Structure & Style"):
    with st.form("style_form"):
        punctuality = st.selectbox("Punctuality/scheduling is a source of stress (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        disclosure = st.selectbox("Therapist self-disclosure", ["", "Too little", "Just right", "Too much"], index=0)
        disclosure_text = st.text_area("Comments on self-disclosure")
        structure = st.selectbox("Session structure/flexibility", ["", "Too rigid", "Balanced", "Too flexible"], index=0)
        structure_text = st.text_area("Comments on session structure")
        comm_style = st.text_area("Communication style")
        autonomy = st.selectbox("Autonomy vs compliance/masking (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        additional_comments_ss = st.text_area("Additional comments / clarifications for this section")
        submitted = st.form_submit_button("Save Section")
        if submitted:
            responses["Structure & Style"] = {
                "Punctuality is a source of stress": punctuality,
                "Self-disclosure": disclosure,
                "Self-disclosure comments": disclosure_text,
                "Session structure": structure,
                "Session structure comments": structure_text,
                "Communication style": comm_style,
                "Autonomy vs masking": autonomy,
                "Structure & Style — Additional comments": additional_comments_ss
            }
            st.success("Saved Structure & Style.")

# -------------------------------
# Section 4: Relational Climate
# -------------------------------
with st.expander("Section 4 — Relational Climate"):
    with st.form("rel_form"):
        safe = st.selectbox("I feel safe, respected, and understood (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        honest = st.selectbox("I feel comfortable being honest (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        post_session = st.multiselect("After sessions, I usually feel:", ["Calm","Relieved","Overwhelmed","Confused","Hopeful","Worse"], default=[])
        stress_signs = st.text_area("Signs of stress or overwhelm")
        stress_help = st.text_area("What helps most when stressed?")
        additional_comments_rc = st.text_area("Additional comments / clarifications for this section")
        submitted = st.form_submit_button("Save Section")
        if submitted:
            responses["Relational Climate"] = {
                "Safe rating": safe,
                "Honest rating": honest,
                "Post-session feelings": post_session,
                "Stress signs": stress_signs,
                "Stress helps": stress_help,
                "Relational Climate — Additional comments": additional_comments_rc
            }
            st.success("Saved Relational Climate.")

# -------------------------------
# Section 5: Therapy Harm & Boundaries
# -------------------------------
with st.expander("Section 5 — Therapy Harm & Boundaries"):
    with st.form("harm_form"):
        felt_friend = st.selectbox("I sometimes feel like my therapist treats me more like a friend than a client (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        self_disclosure = st.selectbox("I sometimes feel uncomfortable with how much my therapist shares about themselves (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        physical_contact = st.selectbox("I feel confused or hurt about physical contact with my therapist (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        dual_roles = st.selectbox("Dual roles with therapist (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        blurred_boundaries = st.selectbox("Times therapist blurred boundaries (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        dismissed_rating = st.selectbox("I sometimes feel dismissed or unheard by my therapist (1–5)", ["",1,2,3,4,5], index=0)
        impact = st.text_area("Anything you'd like your clinician to know about impact?")
        meaningful_response = st.text_area("What acknowledgement or response would feel meaningful?")
        misunderstood_feedback = st.text_area("Ways feedback was misunderstood?")
        feedback_worries = st.text_area("Ways feedback might be misunderstood now?")
        stigmatized_text = st.text_area("Has your therapist ever been insensitive about your identity or other aspects of your experience? Please explain.")
        open_reflection = st.text_area("Anything else about harm, safety, or boundaries?")
        additional_comments_thb = st.text_area("Additional comments / clarifications for this section")
        submitted = st.form_submit_button("Save Section")
        if submitted:
            responses["Therapy Harm & Boundaries"] = {
                "Felt like friend vs client (1–5)": felt_friend,
                "Feeling of confusion over self-disclosure (1–5)": self_disclosure,
                "Feeling of confusion over physical contact (1–5)": physical_contact,
                "Dual roles (1–5)": dual_roles,
                "Blurred boundaries (1–5)": blurred_boundaries,
                "Feeling dismissed or unheard (1–5)": dismissed_rating,
                "Impact on client": impact,
                "Meaningful acknowledgement": meaningful_response,
                "Misunderstood feedback": misunderstood_feedback,
                "Therapist insensitivity / stigmatization": stigmatized_text,
                "Open reflection": open_reflection,
                "Therapy Harm & Boundaries — Additional comments": additional_comments_thb
            }
            st.success("Saved Therapy Harm & Boundaries.")

# -------------------------------
# Section 6: Feedback & Follow-Up Preferences
# -------------------------------
with st.expander("Section 6 — Feedback & Follow-Up Preferences"):
    with st.form("feedback_form"):
        checkin_methods = st.multiselect(
            "How would you like your therapist to check in with you about sessions/comfort?",
            ["In-session", "Written follow-up", "None", "Share planned changes", "Other"],
            default=[]
        )
        checkin_comments = st.text_area("Additional notes on follow-up")
        explore_other = st.text_area("Would you like to explore other ways to address concerns?")
        additional_comments_ffp = st.text_area("Additional comments / clarifications for this section")
        submitted = st.form_submit_button("Save Section")
        if submitted:
            responses["Feedback & Follow-Up Preferences"] = {
                "Check-in methods": checkin_methods,
                "Check-in notes": checkin_comments,
                "Explore other ways": explore_other,
                "Feedback & Follow-Up Preferences — Additional comments": additional_comments_ffp
            }
            st.success("Saved Feedback & Follow-Up Preferences.")

# -------------------------------
# Section 7: Wrap-Up — Safety & Options
# -------------------------------
st.header("Section 7 — Wrap-Up: Safety & Options")
st.markdown(
    "You are welcome to fill this section and share it with your therapist, "
    "or simply use it as a personal reflection tool to help decide whether you feel safe giving feedback."
)
with st.form("wrapup_form"):
    sharing_options = st.multiselect(
        "How are you planning on sharing your feedback?",
        ["Read aloud in session", "Share via email / PDF", "Keep private", "Other"],
        default=[]
    )
    comfort_level = st.selectbox(
        "How do you feel about sharing this feedback?",
        ["", "Comfortable", "Unsure", "Unsafe"],
        index=0
    )
    reactions_reflection = st.text_area("What reactions from your therapist might feel manageable vs harmful?", height=100)
    support_access = st.text_area("Supports you can access before/after sharing", height=100)
    explore_restoration = st.text_area(
        "Would you like to explore other avenues for restoration or resolution, such as third-party facilitation?"
    )
    additional_comments_wrap = st.text_area("Additional comments / clarifications for this section")
    submitted = st.form_submit_button("Save Section")
    if submitted:
        responses["Wrap-Up — Safety & Options"] = {
            "Sharing options": sharing_options,
            "Comfort level": comfort_level,
            "Therapist reactions reflection": reactions_reflection,
            "Support access": support_access,
            "Explore restoration options": explore_restoration,
            "Wrap-Up — Additional comments": additional_comments_wrap
        }
        st.success("Saved Wrap-Up section.")

# -------------------------------
# Download Summary
# -------------------------------
st.markdown("---")
st.header("Create and Download Summary")
include_sections = st.multiselect(
    "Select sections to include in the summary:",
    list(responses.keys()),
    default=list(responses.keys())
)

filtered = {sec: responses[sec] for sec in include_sections if responses[sec]}

if st.button("Generate Word Summary"):
    if not filtered:
        st.warning("No responses yet! Please save at least one section.")
    else:
        docx_bytes = make_docx(filtered)
        st.session_state["docx_bytes"] = docx_bytes
        st.success("Summary generated!")

if "docx_bytes" in st.session_state:
    st.download_button(
        "Download .docx",
        data=st.session_state["docx_bytes"],
        file_name="therapy_feedback_summary.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.caption(
    "All questions are optional. You can expand sections as you wish and download your responses as a summary file at the end."
)

