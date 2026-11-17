import asyncio


async def result():
    return 42


assert asyncio.run(result()) == 42
print("PicoPython asyncio test: PASS")
