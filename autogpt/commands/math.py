"""Math evaluation module."""
from __future__ import annotations

from autogpt.commands.command import command

from sympy import sympify

@command(
    "evaluate_expression",
    "Evaluate mathematical expression using SymPy",
    '"expr": "<expression>"',
)
def evaluate_expression(expr: str) -> list[str]:
    """
    A function that takes in a string and evaluates the expression using SymPy

    Parameters:
        expr (str): expression to be evaluated.
    Returns:
        A result string from SymPy
    """
    return sympify(expr)
