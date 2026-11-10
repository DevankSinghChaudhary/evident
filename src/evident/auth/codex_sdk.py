from __future__ import annotations

import time

from openai_codex import Codex


def auth_codex():
    start = time.time()
    with Codex() as codex:
        thread = codex.thread_start()
        data = codex.models()

        print(thread.id)

        print()
        # print(result.final_response)
        print(f"{time.time() - start:.2f}")


auth_codex()
