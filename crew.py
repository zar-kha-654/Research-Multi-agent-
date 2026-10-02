from agents.researcher import run_researcher
from agents.verifier import run_verifier
from agents.analyst import run_analyst
from agents.report_writer import run_report_writer


def run_research(topic: str, on_agent_start=None):
    """
    Run the research team sequentially.

    on_agent_start:
        Optional callback used by Streamlit to display
        which agent is currently working.
    """

    if on_agent_start:
        on_agent_start("Researcher")

    research = run_researcher(topic)

    if on_agent_start:
        on_agent_start("Verifier")

    verification = run_verifier(
        topic=topic,
        research=research,
    )

    if on_agent_start:
        on_agent_start("Analyst")

    analysis = run_analyst(
        topic=topic,
        research=research,
        verification=verification,
    )

    if on_agent_start:
        on_agent_start("Report Writer")

    final_report = run_report_writer(
        topic=topic,
        research=research,
        verification=verification,
        analysis=analysis,
    )

    return {
        "research": research,
        "verification": verification,
        "analysis": analysis,
        "report": final_report,
    }
