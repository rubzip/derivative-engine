from .basic import Expression, Constant, Product


class Polynomial(Expression):
    def __init__(self, argument: Expression, degree: float):
        def polynomial_derivative(arg: Expression) -> Expression:
            return Product(Constant(degree), Polynomial(arg, degree - 1))

        super().__init__(argument=argument, derivative_class=polynomial_derivative)
        self.degree = degree

    def simplify(self):
        if self.degree == 0:
            return Constant(1)
        if self.degree == 1:
            return self.argument
        arg = self.argument.simplify()
        if isinstance(arg, Constant):
            return Constant(arg.value**self.degree)
        return Polynomial(arg, self.degree)

    def __call__(self, x: float) -> float:
        return self.argument(x) ** self.degree

    def __str__(self):
        return f"({self.argument} ^ {self.degree})"
