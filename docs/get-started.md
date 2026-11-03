---
title: Get started
description: Prepare a Linux machine and the local model runtime for Evident.
---

# Get started

This guide covers the current documented setup for Evident. The first version is being developed and tested on Linux.

There are two parts to the setup:

1. **Hardware:** the machine that runs the model.
2. **Runtime software:** the application used to serve the model locally.

You do not need a server-class machine for the smaller decision-model direction of the project. The current target includes models in the hundreds of millions of parameters, with a larger 4B model also being considered. The larger model has a higher resource requirement.

## 1. Check your hardware

Review the [system requirements](reference/requirements.md) before installing anything.

The minimum baseline does not require a dedicated GPU. A supported GPU can improve model performance, depending on the model and runtime configuration.

## 2. Install Ollama

Evident's current setup uses [Ollama](https://ollama.com/) as its local model runtime.

On Arch Linux, the project setup currently documents the CUDA-enabled AUR package:

```bash
yay -S ollama-cuda
```

Package availability and installation instructions can change. If you use another Linux distribution, follow the installation instructions provided by the [official Ollama website](https://ollama.com/).

## 3. Download the model

The current example model reference is:

```bash
ollama pull kev:4b-q4_K_M
```

This downloads the model into Ollama. The 4B model is a larger option and may require more resources than the smaller decision-model targets.

For model-specific requirements and compatibility, consult the model's own documentation. Do not assume that every model will perform well on the minimum hardware baseline.

## 4. Continue

Once the runtime and model are available, continue with the [Ollama runtime notes](runtime/ollama.md).

!!! warning "Development status"
    These instructions describe the current documented Linux setup. They are not a claim of cross-platform support or a guarantee that every listed model is compatible with every machine.
