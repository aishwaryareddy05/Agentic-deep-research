from crewai import Agent
from crewai import LLM
from langchain_groq import ChatGroq 
from tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    verbose=True,
    timeout=120,
)

research_agent = Agent(
    role="Research Specialist",
    goal="Search for relevant, detailed, indepth  and up-to-date information from trusted sources based on the user’s query.",
    backstory=(
        "You are a skilled analyst who excels at digging deep into documentation, articles, and data sources. "
        "Your job is to fetch facts, references, and key points that help answer complex questions accurately."
    ),  
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation= True
)

answer_drafter_agent = Agent(
    role="Answer Composer",
    goal="Generate clear, insightful,very indepth and well-structured responses based on the research agent’s findings.",
    backstory=(
        "You specialize in transforming raw research into meaningful, human-readable answers. "
        "You value clarity, brevity, and completeness, always tailoring your output to the user’s needs."
    ),
    tools=[tool],  
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation= False
)