from abc import ABC, abstractmethod

class Expresion(ABC):
    def __init__(self, argument: "Expresion" = None):
        self.argument = argument

    @abstractmethod
    def derivative(self) -> "Expresion": ...

    def simplify(self) -> "Expresion":
        if self.argument is None:
            return self
        return self.__class__(self.argument.simplify())

    @abstractmethod    
    def __call__(self, x: float) -> float: ...

class Constant(Expresion):
    def __init__(self, value: float):
        super().__init__()
        self.value = value
    
    def derivative(self) -> "Constant":
        return Constant(0)
    
    def __call__(self, x: float) -> float:
        return self.value
    
    def __str__(self):
        return str(self.value)

class Variable(Expresion):
    def __init__(self):
        super().__init__()

    def derivative(self) -> Constant:
        return Constant(1)
    
    def __call__(self, x: float) -> float:
        return x
    
    def __str__(self):
        return 'x'

