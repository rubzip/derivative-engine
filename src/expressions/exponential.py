import math as m
from .base import Expression, Constant
from .function_base import Function
from .operators import Sum, Product


class Power(Expression):
    def __init__(self, base: Expression, factor: Expression):
        super().__init__(precedence=3)
        self.base = base
        self.factor = factor

    def derivate(self) -> Expression:
        f, g = self.base, self.factor
        term1 = Product(self.copy(), Log(f), g.derivate())
        term2 = Product(self.copy(), g, f.derivate(), Power(f, Constant(-1)))
        return Sum(term1, term2).simplify()

    def simplify(self) -> Expression:
        base = self.base.simplify()
        if base == Constant(0) or base == Constant(1):
            return base

        factor = self.factor.simplify()
        if factor == Constant(1):
            return base
        if factor == Constant(0):
            return Constant(1)

        if isinstance(base, Power):
            return Power(base.base, Product(base.factor, factor)).simplify()

        return Power(base, factor)

    def copy(self) -> "Power":
        return Power(self.base.copy(), self.factor.copy())

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Power)
            and self.base == other.base
            and self.factor == other.factor
        )

    def __call__(self, x: float) -> float:
        return self.base(x) ** self.factor(x)

    def __str__(self):
        base_str = self._add_parentheses(self.base)
        factor_str = self._add_parentheses(self.factor)

        return f"{base_str}^{factor_str}"

    def __hash__(self):
        return hash(("^", self.base, self.factor))


class Log(Function):
    symbol = "log"
    _is_linear = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Power(argument, Constant(-1))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Exp)

    def __call__(self, x: float) -> float:
        return m.log(self.argument(x))


class Exp(Function):
    symbol = "exp"
    _is_linear = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Exp(argument, Constant(-1))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Log)

    def __call__(self, x: float) -> float:
        return m.exp(self.argument(x))
