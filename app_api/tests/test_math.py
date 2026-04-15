# tests/test_math.py

from maths.math_module import add, sub, square


def test_add():
    assert add(2, 3) == 5


def test_sub():
    assert sub(5, 3) == 2


def test_square():
    assert square(4) == 16
