from .basic import Expresion, Constant, Product


class Polynomial(Expresion):
    def __init__(self, argument: Expresion, degree: float):
        def polynomial_derivative(arg: Expresion) -> Expresion:
            return Product(Constant(degree), Polynomial(arg, degree-1))
        super().__init__(argument=argument, derivative_class=polynomial_derivative)
        self.degree = degree
    
    def simplify(self):
        if self.degree == 0:
            return Constant(1)
        if self.degree == 1:
            return self.argument
        arg = self.argument.simplify()
        if isinstance(arg, Constant):
            return Constant(arg.value ** self.degree)
        return Polynomial(arg, self.degree)
    
    def __call__(self, x: float) -> float:
        return self.argument(x) ** self.degree
    
    def __str__(self):
        return f"({self.argument} ^ {self.degree})"
