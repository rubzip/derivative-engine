import math as m
from .basic import Expresion, Constant
from .conjunction import Division, Product, Negation
from .power import Power

class Sin(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument)
    
    def derivative(self):
        return Product(Cos(self.argument), self.argument.derivative())
    
    def __call__(self, x: float) -> float:
        return m.sin(self.argument(x))

    def __str__(self):
        return f"sin({self.argument})"

class Cos(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument)
    
    def derivative(self):
        return Negation(
            Product(Sin(self.argument), self.argument.derivative())
        )
    
    def __call__(self, x: float) -> float:
        return m.cos(self.argument(x))
    
    def __str__(self):
        return f"cos({self.argument})"

class Tan(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument)
    
    def derivative(self):
        return Division(
            self.argument.derivative(), 
            Power(Cos(self.argument), Constant(2))
        )
    
    def __call__(self, x: float) -> float:
        return m.tan(self.argument(x))
    
    def __str__(self):
        return f"tan({self.argument})"
