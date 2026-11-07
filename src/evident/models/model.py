import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from evident.prompts import QUERYEXPANSION_SP
from evident.utilities import web_search

load_dotenv()


class QueryResult(BaseModel):
    base_query: str
    expanded: list[str]
    covered_perspectives: list[str]
    unexplored_perspectives: list[str]
    knowledge_gaps: list[str]
    reasoning_summary: list[str]


if "NVIDIA_API_KEY" not in os.environ:
    raise ValueError(
        "Configuration Error: NVIDIA_API_KEY is missing from environment variables.\n"
        "Set it before before running the application.\n"
        "Usage: Query Expansion for research"
    )


class QueryExpansion:
    def __init__(self, model="gemini-3.5-flash-lite"):
        self.model = model

    async def expand(self, query: str):
        model = ChatOpenAI(
            model=self.model,
            api_key=os.environ["GOOGLE_API_KEY"],
            base_url=os.environ.get(
                "GOOGLE_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/openai/",
            ),
        )
        agent = create_agent(
            model=model,
            system_prompt=QUERYEXPANSION_SP,
            response_format=QueryResult,
            tools=[web_search],
        )
        result = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})
        result = result["structured_response"]
        return {
            "queries": result.expanded,
            "cp": result.covered_perspectives,
            "up": result.unexplored_perspectives,
            "kg": result.knowledge_gaps,
            "rs": result.reasoning_summary,
        }
