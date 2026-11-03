---
title: Core concepts
description: The role Evident is designed to play in an AI research workflow.
---

<div class="ev-kicker">Overview > Core concepts</div>

---

# Core concepts

Evident is intended to act as a dedicated research component inside a larger AI workflow.

Its input is a research topic. Its outputs are intended to be useful both to a person and to another software component.

## A decoupled research engine

Evident was created for [VPipeline](https://github.com/devanksinghchaudhary/vpipeline). Keeping the research engine decoupled means it can be used without requiring the rest of that pipeline.

That separation has two practical consequences:

- Evident can be developed and run as an independent project.
- A larger application can use Evident as one component rather than owning the research logic itself.

## Input and output

The project's current documented interface is deliberately simple at the conceptual level:

| Part | Role |
|---|---|
| Input | A research topic |
| Engine | Evident's research process |
| Output | Research results in formats such as PDF, JSON, and YAML |

The exact schemas, available formats, and supported invocation methods should be treated as implementation details that may evolve while the project is under development.

## Decision models

The project is exploring decision models for focused decisions within the research workflow. These are distinct from using a large general-purpose language model for every decision.

The current local setup uses Ollama. Model size and hardware needs depend on the particular model being run.

## Relationship with VPipeline

VPipeline is a potential consumer of Evident's research output. The projects have separate responsibilities:

- **Evident** — the research engine.
- **VPipeline** — the broader video/documentary production workflow.

This boundary allows either project to change without requiring the other to become a monolith.
