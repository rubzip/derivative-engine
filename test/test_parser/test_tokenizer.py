import pytest
from src.parser.tokenizer import tokenize


@pytest.mark.parametrize("expr, expected", [
    ("   2   + 3", ["2", "+", "3"]),
    (" 2 * x ", ["2", "*", "x"]),
    (" ( x + 1   ) ", ["(", "x", "+", "1", ")"]),
    ("  sin ( x )  ", ["sin", "(", "x", ")"]),
    ("   cos   ( 2 * x   )   ", ["cos", "(", "2", "*", "x", ")"]),
    ("    tan   (   x   ^   2   )  ", ["tan", "(", "x", "^", "2", ")"]),
    ("sinh(x) +     cosh   (x)   ", ["sinh", "(", "x", ")", "+", "cosh", "(", "x", ")"]),
    ("exp(x) / 2", ["exp", "(", "x", ")", "/", "2"]),
    ("   ln   (  10   )", ["ln", "(", "10", ")"]),
    ("3.14*x", ["3.14", "*", "x"]),
    ("-   (    x    -   1    )   ", ["-", "(", "x", "-", "1", ")"]),
])

def test_tokenize(expr: str, expected: list):
    assert tokenize(expr) == expected
