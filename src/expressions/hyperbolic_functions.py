import math as m
from .base import Expression, Constant
from .operators import Function, Power, Sum, Product


class Sinh(Function):
    symbol = "sinh"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Cosh(argument)
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Asinh)

    def __call__(self, x: float) -> float:
        return m.sinh(self.argument(x))


class Cosh(Function):
    symbol = "cosh"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Sinh(argument)
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Acosh)

    def __call__(self, x: float) -> float:
        return m.cosh(self.argument(x))


class Tanh(Function):
    symbol = "tanh"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Power(Cosh(argument), Constant(-2))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Atanh)

    def __call__(self, x: float) -> float:
        return m.tanh(self.argument(x))


class Asinh(Function):
    symbol = "asinh"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Power(Sum(Constant(1), Power(argument, Constant(2))), Constant(-0.5))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Sinh)

    def __call__(self, x: float) -> float:
        return m.asinh(self.argument(x))


class Acosh(Function):
    symbol = "acosh"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Power(Sum(Power(argument, Constant(2)), Constant(-1)), Constant(-0.5))
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Cosh)

    def __call__(self, x: float) -> float:
        return m.acosh(self.argument(x))


class Atanh(Function):
    symbol = "atanh"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Power(Sum(Constant(1), Product(Constant(-1), Power(argument, Constant(2)))), Constant(-1))

    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return isinstance(argument, Tanh)

    def __call__(self, x: float) -> float:
        return m.atanh(self.argument(x))
