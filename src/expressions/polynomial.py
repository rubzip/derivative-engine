from .basic import Expresion, Constant
from .conjunction import Division, Product


class Polynomial(Expresion):
    def __init__(self, argument: Expresion, degree: float):
        super().__init__(argument=argument)
        self.degree = degree
    
    def derivative(self) -> "Product":
        if self.degree == 0:
            return Constant(0)
        return Product(
            Product(
                Constant(self.degree),
                self.argument.derivative()
                ),
            Polynomial(self.argument, self.degree-1)
        )
    
    def simplify(self):
        if self.degree == 0:
            return Constant(1)
        if self.degree == 1:
            return self.argument
        return Polynomial(self.argument.simplify(), self.degree)
    
    def __call__(self, x: float) -> float:
        return self.argument(x) ** self.degree
    
    def __str__(self):
        return f"({self.argument} ^ {self.degree})"
