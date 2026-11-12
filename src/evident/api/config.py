from __future__ import annotations

from typing import Literal

from evident.auth import AuthCodex
from evident.research import Research

METHODS = Literal["codex", "openai-compatible"]


class Evident:
    def __init__(
        self,
        provider: METHODS,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ):
        self.provider = provider.lower()
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        if self.provider == "codex":
            codex = AuthCodex()
            codex.authenticate()
        if self.provider not in METHODS:
            raise ValueError(f"Currently evident only supports: {METHODS} methods")

    def research(self, topic):
        evident = Research(provider=self.provider, web_search=True)
        query = evident.query(query=topic)
        print(query)


app = Evident(provider="google")
app.research("Fermi Paradox")
