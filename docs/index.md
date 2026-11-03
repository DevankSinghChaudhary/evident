---
title: Evident
description: A decoupled research engine designed for AI systems and agents.
---

# Give AI systems a way to research.

Evident is a research engine built for AI systems and agents. It is designed to take a research topic as input and produce structured research outputs that can be used independently or passed into a larger workflow.

It was originally built for [VPipeline](https://github.com/devanksinghchaudhary/vpipeline), but its engine is decoupled so it can also be used as a standalone component.

<div class="ev-action-row">
  <a class="ev-button ev-button-primary" href="get-started/">Get started <span>↗</span></a>
  <a class="ev-button ev-button-secondary" href="concepts/">Explore the project</a>
</div>


## The idea

AI workflows often need more than a generated paragraph. They need research that can be handed from one component to another.

Evident is intended to provide that research layer: a component that accepts a topic and makes its results available in formats that other software can consume.

-   **Independent engine:** Use Evident on its own. It does not require VPipeline to be present.
-   **Workflow-compatible:** Evident can be coupled with VPipeline when research is one stage in a larger content-production process.
-   **Structured results:** The project targets multiple output formats, including PDF, JSON, and YAML.
-   **Local model runtime:** The current setup uses Ollama to run decision models on the user's own machine.


## Where it fits

``` mermaid
flowchart LR
    A["Research topic"] --> B["Evident"]
    B --> C["Research output"]
    C --> D["Standalone use"]
    C --> E["VPipeline or another workflow"]
```

This is the high-level role of the project, not a promise that every stage or output format is already implemented.

## Start here

- [Get started](get-started.md) — prepare your machine and install the runtime.
- [Core concepts](concepts.md) — understand Evident's role and design boundaries.
- [Ollama runtime](runtime/ollama.md) — configure the current local model runtime.
- [System requirements](reference/requirements.md) — review the documented hardware baseline.
