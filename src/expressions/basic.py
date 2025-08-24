from abc import ABC, abstractmethod


class Expression(ABC):
    def __init__(self, argument: "Expression" = None, derivative_class=None):
        self.argument = argument
        self.derivative_class = derivative_class

    def derivative(self) -> "Expression":
        """Chain rule"""
        return Product(self.argument.derivative(), self.derivative_class(self.argument))

    def simplify(self) -> "Expression":
        """Method for simplifying expresion, should be overwritten in some expressions"""
        # If argument is None there is no possible simplification
        if self.argument is None:
            return self
        # Else we are instanciating the same class but with argument simplified
        return self.__class__(self.argument.simplify())

    def equals(self, value: float):
        if not isinstance(self, Constant):
            return False
        return self.value == value

    def __eq__(self, other: "Expression") -> bool:
        if type(self) != type(other):
            return False

        if isinstance(self, Conjunction):
            return (self.left == other.left) and (self.right == other.right)

        if isinstance(self, Constant):
            return self.value == other.value

        if isinstance(self, Variable):
            return True

        if self.argument is not None:
            return self.argument == other.argument

        return False

    @abstractmethod
    def __call__(self, x: float) -> float: ...


class Constant(Expression):
    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def derivative(self) -> "Constant":
        return Constant(0)

    def __call__(self, x: float) -> float:
        return self.value

    def __str__(self):
        return str(self.value)


class Variable(Expression):
    def __init__(self):
        super().__init__()

    def derivative(self) -> Constant:
        return Constant(1)

    def __call__(self, x: float) -> float:
        return x

    def __str__(self):
        return "x"


class Negation(Expression):
    def __init__(self, argument: Expression):
        super().__init__(argument)

    def derivative(self) -> "Negation":
        return Negation(self.argument.derivative()).simplify()

    def simplify(self):
        arg = self.argument.simplify()
        if isinstance(arg, Negation):
            return arg.argument
        if isinstance(arg, Constant):
            return Constant(-arg.value)
        if isinstance(arg, Sum):
            return Sum(Negation(arg.left), Negation(arg.right))
        if isinstance(arg, Subtraction):
            return Subtraction(arg.right, arg.left)
        return Negation(arg)

    def __call__(self, x: float) -> float:
        return -(self.argument(x))

    def __str__(self):
        return f"-({self.argument})"


class Conjunction(Expression):
    def __init__(self, left: Expression, right: Expression):
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
        left = self.left.simplify()
        right = self.right.simplify()

        if left == Negation(right):
            return Constant(0)
        if isinstance(left, Constant) and isinstance(right, Constant):
            return Constant(left.value + right.value)
        if isinstance(left, Constant) and left.value == 0:
            return right
        if isinstance(right, Constant) and right.value == 0:
            return left
        return Sum(left, right)

    def __call__(self, x: float) -> float:
        return self.left(x) + self.right(x)

    def __str__(self):
        return f"{self.left} + {self.right}"


class Subtraction(Conjunction):
    def __init__(self, left, right):
        super().__init__(left, right)

    def derivative(self) -> "Subtraction":
        return Subtraction(left=self.left.derivative(), right=self.right.derivative())

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if left == right:
            return Constant(0)
        if isinstance(left, Constant) and isinstance(right, Constant):
            return Constant(left.value - right.value)
        if isinstance(left, Constant) and left.value == 0:
            return Negation(right)
        if isinstance(right, Constant) and right.value == 0:
            return left
        return Subtraction(left, right)

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
            Product(left=self.left, right=self.right.derivative()),
        )

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Constant) and isinstance(right, Constant):
            return Constant(left.value * right.value)
        if isinstance(left, Constant) and left.value == 0:
            return Constant(0)
        if isinstance(right, Constant) and right.value == 0:
            return Constant(0)
        if isinstance(left, Constant) and left.value == 1:
            return right
        if isinstance(right, Constant) and right.value == 1:
            return left
        if isinstance(left, Constant) and left.value == -1:
            return Negation(right)
        if isinstance(right, Constant) and right.value == -1:
            return Negation(left)
        return Product(left, right)

    def __call__(self, x: float) -> float:
        return self.left(x) * self.right(x)

    def __str__(self):
        return f"{self.left} * {self.right}"


class Division(Conjunction):
    def __init__(self, left, right):
        if isinstance(right, Constant) and right.value == 0:
            raise ZeroDivisionError(f"Zero division error: {left} / {right}")

        super().__init__(left, right)

    def derivative(self) -> "Division":
        return Division(
            Subtraction(
                Product(self.left.derivative(), self.right),
                Product(self.left, self.right.derivative()),
            ),
            Product(self.right, self.right),
        )

    def simplify(self) -> Expression:
        left = self.left.simplify()
        right = self.right.simplify()

        if left == right:
            return Constant(1)
        if isinstance(left, Constant) and isinstance(right, Constant):
            return Constant(left.value / right.value)
        if isinstance(left, Constant) and left.value == 0:
            return Constant(0)
        if isinstance(right, Constant) and right.value == 1:
            return left
        return Division(left, right)

    def __call__(self, x: float) -> float:
        return self.left(x) / self.right(x)

    def __str__(self):
        return f"{self.left} / {self.right}"
