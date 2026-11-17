assert (lambda x: x + 1)(2) == 3


class Base:
    def value(self):
        return 40


class Child(Base):
    def value(self):
        return super().value() + 2


assert Child().value() == 42
assert [x * x for x in range(5) if x % 2 == 0] == [0, 4, 16]
assert list(x + 1 for x in range(3)) == [1, 2, 3]
assert {x: x * x for x in range(3)} == {0: 0, 1: 1, 2: 4}
assert f"value={42}" == "value=42"

try:
    1 / 0
except ZeroDivisionError:
    pass
else:
    raise AssertionError("ZeroDivisionError was not raised")

print("PicoPython core language tests: PASS")
