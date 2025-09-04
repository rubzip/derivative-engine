import math as m

from .base import Expression, Constant
from .function_base import Function
from .operators import Sum, Product
from .exponential import Power


class Sin(Function):
    """Sine function."""
    symbol = "sin"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Cos(argument)
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Asin)
    
    def __call__(self, x):
        return m.sin(self.argument(x))


class Cos(Function):
    """Cosine function."""
    symbol = "cos"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Product(Constant(-1), Sin(argument))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Acos)

    def __call__(self, x):
        return m.cos(self.argument(x))


class Tan(Function):
    """Tangent function."""
    symbol = "tan"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Sum(Constant(1), Power(Tan(argument), Constant(2)))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Atan)
    
    def __call__(self, x):
        return m.tan(self.argument(x))


class Asin(Function):
    """Inverse sine function."""
    symbol = "asin"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Power(Sum(Constant(1), Product(Constant(-1), Power(argument, Constant(2)))), Constant(-0.5))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Sin)

    def __call__(self, x):
        return m.asin(self.argument(x))


class Acos(Function):
    """Inverse cosine function."""
    symbol = "acos"
    _is_linear: bool = False
    
    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Product(
            Constant(-1),
            (
                Power(
                    Sum(Constant(1), Product(Constant(-1), Power(argument, Constant(2)))),
                    Constant(-0.5),
                )
            ),
        )

    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Cos)
    
    def __call__(self, x):
        return m.acos(self.argument(x))


class Atan(Function):
    """Inverse tangent function."""
    symbol = "atan"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Power:
        return Power(Sum(Constant(1), Power(argument, Constant(2))), Constant(-1))

    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Tan)

    def __call__(self, x):
        return m.atan(self.argument(x))
