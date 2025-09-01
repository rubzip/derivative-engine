from abc import ABC, abstractmethod
import math as m

# This is a refactoring
# For making simpler .simplify() we are going to refactor and reduce the size of the library.
# Expression: Interface, every class inhereights from this
#   Constant(Expression): 
#   Variable(Expression): 
#   Fuction(Expression): 
#   Operator(Expression): 
#       Sum(Operator): 
#       Mult(Operator): 
#       Power(Operator): 

class Expression(ABC):
    def __init__(self, quantity: float = 1., precedence: int = None):
        self.quantity = quantity
        self.precedence = int

    @abstractmethod
    def simplify(self) -> "Expression": ...

    @abstractmethod
    def derivate(self) -> "Expression": ...

    @abstractmethod
    def __call__(self, x: float) -> float: ...

    @abstractmethod
    def __str__(self): ...

    @abstractmethod
    def __hash__(self): ...

    def _simplify_null(self) -> "Expression":
        if self.quantity == 0:
            return Constant(0)
        return self
    
    def _add_parentheses(self, child: "Expression") -> str:
        if child.precedence > self.precedence:
            return f"({child})"
        return str(child)
    
    def __mult__(self, other: float):
        if isinstance(other, [float, int]):
            self.quantity *= other
            return self
        raise NotImplementedError("non implemented error multiplication betweeen")


class Constant(Expression):
    def __init__(self, quantity: float = 1):
        super().__init__(quantity=quantity, precedence=0)
    
    def derivate(self) -> "Constant":
        return Constant(0)
    
    def simplify(self) -> "Constant":
        return self
    
    def __eq__(self, other: Expression) -> bool:
        return isinstance(other, Constant) and (other.quantity == self.quantity)
    
    def __call__(self, x):
        return self.quantity

    def __str__(self):
        return str(self.quantity)

class Variable(Expression):
    def __init__(self, quantity: float = 1.):
        super().__init__(quantity, precedence=0)
    
    def derivate(self) -> Constant:
        return Constant(1)
    
    def simplify(self) -> "Variable":
        return self
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self.quantity == other.quantity 

    def __call__(self, x):
        return x
    
    def __str__(self):
        return f"{self.quantity}x"

class Function(Expression):
    def __init__(self, quantity, argument: Expression, derivative_fn: callable, is_inverse: callable, symbol: str, _is_linear: bool = False):
        super().__init__(quantity, precedence=4)
        self.derivate_fn = derivative_fn
        self.argument = argument
        self.is_inverse = is_inverse
        self.symbol = symbol
        self._is_linear = _is_linear
    
    def simplify(self):
        arg = self.argument.simplify()
        if self.is_inverse(arg):
            return arg.argument
        return class(arg)

    def derivate(self):
        arg = self.argument
        return Product(
            self.derivate_fn(arg),
            arg.derivate()
        )
    
    def __str__(self):
        arg = self._add_parentheses(self.argument)
        return f"{self.quantity}{self.symbol}{arg}"

class Operator(Expression):
    def __init__(self, *arguments: Expression, indetity: Expression, nullizer: Expression, quantity: float = 1., precedence: int = 3):
        super().__init__(quantity, precedence)
        self.arguments = arguments
        self.identity = indetity
        self.nullizer = nullizer
    
    def __new__(cls, *arguments, quantity: float):
        if len(arguments) == 0:
            raise ValueError("Invalid void ...")
        if len(arguments) == 1:
            return arguments[0] # Take in count quantity
        if any(arg == cls.nullizer for arg in arguments):
            return Constant(0.)
        filtered_args = [arg for arg in arguments if arg != cls.identity]
        return cls(*filtered_args, quantity)
    
    def sort(): ...


