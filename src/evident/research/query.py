from __future__ import annotations

import time
from typing import Literal

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from openai_codex import Codex, CodexConfig
from pydantic import BaseModel, ConfigDict, Field

from evident.auth import AuthCodex
from evident.prompts import QUERY_EXPANSION_BASE, QUERY_EXPANSION_DEV
from evident.utilities import web_search


class QueryExpansionSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    queries: list[str] = Field(description="Expanded search queries.")


schema = QueryExpansionSchema.model_json_schema()
codex = AuthCodex()
models = codex.models()
DEFAULT_MODEL = list(models.values())[
    0
]  # Default model: GPT 6 Luna for free subscription


class Research:
    def __init__(
        self,
        provider: Literal[
            "codex",
            "openai-compatible",
        ],
        model: str = DEFAULT_MODEL,
        base_url: str | None = None,
        api_key: str | None = None,
        web_search: bool = False,
    ):
        self.provider = provider.lower().strip()
        self.web_search = web_search
        self.model = model
        self.base_url = base_url
        self.api_key = api_key

        if self.provider == "codex":
            overrides = (
                ('web_search="live"',) if web_search else ('web_search="disabled"',)
            )

            self.codex = Codex(config=CodexConfig(config_overrides=overrides))

    def query(self, query: str):
        if self.provider == "codex":
            with self.codex as codex:
                thread = codex.thread_start(
                    developer_instructions=QUERY_EXPANSION_DEV,
                    base_instructions=QUERY_EXPANSION_BASE,
                )
                start = time.perf_counter()
                print(f"Model: {self.model}")
                result = thread.run(query, model=self.model, output_schema=schema)
                expanded = QueryExpansionSchema.model_validate_json(
                    result.final_response
                )
                end = time.perf_counter()
                elapsed = end - start
                print(f"Codex time: {elapsed:.2f}s")
                return expanded

        if self.provider == "openai":
            model = ChatOpenAI(
                model=self.model,
                base_url=self.base_url,
                api_key=self.api_key,
            )
            if self.web_search:
                agent = create_agent(
                    model=model,
                    system_prompt=f"{QUERY_EXPANSION_DEV} \n \n {QUERY_EXPANSION_BASE}",
                    response_format=QueryExpansionSchema,
                    tools=[web_search],
                )
            agent = create_agent(
                model=model,
                system_prompt=f"{QUERY_EXPANSION_DEV} \n \n {QUERY_EXPANSION_BASE}",
                response_format=QueryExpansionSchema,
            )

            result = agent.invoke({"messages": [{"role": "user", "content": query}]})
            return result["structured_response"]
