from .core import Expression, Constant, Product, Power

class Division:
    def __new__(cls, dividend: Expression, divisor: Expression) -> Expression:
        if divisor == Constant(0):
            raise ZeroDivisionError("You can't divide by zero")
        if divisor == Constant(1):
            return dividend
        if dividend == Constant(0):
            return Constant(0)
        
        return Product(dividend, Power(divisor, Constant(-1)))
