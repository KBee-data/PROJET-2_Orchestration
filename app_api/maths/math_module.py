"""Mathematical Operations Module.

Provides standard arithmetic helper functions used across the application.
"""


def add(a: int | float, b: int | float) -> int | float:
    """Calculate the sum of two numbers.

    Args:
        a (int | float): The first operand.
        b (int | float): The second operand.

    Returns:
        int | float: The sum of a and b.
    """
    return a + b


def sub(a: int | float, b: int | float) -> int | float:
    """Calculate the difference between two numbers.

    Args:
        a (int | float): The minuend.
        b (int | float): The subtrahend.

    Returns:
        int | float: The result of subtracting b from a.
    """
    return a - b


def square(a: int | float) -> int | float:
    """Calculate the square of a number.

    Args:
        a (int | float): The base number.

    Returns:
        int | float: The number multiplied by itself.
    """
    return a * a

