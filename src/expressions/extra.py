from .core import Expression, Constant, Product, Power, Function

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

class Abs(Function):
    derivate_fn = lambda arg: Sign(arg)
    is_inverse = lambda x: False
    symbol = "abs"
    _is_linear: bool = False

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
    derivate_fn = lambda arg: Constant(0)
    is_inverse = lambda x: False
    symbol = "sign"
    _is_linear: bool = False

    def __call__(self, x):
        val = self.argument(x)
        return 1 if val > 0 else -1 if val < 0 else 0
