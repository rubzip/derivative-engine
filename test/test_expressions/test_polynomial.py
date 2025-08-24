from src.expressions.basic import Variable
from src.expressions.polynomial import Polynomial
from src.test_utils import evaluate_derivative

VALUES = [1, 2, 3, 4]

def test_polynomial_degree_3():
    expr = Polynomial(Variable(), 3)
    # derivada 3*x^2
    evaluate_derivative(expr, lambda x: 3*x**2, VALUES)

def test_polynomial_degree_1():
    expr = Polynomial(Variable(), 1)
    evaluate_derivative(expr, lambda x: 1, VALUES)

def test_polynomial_degree_0():
    expr = Polynomial(Variable(), 0)
    evaluate_derivative(expr, lambda x: 0, VALUES)
