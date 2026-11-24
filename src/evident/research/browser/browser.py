from evident.research.browser.decision import Decision

decision = Decision(model="tev1:4b")

# Explicitly allow the interactive installation flow.
decision.setup(interactive=True)

result = decision.call(
    output_method="noul",
    state="A webpage contains a documentation article about Python.",
    instruction="Classify the type of webpage.",
    criteria=
)

print(result)
