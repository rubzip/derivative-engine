from .basic import Constant
from .conjunction import Conjunction, Sum, Product, Division
from .logarithm import Logarithm


class Power(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def derivative(self):
        if isinstance(self.right, Constant):
            return Product(
                Product(
                    self.right,
                    Power(self.left, Constant(self.right.value - 1))
                ),
                self.left.derivative()
            )
        return Product(
            Power(self.left, self.right),
            Sum(
                Product(self.right.derivative(), Logarithm(self.left)),
                Product(self.right, Division(self.left.derivative(), self.left))
            )
        )
    
    def simplify(self):
        if isinstance(self.left, Constant) and self.left.value == 1:
            return Constant(1)
        if isinstance(self.left, Constant) and self.left.value == 0:
            return Constant(0)
        if isinstance(self.right, Constant) and self.right.value == 0:
            return Constant(1)
        if isinstance(self.right, Constant) and self.right.value == 1:
            return self.left.simplify()
        return Power(self.left.simplify(), self.right.simplify())

    def __call__(self, x: float) -> float:
        return self.left(x) ** self.right(x)

    def __str__(self):
        return f"({self.left} ^ {self.right})"
