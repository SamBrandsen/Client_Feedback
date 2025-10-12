import streamlit as st
from io import BytesIO
from docx import Document
from datetime import datetime

st.set_page_config(page_title="Client Feedback Form — Enhanced", layout="centered")

# --- Helper function to make DOCX ------------------------------------------
def make_docx(responses: dict, title: str = "Client Feedback Summary") -> bytes:
    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')} (UTC)")
    doc.add_paragraph()

    for section_title, items in responses.items():
        if not items:
            continue
        doc.add_heading(section_title, level=2)
        for q, a in items.items():
            if a is None or (isinstance(a, str) and a.strip() == ""):
                continue
            ans_text = ", ".join([str(x) for x in a if str(x).strip() != ""]) if isinstance(a, list) else str(a)
            doc.add_paragraph(f"Q: {q}", style='Intense Quote')
            doc.add_paragraph(ans_text)
        doc.add_paragraph()

    bio = doc.add_paragraph()
    bio.add_run("Note: This summary was created from user-selected responses. Questions and context were included only where the user provided answers or explicitly chose to include sections.")

    f = BytesIO()
    doc.save(f)
    f.seek(0)
    return f.read()

# --- App Layout -------------------------------------------------------------
st.title("Client Feedback Form — Enhanced")
st.caption("Use this form to reflect on your therapy experience. All questions are optional — you choose what to share.")
st.markdown("---")

# --- Section 0: Entry Point -----------------------------------------------
st.header("Start — choose your focus & style")
focus = st.radio("Which areas would you like this form to focus on today?", (
    "General Feedback", "Concerns, Discomfort, or Harm", "Both"
), key="entry_focus")

style = st.radio("Preferred feedback style:", (
    "Structured (Likert + text)",
    "Semi-structured (guided prompts)",
    "Free-flowing / Upload audio or long text"
), key="entry_style")

st.markdown("---")

super_optional = focus == "Concerns, Discomfort, or Harm"

# --- Section 1: Overall Experience ----------------------------------------
if focus in ["General Feedback", "Both"]:
    st.header("1 — Overall Experience")
    with st.form(key='overall_form'):
        if style.startswith("Structured"):
            st.session_state.setdefault("overall_rating", 3)
            st.session_state.setdefault("overall_text", "")
            st.session_state.setdefault("overall_issues", "")
            overall_rating = st.slider("Overall — how well is therapy meeting your needs?", 1, 5, st.session_state["overall_rating"], key="overall_rating")
            overall_text = st.text_area("Anything you especially enjoy or hope continues?", height=100, key="overall_text")
            overall_issues = st.text_area("Anything that felt stressful, uncomfortable, or less effective? (optional prompts)", height=100, key="overall_issues")
        elif style.startswith("Semi-structured"):
            st.session_state.setdefault("overall_rating_semi", 3)
            st.session_state.setdefault("overall_text_semi", "")
            st.session_state.setdefault("overall_issues_semi", "")
            overall_rating = st.slider("Overall — how well is therapy meeting your needs?", 1, 5, st.session_state["overall_rating_semi"], key="overall_rating_semi")
            overall_text = st.text_area("One thing that feels especially helpful:", key="overall_text_semi")
            overall_issues = st.text_area("One thing that feels difficult or could be improved:", key="overall_issues_semi")
        else:
            st.session_state.setdefault("overall_text_free", "")
            overall_rating = None
            overall_text = st.text_area("Share whatever you like about how therapy is going:", height=200, key="overall_text_free")
            overall_issues = None
        submitted = st.form_submit_button("Save answers")
        if submitted:
            st.session_state["overall_rating"] = overall_rating
            st.session_state["overall_text"] = overall_text
            st.session_state["overall_issues"] = overall_issues

if super_optional:
    st.info("You opted to focus on concerns/harm. Other sections are available below as optional if you'd like to add more.")
    if st.checkbox("Add general feedback about overall experience (optional)", key="overall_optin"):
        with st.form(key='overall_form_optin'):
            overall_rating_opt = st.slider("Overall — how well is therapy meeting your needs?", 1, 5, 3, key="overall_rating_opt")
            overall_text_opt = st.text_area("Anything you especially enjoy or hope continues?", height=100, key="overall_text_opt")
            overall_issues_opt = st.text_area("Anything that felt stressful, uncomfortable, or less effective? (optional prompts)", height=100, key="overall_issues_opt")
            submitted = st.form_submit_button("Save answers")
            if submitted:
                st.session_state["overall_rating"] = overall_rating_opt
                st.session_state["overall_text"] = overall_text_opt
                st.session_state["overall_issues"] = overall_issues_opt

# --- Section 2: Topics & Comfort ------------------------------------------
st.header("2 — Topics & Comfort")
topics_shown = True
if super_optional:
    if not st.checkbox("Discuss topics & comfort (optional)", key="topics_optin"):
        st.caption("Skip if you'd prefer not to reflect on this now")
        topics_shown = False

if topics_shown:
    with st.form(key='topics_form'):
        easy_topics = st.text_area("Topics that are easy to discuss (optional)", key="easy_topics")
        hard_topics = st.text_area("Topics that are more challenging (optional)", key="hard_topics")
        hesitant_topics = st.text_area("Topics you're hesitant to bring up (optional)", key="hesitant_topics")
        training_suggestions = st.text_area("Any training/education you'd suggest for clinicians? (optional)", key="training_suggestions")
        submitted = st.form_submit_button("Save answers")
        if submitted:
            st.session_state["easy_topics"] = easy_topics
            st.session_state["hard_topics"] = hard_topics
            st.session_state["hesitant_topics"] = hesitant_topics
            st.session_state["training_suggestions"] = training_suggestions

# --- Section 3: Structure & Style -----------------------------------------
st.header("3 — Structure & Style")
style_shown = True
if super_optional:
    if not st.checkbox("Reflect on session structure & style (optional)", key="style_optin"):
        st.caption("Skip if not relevant")
        style_shown = False

if style_shown:
    with st.form(key='style_form'):
        punctuality = st.slider("Punctuality/scheduling (1=poor, 5=excellent)", 1, 5, 4, key="punctuality")
        self_disclosure = st.select_slider("Therapist self-disclosure", options=["Too little", "Just right", "Too much"], value="Just right", key="self_disclosure")
        self_disclosure_text = st.text_area("Comments about self-disclosure (optional)", key="self_disclosure_text")
        session_structure = st.select_slider("Session structure/flexibility", options=["Rigid", "Balanced", "Very flexible"], value="Balanced", key="session_structure")
        session_structure_text = st.text_area("Comments about session structure (optional)", key="session_structure_text")
        communication_style = st.text_area("Communication style (optional)", key="communication_style")
        autonomy_masking = st.slider("Autonomy vs. compliance/masking", 1, 5, 3, key="autonomy_masking")
        submitted = st.form_submit_button("Save answers")
        if submitted:
            st.session_state.update({
                "punctuality": punctuality,
                "self_disclosure": self_disclosure,
                "self_disclosure_text": self_disclosure_text,
                "session_structure": session_structure,
                "session_structure_text": session_structure_text,
                "communication_style": communication_style,
                "autonomy_masking": autonomy_masking
            })

# --- Section 4: Relational Climate ----------------------------------------
st.header("4 — Relational Climate")
rel_shown = True
if super_optional:
    if not st.checkbox("Reflect on relational climate (optional)", key="rel_optin"):
        st.caption("Skip if not relevant")
        rel_shown = False

if rel_shown:
    with st.form(key='rel_form'):
        safe_rating = st.slider("I feel safe, respected, and understood in therapy (1-5)", 1, 5, 4, key="safe_rating")
        honest_rating = st.slider("I feel comfortable being honest with my therapist (1-5)", 1, 5, 4, key="honest_rating")
        post_session = st.multiselect("After sessions, I usually feel:", ["Calm", "Relieved", "Overwhelmed", "Confused", "Hopeful", "Worse"], default=["Calm"], key="post_session")
        stress_signs = st.text_area("Signs I'm stressed/overwhelmed in session (optional)", key="stress_signs")
        stress_help = st.text_area("What helps me most when stressed (optional)", key="stress_help")
        submitted = st.form_submit_button("Save answers")
        if submitted:
            st.session_state.update({
                "safe_rating": safe_rating,
                "honest_rating": honest_rating,
                "post_session": post_session,
                "stress_signs": stress_signs,
                "stress_help": stress_help
            })

# --- Section 5: Therapy Harm & Boundaries ---------------------------------
if focus in ["Concerns, Discomfort, or Harm", "Both"]:
    st.header("5 — Therapy Harm & Boundaries")
    with st.form(key='harm_form'):
        harmful_events = st.text_area("Any harmful or boundary-violating experiences? (optional)", key="harmful_events")
        safety_needs = st.text_area("Anything that would make therapy feel safer? (optional)", key="safety_needs")
        submitted = st.form_submit_button("Save answers")
        if submitted:
            st.session_state.update({
                "harmful_events": harmful_events,
                "safety_needs": safety_needs
            })

# --- Generate summary & download ------------------------------------------
st.markdown("---")
st.header("Create summary & download")

# Build responses dict from session_state
responses = {
    "Entry": {"Focus chosen": focus, "Style chosen": style},
    "Overall Experience": {
        "Overall rating (1-5)": st.session_state.get("overall_rating"),
        "What to continue": st.session_state.get("overall_text"),
        "Stressful / less effective": st.session_state.get("overall_issues")
    },
    "Topics & Comfort": {
        "Easy topics": st.session_state.get("easy_topics"),
        "Hard topics": st.session_state.get("hard_topics"),
        "Hesitant topics": st.session_state.get("hesitant_topics"),
        "Training suggestions": st.session_state.get("training_suggestions")
    },
    "Structure & Style": {
        "Punctuality": st.session_state.get("punctuality"),
        "Self-disclosure rating": st.session_state.get("self_disclosure"),
        "Self-disclosure comments": st.session_state.get("self_disclosure_text"),
        "Session structure": st.session_state.get("session_structure"),
        "Session structure comments": st.session_state.get("session_structure_text"),
        "Communication style comments": st.session_state.get("communication_style"),
        "Autonomy vs masking": st.session_state.get("autonomy_masking")
    },
    "Relational Climate": {
        "Safe rating": st.session_state.get("safe_rating"),
        "Honest rating": st.session_state.get("honest_rating"),
        "Post-session feelings": st.session_state.get("post_session"),
        "Stress signs": st.session_state.get("stress_signs"),
        "Stress helps": st.session_state.get("stress_help")
    },
    "Therapy Harm & Boundaries": {
        "Harmful events": st.session_state.get("harmful_events"),
        "Safety needs": st.session_state.get("safety_needs")
    }
}

include_sections = st.multiselect(
    "Which sections should be included in the Word summary?",
    list(responses.keys()),
    default=[k for k in responses.keys() if k != "Entry"],
    key="include_sections"
)

filtered = {sec: responses.get(sec, {}) for sec in include_sections}

if st.button("Generate Word summary", key="generate_summary"):
    docx_bytes = make_docx(filtered, title="Client Feedback Summary")
    st.session_state['docx_bytes'] = docx_bytes
    st.success("Summary generated — you can download the Word file below.")

if 'docx_bytes' in st.session_state:
    st.download_button(
        "Download .docx",
        data=st.session_state['docx_bytes'],
        file_name="client_feedback_summary.docx",
        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        key="download_docx"
    )

st.markdown("---")
st.caption("This app now saves responses in session state, ensuring Word downloads contain the answers and therapy harm sections appear correctly.")

