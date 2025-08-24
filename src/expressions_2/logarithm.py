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

    def __call__(self, x: float) -> float:
        return m.log(self.argument(x))
    
    def __str__(self):
        return f"ln({self.argument})"
