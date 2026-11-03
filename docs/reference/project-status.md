---
title: Project status and scope
description: What the current documentation establishes, and what remains implementation-dependent.
---

<div class="ev-kicker">Technical reference > Project status</div>

---

# Project status and scope

Evident is an actively developing project. Its documentation should distinguish the intended role of the engine from features that have been fully implemented and tested.

## Established project direction

- Evident is a research engine designed for AI systems and agents.
- It accepts a research topic as its conceptual input.
- It is designed to work independently of VPipeline.
- It is intended to provide multiple output formats, including PDF, JSON, and YAML.
- The current documented local model runtime is Ollama.
- The first documented setup is Linux-focused.

## Details that may evolve

The exact research stages, output schemas, model selection rules, supported model tags, and command-line interface are implementation details. They should be documented alongside the code once their interfaces are stable.

## Reporting an issue

When reporting a setup or runtime issue, include:

- Your Linux distribution and version.
- CPU, RAM, and GPU model, including available VRAM.
- Ollama version.
- The exact model tag.
- The command you ran and the complete error output.

Avoid including API keys, access tokens, or other secrets in issue reports.
