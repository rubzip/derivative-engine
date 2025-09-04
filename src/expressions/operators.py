from abc import ABC
from collections import defaultdict

from .base import Expression, Constant


class Operator(Expression, ABC):
    """Base class for mathematical (n-ary) operators."""
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

    def copy(self) -> "Operator":
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

    def __str__(self) -> str:
        return f" {self.symbol} ".join(self._add_parentheses(a) for a in self.arguments)

    def __hash__(self):
        return hash((self.symbol, tuple(self.arguments)))

    def _simplify_args(self, args: list[Expression]) -> list[Expression]:
        if self.absorbent and any(arg == self.absorbent for arg in args):
            return [self.absorbent]
        return [arg.simplify() for arg in args if arg != self.identity]

    def _sort_args(self):
        self.arguments.sort(key=lambda a: (a.precedence, str(a)))


class Sum(Operator):
    """Addition operator."""
    identity = Constant(0)
    absorbent = None
    precedence = 4
    symbol = "+"

    def derivate(self) -> "Sum":
        return Sum(*(arg.derivate() for arg in self.arguments))

    def simplify(self) -> Expression:
        flat_args = []
        constant_sum = 0

        args = self._simplify_args(self.arguments)
        for arg in args:
            if isinstance(arg, Sum):
                flat_args.extend(arg.arguments)
            elif isinstance(arg, Constant):
                constant_sum += arg.value
            else:
                flat_args.append(arg)

        if constant_sum != 0:
            flat_args.append(Constant(constant_sum))

        if not flat_args:
            return Constant(0)

        if len(flat_args) == 1:
            return flat_args[0]

        result = Sum(*flat_args)
        result._sort_args()
        return result

    def group(self) -> Expression:
        groups = defaultdict(lambda: Constant(0))

        for arg in self.arguments:
            if isinstance(arg, Product):
                non_constants = [
                    a for a in arg.arguments if not isinstance(a, Constant)
                ]
                key = tuple(non_constants)
                coeff = 1
                for a in arg.arguments:
                    if isinstance(a, Constant):
                        coeff *= a.value
                groups[key] = (
                    Constant(groups[key].value + coeff)
                    if key in groups
                    else Constant(coeff)
                )
            elif isinstance(arg, Constant):
                groups[()] = (
                    Constant(groups[()].value + arg.value) if () in groups else arg
                )
            else:
                groups[(arg,)] = Constant(1) + groups.get((arg,), Constant(0))

        new_terms = []
        for key, coeff in groups.items():
            if key:
                term = Product(coeff, *key).simplify()
            else:
                term = coeff
            new_terms.append(term)

        return Sum(*new_terms).simplify()

    def __call__(self, x: float) -> float:
        return sum(arg(x) for arg in self.arguments)


class Product(Operator):
    """Multiplication operator."""
    identity = Constant(1)
    absorbent = Constant(0)
    precedence = 2
    symbol = "*"

    def derivate(self) -> Expression:
        terms = []
        for i, _ in enumerate(self.arguments):
            term = [a if j != i else a.derivate() for j, a in enumerate(self.arguments)]
            terms.append(Product(*term))
        return Sum(*terms).simplify()

    def simplify(self) -> Expression:
        flat_args = []
        constant_prod = 1

        args = self._simplify_args(self.arguments)
        for arg in args:
            if isinstance(arg, Product):
                flat_args.extend(arg.arguments)
            elif isinstance(arg, Constant):
                constant_prod *= arg.value
            else:
                flat_args.append(arg)

        if constant_prod == 0:
            return Constant(0)

        if not flat_args:
            return Constant(1)

        if constant_prod != 1:
            flat_args.append(Constant(constant_prod))

        if len(flat_args) == 1:
            return flat_args[0]

        prod = Product(*flat_args)
        prod._sort_args()
        return prod

    def __call__(self, x: float) -> float:
        result = 1.
        for arg in self.arguments:
            result *= arg(x)
        return result
    
    @staticmethod
    def as_factors(*arguments: Expression) -> list[Expression]:
        from .exponential import Power
        factors = []
        for arg in arguments:
            if isinstance(arg, Power):
                factors.append((arg.base, arg.factor))
            else:
                factors.append(arg, Constant(1))
        return factors
