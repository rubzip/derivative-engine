import math as m
from .core import Expression, Function, Constant, Division, Product, Negation, Sum
from .polynomial import Polynomial


class Sin(Function):
    def __init__(self, argument: Expression, quantity: float = 1.):
        super().__init__(argument, derivative_fn=Cos, fn_str="sin", is_inverse=lambda x: isinstance(x, Asin))

    def __call__(self, x: float) -> float:
        return m.sin(self.argument(x))

    def __str__(self):
        return f"sin({self.argument})"


class Cos(Function):
    def __init__(self, argument: Expression, quantity: float = 1.):
        super().__init__(argument, derivative_fn=lambda x: Negation(Sin(x)), fn_str="cos")

    def __call__(self, x: float) -> float:
        return m.cos(self.argument(x))

    def __str__(self):
        return f"cos({self.argument})"


class Tan(Function):
    def __init__(self, argument: Expression, quantity: float = 1.):
        super().__init__(argument, lambda arg: Polynomial(Cos(arg), -2), fn_str="tan")

    def __call__(self, x: float) -> float:
        return m.tan(self.argument(x))

    def __str__(self):
        return f"tan({self.argument})"

class Acos(Function):
    def __init__(self, argument, quantity):
        super().__init__(quantity, argument, derivative_fn, is_inverse, symbol='acos', _is_linear)
