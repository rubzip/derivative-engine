import re
from src.expressions import (
    Expression,
    Constant,
    Variable,
    Sum,
    Subtraction,
    Product,
    Division,
    Power,
    Negation,
    Sin,
    Cos,
    Tan,
    Sinh,
    Cosh,
    Tanh,
    Exponential,
    Logarithm,
)
from .tokenizer import tokenize

FUN_MAP = {
    "sin": Sin,
    "cos": Cos,
    "tan": Tan,
    "sinh": Sinh,
    "cosh": Cosh,
    "tanh": Tanh,
    "exp": Exponential,
    "ln": Logarithm,
    "log": Logarithm,
}


class Parser:
    """Abstract Syntax Tree Implementation"""

    def __init__(self, tokens: list[str]):
        if len(tokens) == 0:
            raise ValueError("Expected ...")
        self.tokens = tokens
        self.fun_map = FUN_MAP
        self.pos = 0
        self.len = len(tokens)

    """
    Priority order:
     1. (parse_base): Variables('x'), Constants, Single Functions (self.fun_map), Parenthesys, and Negation
     2. (parse_factor): Power
     3. (parse_mult_div): Multiplication (and division)
     4. (parse_expr): Adition (and subtractions)
    """

    def _is_int(self, token: str) -> bool:
        return re.match(r"^\-?\d+$", token) is not None

    def _is_float(self, token: str) -> bool:
        return re.match(r"^\-?\d+\.\d*|\-?\d*\.\d+$", token) is not None

    def _is_text(self, token: str) -> bool:
        return re.match(r"[a-zA-Z]+", token) is not None

    def get_function(self, token: str) -> type[Expression] | None:
        """Takes a token and returns a Expression (or None)"""
        return self.fun_map.get(token, None)

    def peek(self) -> str | None:
        """Checks the current token (but doesnt update status)"""
        return self.tokens[self.pos] if self.pos < self.len else None

    def consume(self, expected: str=None) -> str | None:
        """Returns the current token (and updates status)"""
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of input")
        if expected and token != expected:
            raise ValueError(f"Expected: {expected}, got: {token}")
        self.pos += 1
        return token

    def parse_base(self) -> Expression:
        """Parse the deepest-level elements: constants, variables, functions, negation, parentheses."""
        token = self.consume()

        if token is None:
            raise ValueError("Unexpected end of input while parsing base.")

        # Negation
        if token == "-":
            return Negation(self.parse_factor())

        # Parentheses
        if token == "(":
            expr = self.parse_expr()
            self.consume(")")
            return expr

        # Number: integer or float
        if self._is_int(token):
            return Constant(int(token))

        if self._is_float(token):
            return Constant(float(token))

        # Variable
        if token == "x":
            return Variable()

        # Function call
        func_class = self.get_function(token)
        if func_class:
            self.consume("(")  # expect '('
            arg = self.parse_expr()
            self.consume(")")  # expect ')'
            return func_class(arg)

        raise ValueError(f"Unknown token: {token}")

    def parse_factor(self) -> Expression:
        """When we are parsing exponential function we should take in count that the order is right to left.
        So iteratively we are going to parse_factor.
        (Factor is optional)
        E.g: a^b^c^d = a^(b^(c^d))
        """
        base = self.parse_base()
        if self.peek() == "^":
            self.consume()
            factor = self.parse_factor()
            return Power(base, factor)
        return base

    def parse_mult_div(self) -> Expression:
        expr = self.parse_factor()
        while self.peek() in {"*", "/"}:
            operator = self.consume()
            right = self.parse_factor()
            expr_class = Product if operator == "*" else Division
            expr = expr_class(expr, right)
        return expr

    def parse_expr(self) -> Expression:
        expr = self.parse_mult_div()
        while self.peek() in {"+", "-"}:
            operator = self.consume()
            right = self.parse_mult_div()
            expr_class = Sum if operator == "+" else Subtraction
            expr = expr_class(expr, right)
        return expr

    def parse(self) -> Expression:
        self.pos = 0
        expr = self.parse_expr()
        if self.peek() is None:
            return expr
        raise ValueError(
            f"Parsing error. Parsed function: {''.join(self.tokens[:self.pos])}..."
        )


def parse(expr: str) -> Expression:
    tokens = tokenize(expr=expr)
    parser = Parser(tokens=tokens)
    return parser.parse()
