from src.expressions.basic import Constant, Variable
from src.expressions.conjunction import Negation
from src.test_utils import evaluate_derivative


VALUES = [1, 2, 5, 10, 20, 50, 100]

def test_constant():
    expresion = Constant(12)
    expected_derivative = lambda x: 0

    evaluate_derivative(expresion, expected_derivative, VALUES)

def test_variable():
    expresion = Variable()
    expected_derivative = lambda x: 1

    evaluate_derivative(expresion, expected_derivative, VALUES)

def test_negation():
    expresion = Negation(Constant(12))
    expected_derivative = lambda x: 0

    evaluate_derivative(expresion, expected_derivative, VALUES)

def test_negation_variable():
    expresion = Negation(Variable())
    expected_derivative = lambda x: -1

    evaluate_derivative(expresion, expected_derivative, VALUES)
