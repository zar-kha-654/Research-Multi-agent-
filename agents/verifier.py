from crewai import Agent, Crew, Task

from llm import get_llm


def run_verifier(topic: str, research: str):
    llm = get_llm()

    verifier = Agent(
        role="Research Verification Specialist",
        goal=(
            "Check the research findings for unsupported claims, "
            "contradictions, weak evidence and misleading statements."
        ),
        backstory=(
            "You are a meticulous fact-checker. You do not blindly trust "
            "research summaries. You distinguish evidence from interpretation "
            "and clearly identify uncertainty."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=f"""
Research topic:

{topic}

Researcher's findings:

{research}

Verify the research.

For each important claim:

1. Determine whether it is well supported.
2. Identify weak or unsupported claims.
3. Identify contradictions between sources.
4. Distinguish fact from opinion or interpretation.
5. Identify information that may be outdated.
6. Preserve the original source URLs when available.
7. Do not invent verification or pretend to have accessed a source
   that was not provided.

Return a verification brief containing:

- Supported findings
- Questionable findings
- Conflicting information
- Important limitations
- Source reliability notes
""",
        expected_output="""
A structured fact-checking brief clearly separating supported,
questionable, conflicting and uncertain information.
""",
        agent=verifier,
    )

    crew = Crew(
        agents=[verifier],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)
