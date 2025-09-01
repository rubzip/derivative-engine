from .core import Expression, Constant, Sum, Product

class Power(Expression):
    def __init__(self, base: Expression, factor: Expression, quantity: int = 1.):
        super().__init__(quantity, precedence=None)
        self.base = base
        self.factor = factor
    
    def simplify(self):
        base = self.base.simplify()
        if base == Constant(1): # q * 1 ^ f = q
            return Constant(self.quantity)
        if base == Constant(0): # q * 0 ^ f = 0
            return Constant(0)
        
        factor = self.factor.simplify()
        if factor == Constant(0): # q * x ^ 0 = q
            return Constant(self.quantity)
        if factor == Constant(1): 
            return base # add quantity
        
        return Power(base, factor, self.quantity)
    
    def derivate(self):
        return Sum(
            Product(
                Power(self.base, self.factor), self.factor.derivative(), Log(self.base)
                ),
            Product(
                Power(self.base, self.factor), self.factor, self.base.derivative(), Power(self.factor, Constant(-1))
                ),
            quantity=self.quantity
        )
    
    def simplify(self):
        return 
    
    def __call__(self, x: float) -> float:
        return self.quantity * self.base(x) ** self.factor(x)

class Log(Function):
    def __init__(self, argument: Expression, quantity: float = 1.):
        def derivative_fn(self: "Log") -> Expression:
            return Power(self.argument, Constant(-1), self.quantity)
        
        super().__init__(quantity, argument, derivative_fn, is_inverse = lambda x: isinstance(x, Exp), symbol='log', _is_linear=False)

    def __call__(self, x):
        return m.log(x)

class Exp(Function):
    def __init__(self, argument: Expression, quantity: float):
        def derivative_fn(self: "Exp") -> Exp:
            return self
        super().__init__(quantity, argument, derivative_fn=derivative_fn, is_inverse = lambda arg: isinstance(arg, Log), symbol="exp", _is_linear=False)
    
    def __call__(self, x):
        return m.exp(x)