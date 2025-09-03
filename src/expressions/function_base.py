from abc import ABC
from .base import Expression


class Function(Expression, ABC):
    symbol: str = ""
    _is_linear: bool = False

    def __init__(self, argument: Expression):
        super().__init__(precedence=4)
        self.argument = argument

    @staticmethod
    def derivate_fn(argument: Expression) -> Expression:
        """Returns the derivative of the function with respect to its argument.
        This method should be overridden by subclasses to provide the specific derivative logic."""
        raise NotImplementedError()
    
    @staticmethod
    def is_inverse(argument: Expression) -> bool:
        """Checks if the given argument is the inverse of this function.
        This method should be overridden by subclasses if they have a specific inverse function."""
        return False

    def derivate(self) -> Expression:
        from .operators import Product
        arg = self.argument
        return Product(self.derivate_fn(arg), arg.derivate())

    def simplify(self) -> Expression:
        arg = self.argument.simplify()
        if isinstance(arg, Function) and self.is_inverse is not None:
            if self.is_inverse(arg):
                return arg.argument
        return self.__class__(argument=arg)

    def copy(self) -> "Function":
        return self.__class__(self.argument.copy())

    def __eq__(self, other):
        cls = self.__class__
        return isinstance(other, cls) and self.argument == other.argument

    def __str__(self):
        arg = self._add_parentheses(self.argument)
        return f"{self.symbol}{arg}"

    def __hash__(self):
        return hash((self.symbol, self.argument))
