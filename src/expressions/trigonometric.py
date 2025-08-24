import math as m
from .basic import Expression, Constant, Division, Product, Negation, Sum
from .polynomial import Polynomial


class Sin(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument, derivative_class=Cos)

    def __call__(self, x: float) -> float:
        return m.sin(self.argument(x))

    def __str__(self):
        return f"sin({self.argument})"


class Cos(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument, derivative_class=lambda x: Negation(Sin(x)))

    def __call__(self, x: float) -> float:
        return m.cos(self.argument(x))

    def __str__(self):
        return f"cos({self.argument})"


class Tan(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument, lambda arg: Polynomial(Cos(arg), -2))

    def __call__(self, x: float) -> float:
        return m.tan(self.argument(x))

    def __str__(self):
        return f"tan({self.argument})"
