from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Literal, TypeAlias

import ollama
import questionary

from evident.research.browser.ollama_models import decision_models

DecisionMethod: TypeAlias = Literal["choice", "noul", "score"]

DEFAULT_MODEL = "tev1:4b"
QUESTION_ID = "category"


class DecisionError(Exception):
    """Base exception for the decision controller."""


class OllamaUnavailableError(DecisionError):
    """Raised when the local Ollama server cannot be reached."""


class ModelNotInstalledError(DecisionError):
    """Raised when the requested decision model is not installed."""


class ModelInstallationError(DecisionError):
    """Raised when a model download fails."""


class SetupCancelledError(DecisionError):
    """Raised when the user cancels interactive setup."""


class InvalidDecisionRequestError(DecisionError):
    """Raised when a decision request has invalid arguments."""


class DecisionModelManager:
    """Manages local decision models and their installation."""

    def __init__(
        self,
        client: ollama.Client | None = None,
        catalog_provider: Callable[[], list[str]] = decision_models,
    ) -> None:
        self.client = client or ollama.Client()
        self.catalog_provider = catalog_provider

    def installed_models(self) -> set[str]:
        """Return names of all locally installed models."""

        try:
            response = self.client.list()
        except (ollama.RequestError, ollama.ResponseError) as exc:
            raise OllamaUnavailableError(
                f"Could not communicate with Ollama: {exc}"
            ) from exc

        return {model.model for model in response.models}

    def installed_decision_models(self) -> set[str]:
        """Return installed models that belong to the decision catalog."""

        installed = self.installed_models()
        catalog = set(self.catalog_provider())

        return installed.intersection(catalog)

    def is_installed(self, model: str) -> bool:
        """Check whether an exact model name is installed."""

        return model in self.installed_models()

    def available_decision_models(self) -> list[str]:
        """Retrieve decision models from the public catalog."""

        try:
            models = self.catalog_provider()
        except Exception as exc:
            raise DecisionError(
                f"Could not retrieve the decision model catalog: {exc}"
            ) from exc

        return list(dict.fromkeys(models))

    def install(
        self,
        model: str,
        progress_callback: Callable[[str], None] | None = None,
    ) -> None:
        """Download a model and optionally report installation progress."""

        try:
            for progress in self.client.pull(model, stream=True):
                status = progress.status

                if progress.total and progress.completed is not None:
                    percentage = progress.completed / progress.total * 100
                    message = f"{status}: {percentage:.1f}%"
                else:
                    message = status

                if progress_callback:
                    progress_callback(message)

        except (ollama.RequestError, ollama.ResponseError) as exc:
            raise ModelInstallationError(f"Failed to install {model}: {exc}") from exc

        if not self.is_installed(model):
            raise ModelInstallationError(
                f"Ollama finished pulling {model}, "
                "but the model could not be found locally."
            )

    def select_model(
        self,
        requested_model: str,
        interactive: bool = False,
    ) -> str:
        """
        Ensure a decision model is installed.

        Returns the selected model name.
        """

        if self.is_installed(requested_model):
            return requested_model

        if not interactive:
            raise ModelNotInstalledError(
                f"{requested_model!r} is not installed. "
                f"Install it using: ollama pull {requested_model}"
            )

        catalog = self.available_decision_models()

        choices: dict[str, str] = {}

        if requested_model in catalog:
            choices[f"Install requested model ({requested_model})"] = requested_model

        if DEFAULT_MODEL in catalog and DEFAULT_MODEL not in choices.values():
            choices[f"Install recommended model ({DEFAULT_MODEL})"] = DEFAULT_MODEL

        for model in catalog:
            if model not in choices.values():
                choices[model] = model

        if not choices:
            raise DecisionError("No decision models were found in the public catalog.")

        selected = questionary.select(
            f"{requested_model} is not installed.\nChoose a decision model to install:",
            choices=[*choices, "Cancel"],
        ).ask()

        if selected is None or selected == "Cancel":
            raise SetupCancelledError("Model selection was cancelled.")

        model = choices[selected]

        print(f"Installing {model}...")

        self.install(
            model,
            progress_callback=lambda message: print(message),
        )

        return model


class Decision:
    """Evident's Ollama System One decision controller."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        *,
        client: ollama.Client | None = None,
        manager: DecisionModelManager | None = None,
    ) -> None:
        self.client = client or ollama.Client()
        self.manager = manager or DecisionModelManager(self.client)
        self.model = model

    def setup(self, *, interactive: bool = False) -> str:
        """
        Check the requested model and optionally install it.

        Returns the final selected model name.
        """

        self.model = self.manager.select_model(
            requested_model=self.model,
            interactive=interactive,
        )

        return self.model

    @staticmethod
    def _validate_request(
        output_method: str,
        instruction: str,
        criteria: Mapping[str, object],
    ) -> None:
        """Validate System One question arguments."""

        if output_method not in {"choice", "noul", "score"}:
            raise InvalidDecisionRequestError(
                f"Unsupported decision method: {output_method!r}"
            )

        if not instruction.strip():
            raise InvalidDecisionRequestError("Instruction cannot be empty.")

        if not isinstance(criteria, Mapping):
            raise InvalidDecisionRequestError("Criteria must be a mapping.")

        count = len(criteria)

        if output_method == "choice" and not 2 <= count <= 26:
            raise InvalidDecisionRequestError(
                "Choice requires between 2 and 26 criteria."
            )

        if output_method == "score" and not 2 <= count <= 10:
            raise InvalidDecisionRequestError(
                "Score requires between 2 and 10 criteria."
            )

        if output_method == "noul" and count != 2:
            raise InvalidDecisionRequestError(
                "Noul requires exactly two criteria: false and true."
            )

    def call(
        self,
        output_method: DecisionMethod,
        state: str,
        instruction: str,
        criteria: Mapping[str, object],
    ) -> object:
        """Evaluate a decision using Ollama System One."""

        if not state.strip():
            raise InvalidDecisionRequestError("State cannot be empty.")

        self._validate_request(
            output_method,
            instruction,
            criteria,
        )

        if not self.manager.is_installed(self.model):
            raise ModelNotInstalledError(
                f"Decision model {self.model!r} is not installed. "
                "Call setup(interactive=True) or install it manually."
            )

        try:
            response = self.client.systemone(
                model=self.model,
                state=state,
                questions={
                    QUESTION_ID: {
                        "type": output_method,
                        "instructions": instruction,
                        "criteria": dict(criteria),
                    }
                },
            )

        except (ollama.RequestError, ollama.ResponseError) as exc:
            raise DecisionError(f"System One request failed: {exc}") from exc

        return response.answers[QUESTION_ID]
