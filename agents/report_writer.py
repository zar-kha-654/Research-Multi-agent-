from crewai import Agent, Crew, Task

from llm import get_llm


def run_report_writer(
    topic: str,
    research: str,
    verification: str,
    analysis: str,
):
    llm = get_llm()

    writer = Agent(
        role="Research Report Writer",
        goal=(
            "Create a polished, readable and evidence-based research report "
            "using the research, verification and analysis provided."
        ),
        backstory=(
            "You are an experienced research writer. You write clearly, "
            "preserve source attribution, avoid unsupported claims, and "
            "make complex research easy to understand."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=f"""
Write the final research report.

Topic:
{topic}

Research:
{research}

Verification:
{verification}

Analysis:
{analysis}

Create a professional Markdown report.

Use this structure:

# {topic}

## Executive Summary

Briefly explain the most important findings.

## Key Findings

Present the major evidence-based findings.

## Detailed Analysis

Explain the important patterns, comparisons,
and relationships.

## Conflicting or Uncertain Information

Clearly identify disagreements, uncertainty,
and limitations.

## Research Gaps

Explain what remains unclear or requires
additional investigation.

## Sources

List the important source titles and URLs
provided by the research.

Important rules:

- Do not invent citations.
- Do not invent URLs.
- Do not claim a source says something unless the
  provided research supports it.
- Clearly distinguish evidence from interpretation.
- Keep the report readable.
- Use Markdown headings and bullet points.
""",
        expected_output="""
A polished Markdown research report with an executive summary,
key findings, analysis, uncertainty/limitations, research gaps,
and a source list containing the URLs available in the research.
""",
        agent=writer,
    )

    crew = Crew(
        agents=[writer],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)
