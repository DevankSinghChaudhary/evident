from dataclasses import dataclass

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Button, Frame, Label, TextArea


@dataclass
class ProviderConfig:
    provider: str
    base_url: str
    api_key: str


def build_field(
    label: str, hint: str, *, password: bool = False
) -> tuple[HSplit, TextArea]:
    """Create one labelled, bordered input field and its muted hint."""
    area = TextArea(
        height=1,
        multiline=False,
        password=password,
        focusable=True,
        scrollbar=False,
        wrap_lines=False,
    )

    field = HSplit(
        [
            Label(text=label, style="class:field-label"),
            Frame(body=area, style="class:input-frame"),
            Label(text=hint, style="class:hint"),
        ],
        padding=0,
    )
    return field, area


def collect_provider_config() -> ProviderConfig | None:
    provider_field, provider_input = build_field(
        "Provider",
        "e.g. OpenAI, OpenRouter, or a local provider",
    )
    url_field, url_input = build_field(
        "Base URL",
        "e.g. https://api.example.com/v1",
    )
    key_field, key_input = build_field(
        "API key",
        "The key is hidden while you type",
        password=True,
    )

    result: ProviderConfig | None = None

    def submit() -> None:
        nonlocal result
        result = ProviderConfig(
            provider=provider_input.text.strip(),
            base_url=url_input.text.strip(),
            api_key=key_input.text,
        )
        app.exit(result=result)

    continue_button = Button("Continue", handler=submit)

    root = HSplit(
        [
            Label(text="PROVIDER CONFIGURATION", style="class:title"),
            Label(text="Enter the connection details below.", style="class:muted"),
            Window(height=1, char=" "),
            provider_field,
            Window(height=1, char=" "),
            url_field,
            Window(height=1, char=" "),
            key_field,
            Window(height=1, char=" "),
            continue_button,
            Label(
                text="Tab / Shift+Tab: move between fields    Enter: activate button    Ctrl+C: cancel",
                style="class:muted",
            ),
        ],
        padding=0,
    )

    bindings = KeyBindings()

    @bindings.add("tab")
    def _(event) -> None:
        focus_next(event)

    @bindings.add("s-tab")
    def _(event) -> None:
        focus_previous(event)

    @bindings.add("c-c", eager=True)
    def _(event) -> None:
        event.app.exit(result=None)

    style = Style.from_dict(
        {
            "title": "bold #98fb98",
            "muted": "#888888",
            "field-label": "bold",
            "input-frame": "#666666",
            "frame.border": "#666666",
            "text-area": "bg:#181818 #eeeeee",
            "text-area.focused": "bg:#222222 #ffffff",
            "button": "bg:#303030 #eeeeee",
            "button.focused": "bg:#98fb98 #101010 bold",
            "button-arrow": "#ff9638",
        }
    )

    app = Application(
        layout=Layout(root, focused_element=provider_input),
        key_bindings=bindings,
        style=style,
        full_screen=False,
        mouse_support=True,
    )

    try:
        return app.run()
    except EOFError, KeyboardInterrupt:
        return None


class CustomAPI:
    def configure(self):
        config = collect_provider_config()

        if config is None:
            print("\nConfiguration cancelled.")
            return

        if not config.provider or not config.base_url:
            print("\nProvider and Base URL are required.")
            return

        return {
            "provider": config.provider,
            "base_url": config.base_url,
            "api_key": config.api_key,
        }
        print("\nConfiguration received:")
        print(f"Provider: {config.provider}")
        print(f"Base URL: {config.base_url}")
        print(f"API key: {'[provided]' if config.api_key else '[not provided]'}")
