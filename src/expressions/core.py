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
    def __str__(self) -> str: ...

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


class Operator(Expression, ABC):
    identity: Expression = None
    absorbent: Expression = None
    precedence: int = 3
    symbol: str = ""

    def __init__(self, *arguments: Expression):
        super().__init__(precedence=self.precedence)
        if not arguments:
            raise ValueError("Operator needs at least one argument")
        self.arguments = self._simplify_args(arguments)
        self._sort_args()

    def copy(self):
        return self.__class__(*(arg.copy() for arg in self.arguments))

    def __eq__(self, other):
        cls = self.__class__
        if not isinstance(other, cls):
            return False
        if len(self.arguments) != len(other.arguments):
            return False
        self._sort_args()
        other._sort_args()
        return all(a == b for a, b in zip(self.arguments, other.arguments))

    def __str__(self):
        return f" {self.symbol} ".join(self._add_parentheses(a) for a in self.arguments)

    def __hash__(self):
        return hash((self.symbol, tuple(self.arguments)))

    def _simplify_args(self, args: list[Expression]) -> list[Expression]:
        if self.absorbent and any(arg == self.absorbent for arg in args):
            return [self.absorbent]
        return [arg.simplify() for arg in args if arg != self.identity]

    def _sort_args(self):
        self.arguments.sort(key=lambda a: (a.precedence, str(a)))
