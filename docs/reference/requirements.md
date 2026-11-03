---
title: System requirements
description: Current documented hardware baseline for running Evident's model workflow.
---

# System requirements

The following table preserves the current hardware baseline recorded for the project. Actual resource use depends on the model, quantization, context size, and runtime.

| Component | Minimum | Recommended |
|---|---:|---:|
| GPU VRAM | Not required | 6 GB or more |
| System RAM | 8 GB | 16 GB |
| CPU | 4-core x86-64 processor | 6-core or higher x86-64 processor |

!!! info "GPU acceleration"
    A dedicated GPU is not listed as a minimum requirement. A compatible GPU is recommended for better performance where the selected model and runtime can use it.

!!! warning "The 4B model is a larger workload"
    The baseline above should not be interpreted as a guarantee that the 4B example model will run comfortably on every minimum-spec machine. Larger models can require significantly more memory and compute.

## Compatibility

The first version is currently Linux-focused and has been tested on Linux. Other operating systems should be considered unverified until they are tested and documented.
