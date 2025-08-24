import pytest

from src.parser.parser import parse
from src.expressions import Expression, Conjunction, Constant, Variable, Sum, Product, Sin, Cos, Tan, Power, Sinh, Division, Exponential


def check_equal(expected: Expression, expr_str: str):
    """Parse expr_str and compare its AST with expected."""
    parsed = parse(expr_str)
    assert parsed == expected, f"Expected {expected}, got {parsed}"

@pytest.mark.parametrize("expr, expr_str", [
    (Sum(Constant(2), Constant(3)), "2+3"),
    (Product(Constant(2), Variable()), "2*x"),
    (Sum(Variable(), Constant(1)), "(x+1)"),
    (Sin(Variable()), "sin(x)"),
    (Cos(Product(Constant(2), Variable())), "cos(2*x)"),
    (Tan(Power(Variable(), Constant(2))), "(tan(x^2))"),
    (Sum(Sinh(Variable()), Variable()), "sinh(x)+x"),
    (Division(Exponential(Variable()), Constant(2)), "exp(x)/2"),
])
def test_parser(expr, expr_str):
    check_equal(expr, expr_str)
