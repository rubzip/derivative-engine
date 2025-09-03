from abc import ABC, abstractmethod
import math as m


class Expression(ABC):
    def __init__(self, precedence: int = None):
        self.precedence = precedence

    @abstractmethod
    def derivate(self) -> "Expression": ...

    @abstractmethod
    def simplify(self) -> "Expression": ...

    @abstractmethod
    def copy(self) -> "Expression": ...

    @abstractmethod
    def __eq__(self, other: "Expression") -> bool: ...

    @abstractmethod
    def __call__(self, x: float) -> float: ...

    @abstractmethod
    def __str__(self): ...

    @abstractmethod
    def __hash__(self): ...

    def _add_parentheses(self, child: "Expression") -> str:
        if child.precedence > self.precedence:
            return f"({child})"
        return str(child)


class Constant(Expression):
    def __init__(self, value: float):
        super().__init__(precedence=0)
        self.value = value

    def derivate(self) -> "Constant":
        return Constant(0)

    def simplify(self) -> "Constant":
        return self

    def copy(self):
        return Constant(self.value)

    def __eq__(self, other: Expression) -> bool:
        return isinstance(other, Constant) and (other.value == self.value)

    def __call__(self, x):
        return self.value

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)


class Variable(Expression):
    def __init__(self):
        super().__init__(precedence=0)

    def derivate(self) -> Constant:
        return Constant(1)

    def simplify(self) -> "Variable":
        return self

    def copy(self):
        return Variable()

    def __eq__(self, other):
        return isinstance(other, Variable)

    def __call__(self, x):
        return x

    def __str__(self):
        return "x"

    def __hash__(self):
        return hash("x")
