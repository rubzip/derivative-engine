from abc import ABC, abstractmethod
import math as m
from collections import defaultdict

# This is a refactoring
# For making simpler .simplify() we are going to refactor and reduce the size of the library.
# Expression: Interface, every class inhereights from this
#   Constant(Expression): 
#   Variable(Expression): 
#   Fuction(Expression): 
#   Operator(Expression): 
#       Sum(Operator): 
#       Mult(Operator): 
#   Power(Expression): 

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

class Function(Expression):
    derivate_fn: callable = None
    is_inverse: callable = None
    symbol: str = ""
    _is_linear: bool = False

    def __init__(self, argument: Expression):
        super().__init__(precedence=4)
        self.argument = argument
    
    def simplify(self):
        arg = self.argument.simplify()
        if isinstance(arg, Function) and self.is_inverse is not None:
            if self.is_inverse(arg):
                return arg.argument
        return self.__class__(argument=arg)

    def derivate(self):
        arg = self.argument
        return Product(
            self.derivate_fn(arg),
            arg.derivate()
        )
    
    def copy(self):
        return self.__class__(self.argument.copy())
    
    def __str__(self):
        arg = self._add_parentheses(self.argument)
        return f"{self.symbol}{arg}"
    
    def __eq__(self, other):
        cls_ = type(self)
        return isinstance(other, cls_) and self.argument == other.argument

    def __hash__(self):
        return hash((self.symbol, self.argument))

class Log(Function):
    def log_derivate(argument: Expression) -> Expression:
        return Power(argument, Constant(-1))
    
    derivate_fn = log_derivate
    is_inverse = lambda arg: isinstance(arg, Exp)
    symbol = "log"
    _is_linear = False

    def __init__(self, argument: Expression):
        super().__init__(argument)
    
    def __call__(self, x):
        return m.log(self.argument(x))

class Exp(Function):
    derivate_fn = lambda arg: Exp(arg)
    is_inverse = lambda arg: isinstance(arg, Log)
    symbol = "exp"
    _is_linear = False

    def __init__(self, argument: Expression):
        super().__init__(argument)

    def __call__(self, x):
        return m.exp(self.argument(x))

class Operator(Expression):
    identity: Expression = None
    absorbant: Expression = None
    precedence: int = 3
    symbol: str = ''

    def __init__(self, *arguments: Expression):
        super().__init__(precedence=self.precedence)
        if not arguments:
            raise ValueError("Operator needs at least one argument")
        self.arguments = self._simplify_args(arguments)
        self._sort_args()

    def _simplify_args(self, args: list[Expression]) -> list[Expression]:
        if self.absorbant and any(arg == self.absorbant for arg in args):
            return [self.absorbant]
        return [arg.simplify() for arg in args if arg != self.identity]
    
    def copy(self):
        return self.__class__(*self.arguments)

    def _sort_args(self):
        self.arguments.sort(key=lambda a: (a.precedence, str(a)))

    def __str__(self):
        return f" {self.symbol} ".join(self._add_parentheses(a) for a in self.arguments)

    def __hash__(self):
        return hash((self.symbol, tuple(self.arguments)))
    
    def __eq__(self, other):
        self._sort_args()
        

class Sum(Operator):
    identity = Constant(0)
    absorbant = None
    precedence = 1
    symbol = "+"

    def __init__(self, *arguments: Expression):
        super().__init__(*arguments)

    def simplify(self) -> Expression:
        flat_args = []
        constant_sum = 0

        for arg in self.arguments:
            if isinstance(arg, Sum):
                flat_args.extend([a.simplify() for a in arg.arguments])
            elif isinstance(arg, Constant):
                constant_sum += arg.value
            else:
                flat_args.append(arg.simplify())

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
                non_constants = [a for a in arg.arguments if not isinstance(a, Constant)]
                key = tuple(non_constants)
                coeff = 1
                for a in arg.arguments:
                    if isinstance(a, Constant):
                        coeff *= a.value
                groups[key] = Constant(groups[key].value + coeff) if key in groups else Constant(coeff)
            elif isinstance(arg, Constant):
                groups[()] = Constant(groups[()].value + arg.value) if () in groups else arg
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

    def derivate(self) -> Expression:
        return Sum(*(arg.derivate() for arg in self.arguments))

class Product(Operator):
    identity = Constant(1)
    absorbent = Constant(0)
    precedence = 2
    symbol = "*"

    def __init__(self, *arguments: Expression):
        super().__init__(*arguments)

    def simplify(self) -> Expression:
        flat_args = []
        constant_prod = 1

        for arg in self.arguments:
            if isinstance(arg, Product):
                flat_args.extend([a.simplify() for a in arg.arguments])
            elif isinstance(arg, Constant):
                constant_prod *= arg.value
            else:
                flat_args.append(arg.simplify())

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
        result = 1
        for arg in self.arguments:
            result *= arg(x)
        return result

    def derivate(self) -> Expression:
        terms = []
        for i, _ in enumerate(self.arguments):
            deriv_args = [
                a if j != i else a.derivate()
                for j, a in enumerate(self.arguments)
            ]
            terms.append(Product(*deriv_args))
        return Sum(*terms).simplify()


class Power(Expression):
    def __init__(self, base: Expression, factor: Expression):
        super().__init__(precedence=3)
        self.base = base
        self.factor = factor

    def simplify(self):
        base = self.base.simplify()
        if base == Constant(0) or base == Constant(1):
            return base
        
        factor = self.factor.simplify()
        if factor == Constant(1):
            return base
        if factor == Constant(0):
            return Constant(1)
        
        if isinstance(base, Power):
            return Power(base.base, Product(base.factor, factor)).simplify()
        
        return Power(base, factor)

    def derivate(self):
        f, g = self.base, self.factor
        term1 = Product(self, Log(f), g.derivate())
        term2 = Product(self, g, f.derivate(), Power(f, Constant(-1)))
        return Sum(term1, term2).simplify()
    
    def __call__(self, x):
        return self.base(x) ** self.factor(x)
    
    def __str__(self):
        base_str = self._add_parentheses(self.base)
        factor_str = self._add_parentheses(self.factor)
        
        return f"{base_str}^{factor_str}" 

    def __eq__(self, other):
        return isinstance(other, Power) and self.base == other.base and self.factor == other.factor

    def __hash__(self):
        return hash(("^", self.base, self.factor))
