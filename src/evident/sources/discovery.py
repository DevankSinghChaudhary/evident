import time

from evident.models import QueryExpansion

st = time.time()


class Discovery:
    def __init__(self):
        self.query_expander = QueryExpansion()

    async def source(self, query: str):
        expansion = await self.query_expander.expand(query)
        print(f"Total Timed: {time.time() - st:.2f}")
        return expansion
