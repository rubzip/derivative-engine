from abc import abstractmethod
from .basic import Expresion, Constant

class Negation(Expresion):
    def __init__(self, argument: Expresion):
        super().__init__(argument)
    
    def derivative(self) -> "Negation":
        return Product(Constant(-1), self.argument.derivative())
    
    def simplify(self):
        arg = self.argument.simplify()
        if isinstance(arg, Negation):
            return arg.argument.simplify()
        if isinstance(arg, Constant):
            return Constant(-arg.value)
        return Negation(arg)
    
    def __call__(self, x: float) -> float:
        return -(self.argument(x))

    def __str__(self):
        return f"-({self.argument})"

class Conjunction(Expresion):
    def __init__(self, left: Expresion, right: Expresion):
        self.left = left
        self.right = right

    @abstractmethod
    def simplify(self):
        pass

class Sum(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def derivative(self) -> "Sum":
        return Sum(left=self.left.derivative(), right=self.right.derivative())
    
    def simplify(self):
        if isinstance(self.left, Constant) and isinstance(self.right, Constant):
            return Constant(self.left.value + self.right.value)
        if isinstance(self.left, Constant) and self.left.value == 0:
            return self.right.simplify()
        if isinstance(self.right, Constant) and self.right.value == 0:
            return self.left.simplify()
        return Sum(self.left.simplify(), self.right.simplify())
    
    def __call__(self, x: float) -> float:
        return self.left(x) + self.right(x)
    
    def __str__(self):
        return f"{self.left} + {self.right}"

class Substraction(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def derivative(self) -> "Substraction":
        return Substraction(left=self.left.derivative(), right=self.right.derivative())
    
    def simplify(self):
        if isinstance(self.left, Constant) and isinstance(self.right, Constant):
            return Constant(self.left.value - self.right.value)
        if isinstance(self.left, Constant) and self.left.value == 0:
            return Negation(self.right.simplify())
        if isinstance(self.right, Constant) and self.right.value == 0:
            return self.left.simplify()
        return Substraction(self.left.simplify(), self.right.simplify())
    
    def __call__(self, x: float) -> float:
        return self.left(x) - self.right(x)
    
    def __str__(self):
        return f"{self.left} - {self.right}"

class Product(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def derivative(self) -> Sum:
        return Sum(
            Product(left=self.left.derivative(), right=self.right),
            Product(left=self.left, right=self.right.derivative())
        )

    def simplify(self):
        if isinstance(self.left, Constant) and isinstance(self.right, Constant):
            return Constant(self.left.value * self.right.value)
        if isinstance(self.left, Constant) and self.left.value == 0:
            return Constant(0)
        if isinstance(self.right, Constant) and self.right.value == 0:
            return Constant(0)
        if isinstance(self.left, Constant) and self.left.value == 1:
            return self.right.simplify()
        if isinstance(self.right, Constant) and self.right.value == 1:
            return self.left.simplify()
        return Product(self.left.simplify(), self.right.simplify())
    
    def __call__(self, x: float) -> float:
        return self.left(x) * self.right(x)

    def __str__(self):
        return f"{self.left} * {self.right}"

class Division(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def derivative(self) -> "Division":
        return Division(
            Substraction(
                Product(self.left.derivative(), self.right),
                Product(self.left, self.right.derivative())
            ),
            Product(self.right, self.right)
        )
    
    def simplify(self):
        if isinstance(self.left, Constant) and isinstance(self.right, Constant):
            return Constant(self.left.value / self.right.value)
        if isinstance(self.left, Constant) and self.left.value == 0:
            return Constant(0)
        if isinstance(self.right, Constant) and self.right.value == 1:  # fix aquí
            return self.left.simplify()
        return Division(self.left.simplify(), self.right.simplify())
    
    def __call__(self, x: float) -> float:
        return self.left(x) / self.right(x)
    
    def __str__(self):
        return f"{self.left} / {self.right}"
