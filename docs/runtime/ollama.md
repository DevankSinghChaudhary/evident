---
title: Ollama runtime
description: Notes for using Ollama as Evident's current local model runtime.
---

# Ollama runtime

Evident's current setup uses [Ollama](https://ollama.com/) to run models locally.

Ollama is the runtime layer. It is not Evident itself: Evident is the research engine, while Ollama provides a local interface for running the selected model.

## Install

On Arch Linux, the currently documented command is:

```bash
yay -S ollama-cuda
```

This is the CUDA-enabled package used in the project's current Linux setup. If your system does not use an NVIDIA GPU, check the package's current requirements and choose an appropriate Ollama installation for your environment.

## Pull the current example model

```bash
ollama pull kev:4b-q4_K_M
```

The model tag above is the current example recorded in the project setup. Model tags can change or become unavailable, so verify the tag if Ollama cannot find it.

## Start the service

How Ollama is started depends on how it was installed and configured on your distribution. On systems using systemd, check the package instructions and service status rather than assuming the service is already running.

You can verify that the Ollama command is available with:

```bash
ollama --version
```

## Hardware notes

A 4B model can be substantially more demanding than a small specialist decision model. Check available RAM, GPU memory, quantization, and runtime compatibility before selecting a model.

See [System requirements](../reference/requirements.md) for Evident's current baseline.
