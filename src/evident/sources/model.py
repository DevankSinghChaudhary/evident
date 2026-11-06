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


if "NVIDIA_API_KEY" not in os.environ:
    raise ValueError(
        "Configuration Error: NVIDIA_API_KEY is missing from environment variables.\n"
        "Set it before before running the application.\n"
        "Usage: Query Expansion for research"
    )


class QueryExpansion:
    def __init__(self, model="nvidia/nemotron-3-ultra-550b-a55b"):
        self.model = model

    def expand(self, query: str):
        model = ChatOpenAI(
            model=self.model,
            api_key=os.environ["NVIDIA_API_KEY"],
            base_url=os.environ.get(
                "NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"
            ),
        )
        agent = create_agent(
            model=model,
            system_prompt=QUERYEXPANSION_SP,
            response_format=QueryResult,
            tools=[web_search],
        )
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})
        result = result["structured_response"]
        return result
