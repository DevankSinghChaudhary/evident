import os

from dotenv import load_dotenv
from tinyfish import TinyFish

from evident.sources import QueryExpansion

load_dotenv()

if "TINYFISH_API" not in os.environ:
    raise ValueError(
        "Configuration Error: TINYFISH_API is missing from your environment variables.\n"
        "Please set it before running the application."
    )
client = TinyFish(api_key=os.environ["TINYFISH_API"])


class Discovery:
    def __init__(self):
        self.query_expander = QueryExpansion()

    def source(self, query: str):
        expansion = self.query_expander.expand(query)
        return expansion.expanded
