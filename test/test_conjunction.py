from src.expressions.basic import Constant, Variable
from src.expressions.conjunction import Sum, Substraction, Product, Division
from src.test_utils import evaluate_derivative

VALUES = [1, 2, 5, 10, 20]

def test_sum_1():
    expr = Sum(Variable(), Constant(3))
    evaluate_derivative(expr, lambda x: 1, VALUES)

def test_sum_2():
    expr = Sum(Variable(), Variable())
    evaluate_derivative(expr, lambda x: 2, VALUES)

def test_sum_3():
    expr = Sum(Variable(), Sum(Variable(), Variable()))
    evaluate_derivative(expr, lambda x: 3, VALUES)

def test_substraction_1():
    expr = Substraction(Variable(), Constant(5))
    evaluate_derivative(expr, lambda x: 1, VALUES)

def test_substraction_2():
    expr = Substraction(Variable(), Variable())
    evaluate_derivative(expr, lambda x: 0, VALUES)

def test_substraction_3():
    expr = Substraction(Constant(5), Variable())
    evaluate_derivative(expr, lambda x: -1, VALUES)

def test_product_1():
    expr = Product(Variable(), Constant(4))
    evaluate_derivative(expr, lambda x: 4, VALUES)

def test_product_2():
    expr = Product(Variable(), Variable())
    evaluate_derivative(expr, lambda x: 2*x, VALUES)

def test_division():
    expr = Division(Variable(), Constant(2))
    evaluate_derivative(expr, lambda x: 0.5, VALUES)

def test_division_fool():
    expr = Division(Variable(), Variable())
    evaluate_derivative(expr, lambda x: 0, VALUES)
