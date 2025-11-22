# crew.py
from crewai import Crew, Process
from .agents import data_agent, analyst_agent
from .tasks import data_collection_task, analysis_task

def create_stock_crew():
    return Crew(
        agents=[data_agent, analyst_agent],
        tasks=[data_collection_task, analysis_task],
        process=Process.sequential,
        verbose=True
    )
