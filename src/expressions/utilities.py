from .base import Expression, Constant
from .operators import Product
from .exponential import Power
from .function_base import Function


class Division:
    def __new__(cls, dividend: Expression, divisor: Expression) -> Expression:
        if divisor == Constant(0):
            raise ZeroDivisionError("You can't divide by zero")
        if divisor == Constant(1):
            return dividend
        if dividend == Constant(0):
            return Constant(0)

        return Product(dividend, Power(divisor, Constant(-1)))


class Negation:
    def __new__(cls, argument: Expression) -> Expression:
        if isinstance(argument, Constant):
            return Constant(-argument.value)
        return Product(Constant(-1), argument)

class Sqrt:
    def __new__(cls, argument: Expression) -> Expression:
        return Power(argument, Constant(0.5))

class Abs(Function):
    symbol = "abs"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Sign(argument)
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return False

    def __call__(self, x):
        return abs(self.argument(x))

    def simplify(self):
        arg = self.argument.simplify()
        if isinstance(arg, Constant):
            return Constant(abs(arg.value))
        if isinstance(arg, Abs):
            return arg
        return Abs(argument=arg)


class Sign(Function):
    symbol = "sign"
    _is_linear: bool = False

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        return Constant(0)
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        return False
    
    def __call__(self, x):
        val = self.argument(x)
        return 1 if val > 0 else -1 if val < 0 else 0

    def simplify(self):
        arg = self.argument.simplify()
        if isinstance(arg, Constant):
            return Constant(1 if arg.value > 0 else -1 if arg.value < 0 else 0)
        if isinstance(arg, Sign):
            return arg
        return Sign(argument=arg)
