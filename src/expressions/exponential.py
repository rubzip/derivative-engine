import math as m
from .basic import Expression, Division


class Logarithm(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument=argument)
    
    def derivative(self) -> Division:
        return Division(
            self.argument.derivative(),
            self.argument
        )
    
    def simplify(self):
        arg = self.argument.simplify()
        if isinstance(arg, Exponential):
            return arg.argument
        return Logarithm(arg)

    def __call__(self, x: float) -> float:
        return m.log(self.argument(x))
    
    def __str__(self):
        return f"ln({self.argument})"

class Exponential(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument, lambda arg: Exponential(arg))
    
    def simplify(self):
        arg = self.argument.simplify()
        if isinstance(arg, Logarithm):
            return arg.argument
        return Exponential(arg)
    
    def __call__(self, x):
        return m.exp(self.argument(x))

    def __str__(self):
        return f"exp({self.argument})"    
