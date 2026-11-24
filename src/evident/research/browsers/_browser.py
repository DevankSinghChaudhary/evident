from browser.core import Agent
from evident.research.browsers.decision import Decision

decision = Decision(model="tev1:4b")

# Explicitly allow the interactive installation flow.
decision.setup(interactive=True)

result = decision.call(
    output_method="choice",
    state="A webpage contains a documentation article about Python.",
    instruction="Classify the type of webpage.",
    criteria={
        "documentation": "Technical documentation or guides",
        "blog": "An article or personal blog post",
        "other": "Anything else",
    },
)

with Agent(
    "https://www.google.com/maps",
    "Find me Restaurent in Jaipur on the maps."
    "Stop when found 1st restaurent in Raja-Park area."
    "Dont stop when filled the search, actual search it",
    jev=False,
    codex=True,
) as agent:
    previous_elapsed = 0

    for state in agent.run():
        elapsed = state.get("elapsed_ms", 0)
        step_time = elapsed - previous_elapsed
        previous_elapsed = elapsed

        page = state.get("page", {})
        decisions = state.get("decisions", [])
        history = state.get("history", [])

        print(f"\n{'=' * 55}")
        print(f"Status:       {state.get('status')}")
        print(f"Current URL:  {page.get('url', 'Unknown')}")
        print(f"Step time:    {step_time} ms")
        print(f"Total time:   {elapsed} ms")

        if decisions:
            decision = decisions[-1]

            print("\nDECISION")
            print(f"Operation:   {decision.get('operation')}")
            print(f"Choice:      {decision.get('choice')}")
            print(f"Target:      {decision.get('target')}")
            print(f"Confidence:  {decision.get('confidence')}")
            print(f"Latency:     {decision.get('latency_ms')} ms")
            print(f"Probabilities: {decision.get('probabilities')}")

        if history:
            action = history[-1]

            print("\nEXECUTION")
            print(f"Action:          {action.get('action')}")
            print(f"Action type:     {action.get('kind')}")
            print(f"Page changed:    {action.get('page_changed')}")
            print(f"Decision time:   {action.get('latency_ms')} ms")
            print(f"Text model time: {action.get('text_latency_ms')} ms")
            print(f"Text model:      {action.get('text_helper')}")
