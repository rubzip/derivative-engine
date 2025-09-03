import math as m
from .core import Constant
from .expressions import Function, Power, Sum, Product


class Sinh(Function):
    derivate_fn = lambda arg: Cosh(arg)
    is_inverse = lambda x: isinstance(x, Asinh)
    symbol = "sinh"
    _is_linear: bool = False

    def __call__(self, x):
        return m.sinh(self.argument(x))


class Cosh(Function):
    derivate_fn = lambda arg: Sinh(arg)
    is_inverse = lambda x: isinstance(x, Acosh)
    symbol = "cosh"
    _is_linear: bool = False

    def __call__(self, x):
        return m.cosh(self.argument(x))


class Tanh(Function):
    derivate_fn = lambda arg: Power(Cosh(arg), Constant(-2))
    is_inverse = lambda x: isinstance(x, Atanh)
    symbol = "tanh"
    _is_linear: bool = False

    def __call__(self, x):
        return m.tanh(self.argument(x))


class Asinh(Function):
    derivate_fn = lambda arg: Power(
        Sum(Constant(1), Power(arg, Constant(2))), Constant(-0.5)
    )
    is_inverse = lambda x: isinstance(x, Sinh)
    symbol = "asinh"
    _is_linear: bool = False

    def __call__(self, x):
        return m.asinh(self.argument(x))


class Acosh(Function):
    derivate_fn = lambda arg: Power(
        Sum(Power(arg, Constant(2)), Constant(-1)), Constant(-0.5)
    )
    is_inverse = lambda x: isinstance(x, Cosh)
    symbol = "acosh"
    _is_linear: bool = False

    def __call__(self, x):
        return m.acosh(self.argument(x))


class Atanh(Function):
    derivate_fn = lambda arg: Power(
        Sum(Constant(1), Product(Constant(-1), Power(arg, Constant(2)))), Constant(-1)
    )
    is_inverse = lambda x: isinstance(x, Tanh)
    symbol = "atanh"
    _is_linear: bool = False

    def __call__(self, x):
        return m.atanh(self.argument(x))
