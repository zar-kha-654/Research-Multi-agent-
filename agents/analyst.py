from crewai import Agent, Crew, Task

from llm import get_llm


def run_analyst(topic: str, research: str, verification: str):
    llm = get_llm()

    analyst = Agent(
        role="Research Analyst",
        goal=(
            "Turn verified research into clear findings, comparisons, "
            "patterns, disagreements and research gaps."
        ),
        backstory=(
            "You are an analytical researcher who works from evidence. "
            "You avoid unsupported conclusions and clearly distinguish "
            "evidence from interpretation."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=f"""
Research topic:

{topic}

Original research:

{research}

Verification:

{verification}

Analyze the material.

Identify:

1. The most important findings.
2. Major patterns or trends.
3. Important comparisons.
4. Agreements between sources.
5. Disagreements between sources.
6. Important limitations.
7. Research gaps or unanswered questions.

Do not introduce facts that are not present in the provided material.

Keep the analysis evidence-based.
""",
        expected_output="""
A concise analytical brief containing the main findings,
patterns, comparisons, disagreements, limitations and gaps.
""",
        agent=analyst,
    )

    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)
