from __future__ import annotations

import time

from openai_codex import Codex, CodexConfig
from pydantic import BaseModel, ConfigDict, Field

from evident.auth import AuthCodex
from evident.prompts import QUERY_EXPANSION_BASE, QUERY_EXPANSION_DEV


class QueryExpansionSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    queries: list[str] = Field(description="Expanded search queries.")


schema = QueryExpansionSchema.model_json_schema()


class Research:
    def __init__(self, provider: str, web_search: bool = False):
        self.provider = provider.lower().strip()
        self.web_search = web_search

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
                codex = AuthCodex()
                models = codex.models()
                for model in models.values():
                    start = time.time()
                    print(f"Model: {model}")
                    result = thread.run(query, model=model, output_schema=schema)
                    expanded = QueryExpansionSchema.model_validate_json(
                        result.final_response
                    )
                    print(expanded)
                    print(f"Timed: {time.time() - start:.2f}s")


research = Research(provider="codex")
result = research.query("How gravity lensing work?")
