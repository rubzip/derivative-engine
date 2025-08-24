import math as m
from .basic import Expresion, Product, Negation
from .polynomial import Polynomial

class Sinh(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument, derivative_class=Cosh)
    
    def __call__(self, x: float) -> float:
        return m.sinh(self.argument(x))

    def __str__(self):
        return f"sinh({self.argument})"

class Cosh(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument, derivative_class=lambda x: Sinh(x))
    
    def __call__(self, x: float) -> float:
        return m.cosh(self.argument(x))
    
    def __str__(self):
        return f"cosh({self.argument})"

class Tanh(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument, lambda arg: Polynomial(Cosh(arg), -2))
    
    def __call__(self, x: float) -> float:
        return m.tanh(self.argument(x))
    
    def __str__(self):
        return f"tanh({self.argument})"
