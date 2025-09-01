import math as m
from .core import Expression, Function, Product, Negation
from .polynomial import Polynomial


class Sinh(Function):
    def __init__(self, argument: Expression):
        super().__init__(argument, derivative_fn=Cosh, fn_str="sinh")

    def __call__(self, x: float) -> float:
        return m.sinh(self.argument(x))


class Cosh(Function):
    def __init__(self, argument: Expression):
        super().__init__(argument, derivative_fn=Sinh, fn_str="cosh")

    def __call__(self, x: float) -> float:
        return m.cosh(self.argument(x))


class Tanh(Function):
    def __init__(self, argument: Expression):
        super().__init__(argument, lambda arg: Polynomial(Cosh(arg), -2), fn_str="tanh")

    def __call__(self, x: float) -> float:
        return m.tanh(self.argument(x))
