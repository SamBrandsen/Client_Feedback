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

    doc.add_paragraph(
        "Summary for Therapists:\n"
        "This document compiles client feedback from the therapy reflection tool. "
        "All responses are provided as entered by the client. "
        "Only answered questions are included. Likert values (1–5) reflect selected ratings. "
        "Blank answers are excluded."
    )
    doc.add_paragraph()

    for i, (section, qas) in enumerate(responses.items(), start=1):
        if not qas:
            continue
        doc.add_heading(f"Section {i}: {section}", level=2)
        for q, a in qas.items():
            if a is None or (isinstance(a, list) and len(a) == 0) or str(a).strip() == "":
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
# Initialize session state & all variables
# -------------------------------
if "responses" not in st.session_state:
    st.session_state["responses"] = {}

# Initialize all variables to None
rating = enjoy = stress = additional_comments_oe = None
easy = hard = hesitant = training = additional_comments_tc = None
punctuality = disclosure = disclosure_text = structure = structure_text = comm_style = autonomy = session_frequency = directive_preferences = additional_comments_ss = None
safe = honest = post_session = stress_signs = stress_help = additional_comments_rc = None
felt_friend = self_disclosure = physical_contact = dual_roles = blurred_boundaries = dismissed_rating = impact = meaningful_response = financial_concerns = attachment_highs_lows = stigmatized_text = open_reflection = additional_comments_thb = None
checkin_methods = checkin_comments = explore_other = additional_comments_ffp = None
feedback_emotions = feedback_fears = ideal_usage = open_wrap_up = None

# -------------------------------
# Introduction — with test mode notice
# -------------------------------
st.title("Therapy Feedback Form")
st.warning("⚠️ This is an experimental / early version of the tool.")
st.markdown("""
This form helps you reflect on your therapy experiences — what’s working, what feels hard, and what you might want to share. 
All questions are optional and only answered questions will appear in the final download. 
You can answer as many or as few as you like, and save everything at the end using the **“Save All Sections”** button.
""")
st.info("💡 Your responses are only stored locally in your browser session. They are **not uploaded or sent anywhere**.")
st.markdown("---")

# -------------------------------
# Section 0 — Entry Point
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
        if s == "Structured" else "Focuses on short open-ended reflection",
    key="entry_style"
)
st.markdown("---")
harm_expanded = focus in ["Concerns, Discomfort, or Harm", "Both"]

# -------------------------------
# Section 1 — Overall Experience
# -------------------------------
st.header("Section 1 — Overall Experience")
if focus in ["General Feedback", "Both"]:
    if style == "Structured":
        rating = st.selectbox("Overall, how well is therapy meeting your needs? (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        enjoy = st.text_area("Anything you especially enjoy or hope continues?", height=100)
        stress = st.text_area("Anything stressful, uncomfortable, or less effective?", height=100)
    else:
        enjoy = st.text_area("What is helpful about therapy?", height=100)
        stress = st.text_area("What feels difficult or could be improved?", height=100)
    additional_comments_oe = st.text_area("Additional comments / clarifications for this section", key="additional_comments_oe")

# -------------------------------
# Section 2 — Topics & Comfort
# -------------------------------
with st.expander("Section 2 — Topics & Comfort"):
    if style == "Structured":
        easy = st.text_area("What topics are easy to discuss with your therapist?")
        hard = st.text_area("What topics are more challenging to discuss?")
        hesitant = st.text_area("Any topics you’ve been hesitant to bring up?")
        training = st.text_area("Trainings or resources you wish your therapist knew about?")
    else:
        easy = st.text_area("Topics you feel comfortable discussing?")
        hard = st.text_area("Topics that feel difficult?")
    additional_comments_tc = st.text_area("Additional comments / clarifications for this section", key="additional_comments_tc")

# -------------------------------
# Section 3 — Structure & Style
# -------------------------------
with st.expander("Section 3 — Structure & Style"):
    if style == "Structured":
        punctuality = st.selectbox("Punctuality/scheduling is a source of stress (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        disclosure = st.selectbox(
            "Therapist self-disclosure",
            ["", "Would prefer less self-disclosure",
             "The current amount of self-disclosure is good",
             "Would prefer more self-disclosure",
             "I am unsure or have conflicting feelings about self-disclosure"], index=0
        )
        disclosure_text = st.text_area("Comments on self-disclosure")
        structure = st.selectbox(
            "Session structure/flexibility",
            ["", "Would prefer more flexibility",
             "The current balance of structure/flexibility is good",
             "Would prefer more structure",
             "I am uncertain or have conflicting feelings about session structure/flexibility"], index=0
        )
        structure_text = st.text_area("Comments on session structure")
        comm_style = st.text_area("Communication style")
        autonomy = st.selectbox("How well does therapy support your autonomy/ability to be yourself?", ["", 1, 2, 3, 4, 5], index=0)
        session_frequency = st.text_area("Thoughts on therapist availability or session frequency?")
        directive_preferences = st.text_area("Areas you wish therapist were more or less directive/proactive?")
    else:
        enjoy = st.text_area("How do you experience the structure of sessions?")
        stress = st.text_area("Anything you’d like to change about structure or therapist style?")
    additional_comments_ss = st.text_area("Additional comments / clarifications for this section", key="additional_comments_ss")

# -------------------------------
# Section 4 — Relational Climate
# -------------------------------
with st.expander("Section 4 — Relational Climate"):
    if style == "Structured":
        safe = st.selectbox("I feel safe, respected, and understood (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        honest = st.selectbox("I feel comfortable being honest (1–5)", ["", 1, 2, 3, 4, 5], index=0)
        post_session = st.multiselect("Overall emotional experiences after sessions (check all that apply)",
                                      ["Calm","Relieved","Overwhelmed","Confused","Hopeful","Worse"], default=[])
        stress_signs = st.text_area("Signs you notice if you start to feel stressed during a session")
        stress_help = st.text_area("What helps most when stressed during or after a session?")
    else:
        post_session = st.text_area("Emotional experiences after sessions?")
        stress_help = st.text_area("What helps when stressed during/after sessions?")
    additional_comments_rc = st.text_area("Additional comments / clarifications for this section", key="additional_comments_rc")

# -------------------------------
# Section 5 — Therapy Harm & Boundaries
# -------------------------------
with st.expander("Section 5 — Therapy Harm & Boundaries", expanded=harm_expanded):
    if style == "Structured":
        felt_friend = st.selectbox("I sometimes feel like my therapist treats me more like a friend than a client (1–5)", ["",1,2,3,4,5], index=0)
        self_disclosure = st.selectbox("I sometimes feel uncomfortable with how much my therapist shares (1–5)", ["",1,2,3,4,5], index=0)
        physical_contact = st.selectbox("I feel confused or hurt about physical contact (1–5)", ["",1,2,3,4,5], index=0)
        dual_roles = st.text_area("Dual roles: overlap in social/professional contexts?")
        blurred_boundaries = st.text_area("Any confusing moments regarding boundaries that affected you?")
        dismissed_rating = st.selectbox("I sometimes feel dismissed or unheard (1–5)", ["",1,2,3,4,5], index=0)
        impact = st.text_area("Impact of these experiences")
        meaningful_response = st.text_area("What acknowledgement or response would feel meaningful?")
        financial_concerns = st.text_area("Any financial concerns (e.g., overbilling, pressured sessions)?")
        attachment_highs_lows = st.text_area("Moments of intense emotional highs/lows or confusing attachment feelings?")
        stigmatized_text = st.text_area("Insensitive behavior regarding identity or experience?")
        open_reflection = st.text_area("Anything else about harm, safety, or boundaries?")
    else:
        open_reflection = st.text_area("Any experiences of concern, harm, or boundary issues you want to note?")
    additional_comments_thb = st.text_area("Additional comments / clarifications for this section", key="additional_comments_thb")

# -------------------------------
# Section 6+7 — Feedback, Wrap-Up, Safety & Options
# -------------------------------
with st.expander("Section 6 — Feedback & Wrap-Up"):
    if style == "Structured":
        ideal_usage = st.multiselect(
            "How would you ideally like your therapist to use this feedback?",
            ["Discuss in session", "Read privately", "Acknowledge through email", "Share how they plan to make changes", "Other"], default=[]
        )
        feedback_emotions = st.multiselect(
            "Emotions when sharing feedback (select all that apply)",
            ["Comfortable","Nervous","Afraid","Uncertain","Relieved","Secure","Conflicted","Feeling guilt"], default=[]
        )
        feedback_fears = st.multiselect(
            "Any fears about sharing feedback (select all that apply)",
            ["Receiving a defensive response","Loss of connection or regard","Being forced into other treatment","Therapist ends therapy","Other"], default=[]
        )
        open_wrap_up = st.text_area("Additional thoughts or clarifications about sharing feedback / supports")
    else:
        open_wrap_up = st.text_area("Any thoughts about sharing feedback or support needs?")
        
# -------------------------------
# Save All Sections
# -------------------------------
st.markdown("---")
if st.button("💾 Save All Sections"):
    st.session_state["responses"] = {
        "Overall Experience": {
            "Overall rating (1–5)": rating,
            "What to continue / what is going well": enjoy,
            "Stressful / less effective": stress,
            "Additional comments": additional_comments_oe
        },
        "Topics & Comfort": {
            "Topics easy to discuss": easy,
            "Topics harder to discuss": hard,
            "Hesitant topics": hesitant,
            "Desired trainings/resources": training,
            "Additional comments": additional_comments_tc
        },
        "Structure & Style": {
            "Punctuality stress": punctuality,
            "Self-disclosure": disclosure,
            "Disclosure comments": disclosure_text,
            "Session structure": structure,
            "Structure comments": structure_text,
            "Communication style": comm_style,
            "Autonomy vs masking": autonomy,
            "Therapist availability / frequency": session_frequency,
            "Directive/proactive preferences": directive_preferences,
            "Additional comments": additional_comments_ss
        },
        "Relational Climate": {
            "Safe rating": safe,
            "Honesty rating": honest,
            "Post-session feelings": post_session,
            "Stress signs": stress_signs,
            "What helps when stressed": stress_help,
            "Additional comments": additional_comments_rc
        },
        "Therapy Harm & Boundaries": {
            "Felt like friend vs client (1–5)": felt_friend,
            "Uncomfortable self-disclosure (1–5)": self_disclosure,
            "Physical contact confusion (1–5)": physical_contact,
            "Dual roles": dual_roles,
            "Blurred/confusing boundaries": blurred_boundaries,
            "Feeling dismissed/unheard (1–5)": dismissed_rating,
            "Impact": impact,
            "Meaningful acknowledgement": meaningful_response,
            "Financial concerns": financial_concerns,
            "Attachment/highs-lows": attachment_highs_lows,
            "Therapist insensitivity": stigmatized_text,
            "Open reflection": open_reflection,
            "Additional comments": additional_comments_thb
        },
        "Feedback & Wrap-Up": {
            "Ideal usage of feedback": ideal_usage,
            "Emotions when sharing feedback": feedback_emotions,
            "Fears about sharing feedback": feedback_fears,
            "Additional notes": open_wrap_up
        }
    }
    st.success("✅ All sections saved!")

# -------------------------------
# Download Summary
# -------------------------------
st.markdown("---")
st.header("Create and Download Summary")
st.markdown(
    "Thank you for taking the time to use this tool! Please check your download to ensure "
    "answers appear and are formatted as desired."
)
include_sections = st.multiselect("Select sections to include:", list(st.session_state["responses"].keys()), default=list(st.session_state["responses"].keys()))
filtered = {sec: st.session_state["responses"][sec] for sec in include_sections if st.session_state["responses"][sec]}

if st.button("Generate Word Summary"):
    if not filtered:
        st.warning("No responses yet! Please fill and save sections first.")
    else:
        docx_bytes = make_docx(filtered)
        st.session_state["docx_bytes"] = docx_bytes
        st.success("Summary generated!")

if "docx_bytes" in st.session_state:
    filename = f"therapy_feedback_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.docx"
    st.download_button(
        "⬇️ Download Word Summary",
        data=st.session_state["docx_bytes"],
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.caption("All responses remain local to your browser until you download them.")

