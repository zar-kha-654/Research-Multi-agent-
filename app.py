import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg
import os

import streamlit as st

from crew import run_research


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="ResearchCrew",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# LOAD SECRETS
# ---------------------------------------------------------

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if "SERPER_API_KEY" in st.secrets:
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
<style>

    /* Main page */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(99, 102, 241, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(14, 165, 233, 0.10),
                transparent 30%
            ),
            #080b12;
        color: #f8fafc;
    }

    /* Hide default Streamlit decoration */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 24, 0.96);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Hero */
    .hero {
        padding: 2.2rem 0 1.5rem 0;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(99,102,241,0.14);
        border: 1px solid rgba(129,140,248,0.25);
        color: #a5b4fc;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    .hero h1 {
        font-size: clamp(2.5rem, 6vw, 4.5rem);
        line-height: 0.98;
        margin: 1rem 0 0.8rem 0;
        letter-spacing: -0.055em;
        color: #f8fafc;
    }

    .hero p {
        max-width: 760px;
        font-size: 1.08rem;
        line-height: 1.7;
        color: #94a3b8;
    }

    /* Agent cards */
    .agent-card {
        padding: 1rem 1.1rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.025);
        margin-bottom: 0.7rem;
    }

    .agent-name {
        font-weight: 700;
        color: #f8fafc;
    }

    .agent-description {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }

    /* Report */
    .report-box {
        padding: 1.4rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.025);
    }

    /* Metric */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        padding: 1rem;
        border-radius: 16px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        min-height: 3rem;
        font-weight: 700;
        border: 1px solid rgba(129,140,248,0.35);
        background: linear-gradient(
            135deg,
            rgba(99,102,241,0.95),
            rgba(79,70,229,0.95)
        );
        color: white;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(165,180,252,0.8);
    }

    /* Text area */
    textarea {
        border-radius: 14px !important;
    }

</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 🔎 ResearchCrew")

    st.caption("Multi-agent research assistant")

    st.divider()

    st.markdown("### Your research team")

    agents = [
        ("🔎", "Researcher", "Finds sources and evidence"),
        ("🧪", "Verifier", "Checks claims and contradictions"),
        ("🧠", "Analyst", "Extracts patterns and insights"),
        ("✍️", "Report Writer", "Creates the final report"),
    ]

    for icon, name, description in agents:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-name">{icon} {name}</div>
                <div class="agent-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown("### Stack")

    st.caption("CrewAI · Groq · GPT-OSS 120B · Serper · Streamlit")

    st.divider()

    st.caption(
        "Research results should be independently checked before "
        "being used for important decisions."
    )


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
<div class="hero">

<span class="hero-badge">AI RESEARCH WORKSPACE</span>

<h1>Research deeper.<br>Understand faster.</h1>

<p>
Give ResearchCrew a question. Four specialized AI agents will
search for evidence, verify important claims, analyze the findings,
and turn everything into a structured research report.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------

st.markdown("### What do you want to research?")

topic = st.text_area(
    "Research topic",
    placeholder=(
        "Example: What are the latest developments in AI coding "
        "agents and how are they changing software development?"
    ),
    height=130,
    label_visibility="collapsed",
)


# ---------------------------------------------------------
# EXAMPLES
# ---------------------------------------------------------

st.markdown("**Try a research question**")

examples = [
    "Latest developments in AI coding agents",
    "How multi-agent systems are being used in healthcare",
    "Recent advances in open-source reasoning models",
]

cols = st.columns(3)

for i, example in enumerate(examples):
    with cols[i]:
        if st.button(example, key=f"example_{i}"):
            st.session_state["topic"] = example
            st.rerun()


if "topic" in st.session_state and not topic:
    topic = st.session_state["topic"]


st.write("")


# ---------------------------------------------------------
# START BUTTON
# ---------------------------------------------------------

start = st.button(
    "🚀 Start Research",
    type="primary",
)


# ---------------------------------------------------------
# RESEARCH EXECUTION
# ---------------------------------------------------------

if start:

    if not topic.strip():
        st.warning("Enter a research topic first.")
        st.stop()

    # Check API keys
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is missing.")
        st.stop()

    if not os.getenv("SERPER_API_KEY"):
        st.error("SERPER_API_KEY is missing.")
        st.stop()

    st.divider()

    st.markdown("## ⚡ Research in progress")

    progress = st.progress(0)

    status_box = st.empty()

    agent_status = {
        "Researcher": "waiting",
        "Verifier": "waiting",
        "Analyst": "waiting",
        "Report Writer": "waiting",
    }

    agent_order = [
        "Researcher",
        "Verifier",
        "Analyst",
        "Report Writer",
    ]

    def render_agents(active_agent):

        html = """
        <div style="
            display:grid;
            grid-template-columns:repeat(4, 1fr);
            gap:10px;
            margin:1rem 0 1.5rem 0;
        ">
        """

        icons = {
            "Researcher": "🔎",
            "Verifier": "🧪",
            "Analyst": "🧠",
            "Report Writer": "✍️",
        }

        for name in agent_order:

            if name == active_agent:
                state = "● Working"
                opacity = "1"
                border = "rgba(129,140,248,0.65)"
            elif agent_status[name] == "complete":
                state = "✓ Complete"
                opacity = "0.9"
                border = "rgba(34,197,94,0.35)"
            else:
                state = "○ Waiting"
                opacity = "0.55"
                border = "rgba(255,255,255,0.08)"

            html += f"""
            <div style="
                padding:1rem;
                border-radius:14px;
                border:1px solid {border};
                background:rgba(255,255,255,0.025);
                opacity:{opacity};
            ">
                <div style="font-size:1.3rem;">
                    {icons[name]}
                </div>
                <div style="
                    margin-top:0.35rem;
                    font-weight:700;
                    color:#f8fafc;
                ">
                    {name}
                </div>
                <div style="
                    margin-top:0.2rem;
                    color:#94a3b8;
                    font-size:0.78rem;
                ">
                    {state}
                </div>
            </div>
            """

        html += "</div>"

        status_box.markdown(
            html,
            unsafe_allow_html=True,
        )

    def agent_started(name):

        # Mark previous agents complete
        for previous in agent_order:
            if previous == name:
                break

            agent_status[previous] = "complete"

        render_agents(name)

        current_index = agent_order.index(name)

        progress.progress(
            current_index / len(agent_order)
        )

    try:

        agent_started("Researcher")

        result = run_research(
            topic.strip(),
            on_agent_start=agent_started,
        )

        for name in agent_order:
            agent_status[name] = "complete"

        render_agents(None)

        progress.progress(1.0)

        st.success("Research completed successfully.")

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------

        st.markdown("## Research complete")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Agents", "4")

        with col2:
            st.metric("Workflow", "Sequential")

        with col3:
            st.metric("Web Research", "Enabled")

        with col4:
            st.metric("Model", "GPT-OSS 120B")

        # -------------------------------------------------
        # FINAL REPORT
        # -------------------------------------------------

        st.markdown("## 📄 Final Research Report")

        st.markdown(
            '<div class="report-box">',
            unsafe_allow_html=True,
        )

        st.markdown(result["report"])

        st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------------------------------
        # AGENT OUTPUTS
        # -------------------------------------------------

        st.markdown("## 🧩 Research Trail")

        with st.expander("🔎 Researcher output"):
            st.markdown(result["research"])

        with st.expander("🧪 Verifier output"):
            st.markdown(result["verification"])

        with st.expander("🧠 Analyst output"):
            st.markdown(result["analysis"])

        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        st.download_button(
            label="⬇️ Download Research Report",
            data=result["report"],
            file_name="research_report.md",
            mime="text/markdown",
        )

    except Exception as e:

        st.error(
            "Something went wrong while running the research team."
        )

        with st.expander("Technical error"):
            st.exception(e)
