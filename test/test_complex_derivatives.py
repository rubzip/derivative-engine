import math
from src.expressions.basic import Variable, Constant, Sum, Subtraction, Product, Division, Negation
from src.expressions.polynomial import Polynomial
from src.expressions.power import Power
from src.expressions.trigonometric import Sin, Cos, Tan
from src.expressions.hyperbolic import Sinh, Cosh, Tanh
from src.expressions.exponential import Logarithm
from src.test_utils import evaluate_derivative

VALUES = [0.1, 0.5, 1.0, 2.0, 3.0]

# ----------------------
# Sum + Product + Division
# f(x) = (x + 2) * (x - 3) / x
# f'(x) = [(1*(x-3)+(x+2)*1)*x - (x+2)*(x-3)*1]/x^2
#        = [2x-1]*?
def test_sum_product_division():
    x = Variable()
    expr = Division(
        Product(Sum(x, Constant(2)), Subtraction(x, Constant(3))),
        x
    )
    def expected_derivative(x_val):
        # d/dx [(x+2)(x-3)/x] = ((2x -1)*x - (x+2)(x-3))/x^2
        numerator = ((x_val + 2) * 1 + 1 * (x_val - 3)) * x_val - (x_val + 2)*(x_val - 3)
        denominator = x_val**2
        return numerator / denominator
    evaluate_derivative(expr, expected_derivative, VALUES)

# ----------------------
# Polynomial + Sin
# f(x) = sin(x^3)
# f'(x) = 3 * cos(x^3) * x^2
def test_sin_polynomial():
    x = Variable()
    expr = Sin(Polynomial(x, 3))  # sin(x^3)
    evaluate_derivative(expr, lambda x_val: math.cos(x_val**3) * 3 * x_val**2, VALUES)

# ----------------------
# Power with variable exponent
# f(x) = x^x
def test_power_variable_exponent():
    x = Variable()
    expr = Power(x, x)  # x^x
    evaluate_derivative(expr, lambda x_val: x_val**x_val * (1 + math.log(x_val)), VALUES)

# ----------------------
# Logarithm + Product
# f(x) = ln(x * (x + 1))
def test_log_product():
    x = Variable()
    expr = Logarithm(Product(x, Sum(x, Constant(1))))  # ln(x*(x+1))
    evaluate_derivative(expr, lambda x_val: 1/(x_val*(x_val+1)) * ((1*(x_val+1) + x_val*1)), VALUES)

# ----------------------
# Nested Trigonometric + Hyperbolic
# f(x) = cos(sinh(x)) + tanh(x)
def test_trig_hyperbolic():
    x = Variable()
    expr = Sum(Cos(Sinh(x)), Tanh(x))
    evaluate_derivative(expr, lambda x_val: -math.sin(math.sinh(x_val))*math.cosh(x_val) + 1/(math.cosh(x_val)**2), VALUES)

# ----------------------
# Negation + Division
# f(x) = - (x / (x+1))
def test_negation_division():
    x = Variable()
    expr = Negation(Division(x, Sum(x, Constant(1))))
    evaluate_derivative(expr, lambda x_val: -((1*(x_val+1) - x_val*1)/(x_val+1)**2), VALUES)
