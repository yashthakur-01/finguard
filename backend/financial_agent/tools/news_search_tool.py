# tools/news_search_tool.py
from pydantic import BaseModel, PrivateAttr
from typing import Type, Dict, Any
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from ..config import SERPER_API_KEY


class CompanyNewsInput(BaseModel):
    company: str


class CompanyNewsTool(BaseTool):
    name: str = "company_news_tool"
    description: str = "Fetch latest company news using Serper search"
    args_schema: Type[BaseModel] = CompanyNewsInput
    _search: SerperDevTool = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._search = SerperDevTool(api_key=SERPER_API_KEY, type="news")

    def _run(self, company: str) -> Dict[str, Any]:
        query = f"{company} latest stock news earnings updates"
        result = self._search.run(query)
        return {
            "company": company,
            "news_results": result
        }
