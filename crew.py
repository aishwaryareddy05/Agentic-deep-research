from agents import research_agent, answer_drafter_agent
from tasks import research_task, draft_task
from crewai import Crew,Process

crew = Crew(
    agents=[research_agent, answer_drafter_agent],
    tasks=[research_task, draft_task],
    process=Process.sequential,
    verbose=True
)