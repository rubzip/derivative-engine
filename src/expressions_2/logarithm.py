import math as m
from .basic import Expresion, Division


class Logarithm(Expresion):
    def __init__(self, argument: Expresion):
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

class Exponential(Expresion):
    def __init__(self, argument: Expresion):
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
