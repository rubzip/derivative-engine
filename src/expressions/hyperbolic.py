import math as m
from .basic import Expression, Product, Negation
from .polynomial import Polynomial


class Sinh(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument, derivative_class=Cosh)

    def __call__(self, x: float) -> float:
        return m.sinh(self.argument(x))

    def __str__(self):
        return f"sinh({self.argument})"


class Cosh(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument, derivative_class=lambda x: Sinh(x))

    def __call__(self, x: float) -> float:
        return m.cosh(self.argument(x))

    def __str__(self):
        return f"cosh({self.argument})"


class Tanh(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument, lambda arg: Polynomial(Cosh(arg), -2))

    def __call__(self, x: float) -> float:
        return m.tanh(self.argument(x))

    def __str__(self):
        return f"tanh({self.argument})"
