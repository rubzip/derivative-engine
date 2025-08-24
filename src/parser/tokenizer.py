import re

TOKEN_REGEX = r"\d+\.\d*|\.\d+|\d+|[a-zA-Z]+|[()+\-*/^]"

def tokenize(expr: str) -> list:
    return re.findall(TOKEN_REGEX, expr.replace(" ", "").lower())
