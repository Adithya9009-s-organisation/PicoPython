def identity(function):
    return function


@identity
def decorated(value: int, /, extra=0, *, offset=0) -> int:
    return value + extra + offset


def comprehension_and_unpacking(items):
    squares = {item: item * item for item in items}
    evens = {item for item in items if item % 2 == 0}
    generated = (item + 1 for item in items)
    first, *middle, last = items
    return squares, evens, list(generated), first, middle, last


def keyword_unpacking(function, arguments):
    return function(**arguments)


def update_closure():
    value = 0

    def update():
        nonlocal value
        value += 1

    update()
    return value


async def async_value():
    return 42


async def await_value():
    return await async_value()


def assignment_expression():
    if (value := len("PicoPython")):
        return value
    return 0


def chained_exception():
    try:
        raise ValueError("inner")
    except ValueError as error:
        raise RuntimeError("outer") from error


number: int = 42

assert decorated(1, 2, offset=3) == 6
assert comprehension_and_unpacking([1, 2, 3]) == (
    {1: 1, 2: 4, 3: 9},
    {2},
    [2, 3, 4],
    1,
    [2],
    3,
)
assert update_closure() == 1
assert assignment_expression() == 10
assert number == 42
print("PicoPython syntax compatibility tests: PASS")
