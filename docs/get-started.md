# Get started

To start with evident you need some prerequisites, there are two types of prerequisites:  
  
- Hardware, and
- Application such as Ollama
  
Because you need to run essentially models on your hardware. However, you do not need to have crazy servers instead consumer hardware because we will be running only decision models which are few hundered million parameters. But we will be running 4B decision model which will require significant more hardware requirement but in limit.

---

## Hardware requirement

|Hardware|Minimum|Recommended|
|---|---|---|
|GPU VRAM|not required|6GB+|
|RAM|8GB|16GB|
|CPU|4-cores x86-64 processor|6-cores or higher x86-64 processor|

!!! warning "GPU Requirement"

    Even though GPU VRAM is not required in minimum but GPU should be present for better results in decision models.

---

## Application requirement

For evident there is decision model requirement. So, for that we need [Ollama](https://www.ollama.com).

!!! important "Linux tested only"

    This is all linux tested so first version is linux based.

Install ollam:

```bash
yay -S ollama-cuda

```

Pull model:

```bash
ollama pull kev:4b-q4_K_M

```


