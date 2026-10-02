from crewai import Agent, Crew, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

from llm import get_llm


def run_researcher(topic: str):
    llm = get_llm()

    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

    researcher = Agent(
        role="Web Research Specialist",
        goal=(
            "Find current, relevant and trustworthy information about the "
            "research topic and collect useful evidence from online sources."
        ),
        backstory=(
            "You are a careful research specialist. You search for primary "
            "sources whenever possible, compare multiple sources, and never "
            "invent facts or URLs."
        ),
        tools=[search_tool, scrape_tool],
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=f"""
Research the following topic:

{topic}

Instructions:

1. Search the web for current and relevant information.
2. Prefer primary sources, official documentation, research papers,
   institutional sources and direct announcements.
3. Use multiple sources rather than relying on one webpage.
4. Read important webpages when necessary.
5. Identify the main factual findings.
6. Include the source title and exact URL for important sources.
7. Clearly separate established facts from claims or opinions.
8. Do not invent information.
9. Focus on useful evidence that another agent can verify.

Return:

- Research findings
- Important facts
- Key developments
- Important source URLs
- Any uncertainty or conflicting information
""",
        expected_output="""
A detailed research brief containing factual findings,
source titles, URLs, important evidence, and uncertainties.
""",
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)
