async def result():
    return 42


async def awaited_result():
    return await result()


coroutine = awaited_result()
try:
    coroutine.send(None)
except StopIteration:
    pass
else:
    raise AssertionError("coroutine did not complete")

print("PicoPython async/await syntax test: PASS")
