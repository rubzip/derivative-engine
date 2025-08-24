import math

from src.expressions.basic import Variable, Constant
from src.expressions.power import Power
from src.test_utils import evaluate_derivative

VALUES = [1, 2, 3]


def test_power_constant_exponent():
    expr = Power(Variable(), Constant(3))  # x^3
    evaluate_derivative(expr, lambda x: 3 * x**2, VALUES)


def test_power_variable_exponent():
    expr = Power(Variable(), Variable())  # x^x
    evaluate_derivative(expr, lambda x: x**x * (1 + math.log(x)), VALUES)
