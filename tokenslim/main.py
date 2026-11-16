
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="TokenSlim | AI Coding Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DESIGN SYSTEM ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #0B1020;
    --panel: #121A2B;
    --border: #26334A;
    --purple: #8B7CFF;
    --cyan: #4DD9E8;
    --muted: #94A3B8;
}

.stApp {
    background: var(--bg);
    color: #F1F5F9;
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #0E1525;
    border-right: 1px solid #26334A;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

.hero {
    background: linear-gradient(120deg, #191D3B, #172A40 65%, #122B38);
    border: 1px solid #354363;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 24px;
}

.hero-label {
    color: #A99DFF;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero-title {
    font-family: 'Space Grotesk';
    font-size: 37px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 12px 0 8px;
}

.hero-subtitle {
    color: #B6C2D5;
    font-size: 15px;
}

.metric-card {
    background: #121A2B;
    border: 1px solid #26334A;
    border-radius: 15px;
    padding: 19px;
    min-height: 115px;
}

.metric-label {
    color: #94A3B8;
    font-size: 13px;
}

.metric-value {
    font-family: 'Space Grotesk';
    font-size: 27px;
    font-weight: 700;
    color: #F8FAFC;
    margin-top: 9px;
}

.metric-note {
    color: #4DD9A8;
    font-size: 12px;
    margin-top: 4px;
}

.section-heading {
    font-family: 'Space Grotesk';
    font-size: 19px;
    font-weight: 600;
    margin: 22px 0 12px;
    color: #F8FAFC;
}

.info-card {
    background: #121A2B;
    border: 1px solid #26334A;
    border-radius: 15px;
    padding: 20px;
}

.status {
    display: inline-block;
    background: #183B35;
    color: #62E6B1;
    padding: 5px 11px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
}

.stButton > button {
    background: linear-gradient(100deg, #7667F5, #4F83E8);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 44px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border: 1px solid #A99DFF;
    color: white;
    transform: translateY(-1px);
}

.stTextArea textarea {
    background: #101829 !important;
    color: #E2E8F0 !important;
    border: 1px solid #354363 !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #121A2B;
    border-color: #354363;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 0 22px">
        <div style="font-size:27px;font-weight:800;
                    font-family:'Space Grotesk';">
            ⚡ TOKEN<span style="color:#9484FF">SLIM</span>
        </div>
        <div style="font-size:10px;letter-spacing:2px;
                    color:#94A3B8;">
            AUTONOMOUS CODING AGENT
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "WORKSPACE",
        ["Overview", "Coding Agent", "Token Analytics", "Settings"],
        label_visibility="visible"
    )

    st.markdown("---")

    st.markdown("**SYSTEM STATUS**")
    st.markdown(
        '<span class="status">● DEMO MODE</span>',
        unsafe_allow_html=True
    )

    st.caption("Bifrost connection: Not configured")
    st.caption("Agent engine: In development")

    st.markdown("---")
    st.caption("TokenSlim v0.1.0")
    st.caption("Built for the Global AI Hackathon")


# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
    <div class="hero-label">INTELLIGENT DEVELOPMENT WORKSPACE</div>
    <div class="hero-title">Code smarter. Spend less.</div>
    <div class="hero-subtitle">
        An autonomous coding agent engineered to solve software
        tasks with minimal context and optimized token consumption.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- METRICS ----------------

col1, col2, col3, col4 = st.columns(4)

metrics = [
    (col1, "TOTAL TASKS", "—", "Awaiting first task"),
    (col2, "TOKENS USED", "—", "No live usage yet"),
    (col3, "TOKENS SAVED", "—", "Benchmark pending"),
    (col4, "SUCCESS RATE", "—", "Awaiting test results")
]

for col, label, value, note in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)


# ---------------- MAIN WORKSPACE ----------------

if page == "Overview":

    st.markdown(
        '<div class="section-heading">Your workspace</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.65, 1])

    with left:

        st.markdown('<div class="info-card">', unsafe_allow_html=True)

        st.markdown("### ⚡ Start a coding task")

        st.caption(
            "Describe what you want your AI coding agent to accomplish."
        )

        task = st.text_area(
            "Coding instructions",
            placeholder=(
                "Example: Analyze my Python authentication module, "
                "identify bugs, generate a minimal patch and run tests."
            ),
            height=150,
            label_visibility="collapsed"
        )

        language = st.selectbox(
            "Programming language",
            ["Python", "JavaScript", "TypeScript", "Java", "C++"]
        )

        if st.button("Initialize coding task →", use_container_width=True):

            if task.strip():

                st.session_state["task"] = task
                st.session_state["language"] = language
                st.session_state["submitted"] = True

                st.success(
                    "Task captured! Agent execution will be enabled "
                    "after backend integration."
                )

            else:
                st.warning("Please enter a coding task first.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:

        st.markdown('<div class="info-card">', unsafe_allow_html=True)

        st.markdown("### ◈ Agent configuration")

        st.write("**Execution mode**")
        st.info("Demo mode — backend not connected")

        st.write("**AI gateway**")
        st.write("Bifrost · Not configured")

        st.write("**Context strategy**")
        st.write("Smart context selection · Planned")

        st.write("**Verification**")
        st.write("Automated testing · Planned")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("submitted", False):

        st.markdown("### Latest task")

        st.code(st.session_state["task"])

        st.caption(
            "This is a saved demo task, not an executed coding result."
        )


elif page == "Coding Agent":

    st.markdown("## Coding Agent")
    st.write("Your autonomous software development workspace.")

    st.text_area(
        "Describe your coding task",
        height=180,
        placeholder="What should the agent build or fix?"
    )

    st.info(
        "Agent execution is not connected yet. "
        "The next development stage will add the coding engine."
    )


elif page == "Token Analytics":

    st.markdown("## Token Analytics")

    st.info(
        "Real token analytics will appear here after model integration. "
        "No benchmark results have been recorded yet."
    )

    st.markdown("### Planned performance metrics")

    st.write("- Input tokens")
    st.write("- Output tokens")
    st.write("- Tokens saved against baseline")
    st.write("- Task completion rate")
    st.write("- Execution time")


elif page == "Settings":

    st.markdown("## Settings")

    st.write("**Application:** TokenSlim")
    st.write("**Version:** 0.1.0")
    st.write("**Gateway:** Bifrost (pending configuration)")
    st.write("**Environment:** Local development")

    st.warning(
        "Never paste API keys directly into your source code. "
        "We will use environment variables."
    )


# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#64748B;font-size:12px;">
        TOKENSLIM · INTELLIGENCE WITH EFFICIENCY · 2026
    </div>
    """,
    unsafe_allow_html=True
)
