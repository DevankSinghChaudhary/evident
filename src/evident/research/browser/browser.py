from evident.research.browser.decision import Decision

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

print(result)
