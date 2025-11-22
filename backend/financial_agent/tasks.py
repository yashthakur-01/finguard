# tasks.py
from crewai import Task
from .agents import data_agent, analyst_agent
from .schemas import StockDecision


data_collection_task = Task(
    description=(
        "Collect every important piece of financial and news data for "
        "{company_name} ({ticker}). Use all tools. Prepare a structured "
        "financial intelligence report useful for high-level investment decisions."
    ),
    agent=data_agent,
    expected_output="A structured research report with fundamentals, metrics and news."
)

analysis_task = Task(
    description=(
        "Analyze the research report for {company_name} ({ticker}). "
        "At the end, respond ONLY with JSON following the StockDecision schema."
    ),
    agent=analyst_agent,
    expected_output="JSON response of StockDecision.",
    output_json=StockDecision,
)
