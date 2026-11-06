import asyncio

from evident.sources import Discovery


async def main():
    discover = Discovery()
    queries = await discover.source("Fermi Paradox")
    print(queries)


if __name__ == "__main__":
    asyncio.run(main())
