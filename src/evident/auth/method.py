"""
METHOD FOR AUTHENTICATION FOR LLM
"""

from __future__ import annotations

import questionary

METHODS = [
    "Sign-in With ChatGPT",
    "Custom API",
    "Ollama (Local)",
]


def method():
    auth_method = questionary.select(
        "Select an authentication method:",
        choices=METHODS,
    ).ask()
    return auth_method
