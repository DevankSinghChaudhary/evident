from __future__ import annotations

from evident.auth import METHODS, AuthCodex, CustomAPI, auth_method

METHOD = auth_method()


class AuthEvident:
    def __init__(self):
        self.siwc = METHODS[0]

    def authenticate(self):
        if METHOD == self.siwc:
            codex = AuthCodex()
            codex.authenticate()
        else:
            custom_api = CustomAPI()
            config = custom_api.configure()
            return config


evident = AuthEvident()
config = evident.authenticate()
if isinstance(config, dict):
    print(config)
