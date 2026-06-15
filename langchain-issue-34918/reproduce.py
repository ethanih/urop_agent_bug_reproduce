import asyncio


async def empty_stream():
    if False:
        yield None


async def aggregate_stream(stream):
    got_data = False
    async for chunk in stream:
        got_data = True
        print("chunk:", chunk)
    if not got_data:
        raise ValueError("No data received from Ollama stream.")


async def main():
    try:
        await aggregate_stream(empty_stream())
    except ValueError as exc:
        print("BUG CONFIRMED:", exc)


if __name__ == "__main__":
    asyncio.run(main())
