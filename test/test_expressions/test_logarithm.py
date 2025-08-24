import math
from src.expressions.basic import Variable
from src.expressions.exponential import Logarithm
from src.test_utils import evaluate_derivative

VALUES = [0.1, 0.5, 1.0, 2.0]

def test_logarithm():
    expr = Logarithm(Variable())
    evaluate_derivative(expr, lambda x: 1/x, VALUES)
