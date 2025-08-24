import math
from src.expressions.basic import Variable
from src.expressions.hyperbolic import Sinh, Cosh, Tanh
from src.test_utils import evaluate_derivative

VALUES = [0.1, 0.5, 1.0, 2.0]


def test_sinh():
    expr = Sinh(Variable())
    evaluate_derivative(expr, lambda x: math.cosh(x), VALUES)


def test_cosh():
    expr = Cosh(Variable())
    evaluate_derivative(expr, lambda x: math.sinh(x), VALUES)


def test_tanh():
    expr = Tanh(Variable())
    evaluate_derivative(expr, lambda x: 1 / math.cosh(x) ** 2, VALUES)
