from __future__ import annotations

from typing import Literal

import ollama
import questionary

from evident.research.browser.ollama_models import decision_models, download_model

DMETHODS = Literal["choice", "noul", "score"]
DEFAULT = "tev1:4b"


class Decision:
    def __init__(
        self,
        model: str,
    ):
        self.model = model

        self.available_models = ollama.list()
        self.available_models = None
        self.ollama_models = decision_models()
        if self.available_models is None:
            no_model = questionary.select(
                "You don't have any decision model installed on your system \n Want to download?",
                choices=["Download", "No"],
            ).ask()
            if no_model == "Download":
                _download_model = questionary.select(
                    "Choose any decision model (Preferred tev1:4b for most hardware):",
                    choices=self.ollama_models,
                ).ask()
                try:
                    download_model(_download_model)
                except ValueError as v:
                    print(f"Cannot download model: {v}")
                self.available_models = ollama.list()

            else:
                raise ValueError(
                    "You don't have any Decision Model download on your system.\n"
                    "Evident needs at least one Decision Model to function."
                )

        models = []
        for _model in self.available_models.models:
            models.append(_model.model)

        if self.model not in models:
            CHOICE = ["Yes", "No", "tev1:4b"]
            concent = questionary.select(
                f"You don't have {self.model} installed. \n"
                f"You want to install {self.model} or {DEFAULT}",
                choices=CHOICE,
            ).ask()
            print(concent)

            if concent == CHOICE[0]:
                stream = ollama.pull(self.model, stream=True)
                for progress in stream:
                    print(progress)
            elif concent == CHOICE[2]:
                stream = ollama.pull(CHOICE[2], stream=True)
                for progress in stream:
                    print(progress)
            else:
                raise ValueError(
                    f"You don't have {self.model} installed on your system\n"
                    "You need to install via Ollama\n"
                    "Either install any Decision Model manually from ollama or re-run the script"
                )

    def call(
        self, output_method: DMETHODS, state: str, instruction: str, criteria: dict
    ):
        response = ollama.systemone(
            model=self.model,
            state=state,
            questions={
                "category": {
                    "type": output_method,
                    "instruction": instruction,
                    "criteria": criteria,
                }
            },
        )
        return response.answers["category"]


systemone = Decision("ihphv")
