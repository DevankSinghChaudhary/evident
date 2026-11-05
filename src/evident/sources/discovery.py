import os

from dotenv import load_dotenv
from tinyfish import TinyFish

from evident.sources import QueryExpansion

load_dotenv()
client = TinyFish(api_key=os.environ["TINYFISH_API"])


class Discovery:
    def __init__(self):
        self.query_expander = QueryExpansion()

    def source(self, query: str):
        expansion = self.query_expander.expand(query)
        print(expansion)
        print()
        print(expansion.expanded)


discover = Discovery()
result = discover.source("How Black Hole Works?")
print(result)
