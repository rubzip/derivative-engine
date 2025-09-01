import math as m

from .core import Expression, Constant, Conjunction, Sum, Product, Division
from .exponential import Logarithm
from .polynomial import Polynomial


class Power(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right, precedence_order=2, op_symbol='^')

    def derivative(self) -> Expression:
        return Product(
            Power(self.left, self.right),
            Sum(
                Product(self.right.derivative(), Logarithm(self.left)),
                Product(self.right, Division(self.left.derivative(), self.left)),
            ),
        )

    def simplify(self) -> Expression:
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(right, Constant):
            if right.value == 0:
                return Constant(1)
            if right.value == 1:
                return left
            if isinstance(left, Constant):
                return Constant(left.value**right.value)
            return Polynomial(left, right.value)
        return Power(left, right)

    def __call__(self, x: float) -> float:
        return self.left(x) ** self.right(x)

    def __str__(self):
        base_str = self._add_parentheses(self.left)
        if isinstance(self.right, Power):
            exponent_str = f"({self.right})"
        else:
            exponent_str = self._add_parentheses(self.right)
        return f"{base_str} ^ {exponent_str}"
