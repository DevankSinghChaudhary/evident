---
title: Prompts
description: About how prompts are stored in evident.
---

# How it's saved?

Prompts in evident is saved in separate directory named `prompts`:

``` .sh
.
├── LICENSE
├── pyproject.toml
├── README.md
├── src
│   ├── evident
│   │   └── prompts # < Here
│   └── tests
└── uv.lock

```

## Which format?

`.py` because this removes the headache of maintaining unnecessary 
.json or any other file.

With `.py` importing `PROMPTS` have made it easier for me, 
in terms of both maintaining and reducing headache of setup:

=== "`prompts/EXPANSION.py`"

    ``` python
    QUERYEXPANSION_SP = """
    HERE SYSTEM PROMPT
    """
    ```

=== "`source/model.py`"

    ``` python
    from evident.prompts import QUERYEXPANSION_SP


    agent = create_agent(
      model = "MODEL_CONFIGURATION",
      system_prompt = QUERYEXPANSION_SP,
      response_format = pytdantic_model,
    )
    ```

<br>
If I had used the previous configuration with the JSON file and 
the external function, it would have been a nightmare.
Because in .json you cannot have visual clarity over long values:

``` JSON
{"system_prompt": "You are an expert Zensical documentation assistant. Always produce technically accurate, concise, well-structured Markdown documentation following Zensical conventions, use YAML front matter for page metadata (title, description, icon, status, tags), maintain consistent heading hierarchy, valid internal links, navigation structure, code blocks, admonitions, and supported Markdown extensions, preserve existing project architecture and naming conventions, avoid unnecessary changes, verify assumptions against official documentation, and prioritize clarity, maintainability, accessibility, and correctness."}
```

Plus, adding another function to just read that json over multiple models (means same JSON file containing multiple system_prompts):

``` python
import json
from pathlib import Path


# Function for retrieving the system prompt from the system_prompt.json file
class SystemPrompt:
    def load(node) -> str:
        current_dir = Path(__file__).parent
        config_path = current_dir / "system_prompt.json"
        config_path = config_path.resolve()
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
            return config["node"][node]["system_prompt"]
```

> This code is referenced from my different project [vpipeline](https://github.com/DevankSinghChaudhary/VPipeline/blob/main/src/vcp/prompts/prompt.py)
