"""
Authentication pipeline.
"""

from __future__ import annotations

import webbrowser

from openai_codex import Codex
from yaspin import yaspin

spinner = yaspin()


class AuthCodex:
    def authenticate(self):
        with Codex() as codex:
            spinner.start()
            if codex.account().account is not None:
                print("Already authenticated. Start your research session")
            else:
                login = codex.login_chatgpt()
                webbrowser.open(login.auth_url)
                print(login.wait().success)
            spinner.stop()

    def logout(self):
        with Codex() as codex:
            spinner.start()
            if codex.account().account is not None:
                codex.logout()
            spinner.stop()

    def models(self):
        with Codex() as codex:
            response = codex.models()
            models = response.data
            return {
                model.display_name: model.id for model in models if not model.hidden
            }
