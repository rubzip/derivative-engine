import math as m
from .core import Expression, Function, Constant, Power, Sum, Product
from .polynomial import Polynomial


class Sin(Function):
    derivate_fn = lambda arg: Cos(arg)
    is_inverse = lambda x: isinstance(x, Asin)
    symbol = "sin"
    _is_linear: bool = False

    def __call__(self, x):
        return m.sin(self.argument(x))

class Cos(Function):
    derivate_fn = lambda arg: Product(Constant(-1), Sin(arg))
    is_inverse = lambda x: isinstance(x, Acos)
    symbol = "cos"
    _is_linear: bool = False

    def __call__(self, x):
        return m.cos(self.argument(x))

class Tan(Function):
    derivate_fn = lambda arg: Power(Cos(arg), Constant(-2))
    is_inverse = lambda x: isinstance(x, Atan)
    symbol = "tan"
    _is_linear: bool = False

    def __call__(self, x):
        return m.tan(self.argument(x))

class Asin(Function):
    derivate_fn = lambda arg: Power(Sum(Constant(1), Product(Constant(-1), Power(arg, Constant(2)))), Constant(-0.5))
    is_inverse = lambda x: isinstance(x, Sin)
    symbol = "asin"
    _is_linear: bool = False

    def __call__(self, x):
        return m.asin(self.argument(x))

class Acos(Function):
    derivate_fn = lambda arg: Product(Constant(-1), (Power(Sum(Constant(1), Product(Constant(-1), Power(arg, Constant(2)))), Constant(-0.5))))
    is_inverse = lambda x: isinstance(x, Cos)
    symbol = "acos"
    _is_linear: bool = False

    def __call__(self, x):
        return m.acos(self.argument(x))

class Atan(Function):
    derivate_fn = lambda arg: Power(Sum(Constant(1), Power(arg, Constant(2))), Constant(-1))
    is_inverse = lambda x: isinstance(x, Tan)
    symbol = "atan"
    _is_linear: bool = False

    def __call__(self, x):
        return m.atan(self.argument(x))
