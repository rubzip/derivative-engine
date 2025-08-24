import math as m

from .basic import Expresion, Constant
from .conjunction import Division, Product, Negation
from .power import Power

class Cosh(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument)
    
    def derivative(self):
        return Product(
            Sinh(self.argument), 
            self.argument.derivative()
        )
    
    def __call__(self, x: float) -> float:
        return m.cosh(self.argument(x))
    
    def __str__(self):
        return f"cosh({self.argument})"

class Sinh(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument)
    
    def derivative(self):
        return Product(
            Cosh(self.argument),
            self.argument.derivative()
        )

    def __call__(self, x: float) -> float:
        return m.sinh(self.argument(x))

    def __str__(self):
        return f"sinh({self.argument})"

class Tanh(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument)
    
    def derivative(self):
        return Division(
            self.argument.derivative(),
            Power(
                Cosh(self.argument), Constant(2)
            )
        )
    
    def __call__(self, x: float) -> float:
        return m.tanh(self.argument(x))
    
    def __str__(self):
        return f"tanh({self.argument})"
