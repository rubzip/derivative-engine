import math
from src.expressions.basic import Variable, Constant, Sum, Product, Division, Negation
from src.expressions.polynomial import Polynomial
from src.expressions.power import Power
from src.expressions.trigonometric import Sin, Cos, Tan
from src.expressions.hyperbolic import Sinh, Cosh, Tanh
from src.expressions.exponential import Logarithm
from src.test_utils import evaluate_derivative

VALUES = [0.1, 0.5, 1.0, 2.0, 3.0]

# ----------------------
# 1. Sin(x^3 + ln(x))
def test_sin_polynomial_log():
    x = Variable()
    expr = Sin(Sum(Polynomial(x, 3), Logarithm(x)))
    evaluate_derivative(expr, lambda x_val: math.cos(x_val**3 + math.log(x_val)) * (3*x_val**2 + 1/x_val), VALUES)

# ----------------------
# 2. sinh(x) * cos(x^2)
def test_sinh_cos_polynomial():
    x = Variable()
    expr = Product(Sinh(x), Cos(Polynomial(x, 2)))
    evaluate_derivative(expr, lambda x_val: math.cosh(x_val)*math.cos(x_val**2) - 2*x_val*math.sinh(x_val)*math.sin(x_val**2), VALUES)

# ----------------------
# 3. (x^2 + 1) / (x + 1)^3
def test_division_power_polynomial():
    x = Variable()
    numerator = Sum(Polynomial(x, 2), Constant(1))
    denominator = Power(Sum(x, Constant(1)), Constant(3))
    expr = Division(numerator, denominator)
    evaluate_derivative(expr, lambda x_val: ((2*x_val)*(x_val+1)**3 - (x_val**2+1)*3*(x_val+1)**2) / (x_val+1)**6, VALUES)

# ----------------------
# 4. tanh(x^2 + sin(x))
def test_tanh_polynomial_trig():
    x = Variable()
    expr = Tanh(Sum(Polynomial(x, 2), Sin(x)))
    evaluate_derivative(expr, lambda x_val: 1/math.cosh(x_val**2 + math.sin(x_val))**2 * (2*x_val + math.cos(x_val)), VALUES)

# ----------------------
# 5. -(-x^2 + sin(x))
def test_nested_negation():
    x = Variable()
    expr = Negation(Sum(Negation(Polynomial(x, 2)), Sin(x)))
    evaluate_derivative(expr, lambda x_val: 2*x_val + math.cos(x_val), VALUES)

# ----------------------
# 6. ln(x^2 + x + 1)
def test_log_polynomial_sum():
    x = Variable()
    expr = Logarithm(Sum(Sum(Polynomial(x,2), x), Constant(1)))
    evaluate_derivative(expr, lambda x_val: (2*x_val + 1) / (x_val**2 + x_val + 1), VALUES)

# ----------------------
# 7. cos(x^3 * sin(x))
def test_cos_polynomial_trig_product():
    x = Variable()
    expr = Cos(Product(Polynomial(x,3), Sin(x)))
    evaluate_derivative(expr, lambda x_val: -math.sin(x_val**3*math.sin(x_val)) * (3*x_val**2*math.sin(x_val) + x_val**3*math.cos(x_val)), VALUES)

# ----------------------
# 8. (x + 1)^x
def test_power_variable_exponent():
    x = Variable()
    expr = Power(Sum(x, Constant(1)), x)
    evaluate_derivative(expr, lambda x_val: (x_val+1)**x_val * (math.log(x_val+1) + x_val/(x_val+1)), VALUES)

# ----------------------
# 9. sin(tanh(x)) + ln(cosh(x))
def test_trig_hyper_log():
    x = Variable()
    expr = Sum(Sin(Tanh(x)), Logarithm(Cosh(x)))
    evaluate_derivative(expr, lambda x_val: math.cos(math.tanh(x_val))*(1/math.cosh(x_val)**2) + math.tanh(x_val), VALUES)

# ----------------------
# 10. Complex nested combination
# f(x) = ((x^2 + 1)*sin(x) + cos(x^3)) / (x + tanh(x))
def test_complex_nested():
    x = Variable()
    numerator = Sum(Product(Sum(Polynomial(x,2), Constant(1)), Sin(x)), Cos(Polynomial(x,3)))
    denominator = Sum(x, Tanh(x))
    expr = Division(numerator, denominator)
    def expected_derivative(x_val):
        num = ((2*x_val)*(1) + 0)*math.sin(x_val) + (x_val**2+1)*math.cos(x_val) + -math.sin(x_val**3)*3*x_val**2
        den = x_val + math.tanh(x_val)
        der_num = ((2*x_val)*math.sin(x_val) + (x_val**2+1)*math.cos(x_val) - 3*x_val**2*math.sin(x_val**3))
        der_den = 1 + 1/math.cosh(x_val)**2
        return (der_num*den - num*der_den) / den**2
    evaluate_derivative(expr, expected_derivative, VALUES)
