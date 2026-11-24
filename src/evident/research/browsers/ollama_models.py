import httpx
import ollama

BASE_URL = "https://ollama.kinduff.com/api"


def decision_models():
    response = httpx.get(
        f"{BASE_URL}/models",
        params={"capability": "decision"},
        timeout=15,
    )
    response.raise_for_status()

    names = []
    for model_name in response.json()["models"]:
        for size in model_name["sizes"]:
            names.append(f"{model_name['name']}:{size}")
    return names


def download_model(model: str):
    stream = ollama.pull(model, stream=True)
    last_status = None

    for chunk in stream:
        if chunk.total and chunk.completed is not None:
            percent = (chunk.completed / chunk.total) * 100
            print(f"\r{chunk.status}: {percent:.1f}%\033[K", end="", flush=True)
            last_status = chunk.status
        elif chunk.status != last_status:
            if (
                last_status
                and last_status.startswith("pulling ")
                and last_status != "pulling manifest"
            ):
                print()
            print(chunk.status, flush=True)
            last_status = chunk.status
    print()
