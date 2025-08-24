import math
from src.expressions.basic import Variable
from src.expressions.trigonometric import Sin, Cos, Tan
from src.test_utils import evaluate_derivative

VALUES = [0.1, 0.5, 1.0, 2.0]


def test_sin():
    expr = Sin(Variable())
    evaluate_derivative(expr, lambda x: math.cos(x), VALUES)


def test_cos():
    expr = Cos(Variable())
    evaluate_derivative(expr, lambda x: -math.sin(x), VALUES)


def test_tan():
    expr = Tan(Variable())
    evaluate_derivative(expr, lambda x: 1 / math.cos(x) ** 2, VALUES)
