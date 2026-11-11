from __future__ import annotations

from evident.auth import AuthCodex


class Evident:
    def __init__(
        self,
        provider: str = "codex",
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

    def research(self, topic):

