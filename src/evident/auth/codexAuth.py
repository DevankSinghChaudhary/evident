"""
Authentication pipeline.
"""

from __future__ import annotations

import webbrowser

from openai_codex import Codex


class AuthCodex:
    def authenticate(self):
        with Codex() as codex:
            if codex.account().account is not None:
                print("Already authenticated. Start your research session")
            else:
                login = codex.login_chatgpt()
                webbrowser.open(login.auth_url)
                print(login.wait().success)

    def logout(self):
        with Codex() as codex:
            if codex.account().account is not None:
                codex.logout()

    def models(self):
        with Codex() as codex:
            response = codex.models()
            models = response.data
            return {
                model.display_name: model.id for model in models if not model.hidden
            }
