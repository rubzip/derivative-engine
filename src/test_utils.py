from src.expressions.basic import Expression

def evaluate_derivative(expresion: Expression, expected_derivative: callable, values: list[float], tol: float = 1e-6):
    derivative_exp = expresion.simplify().derivative().simplify()
    for x in values:
        actual = derivative_exp(x)
        expected = expected_derivative(x)
        if abs(actual - expected) > tol:
            raise ValueError(f"Failed on x={x}: Computed derivative={actual}, Expected derivative={expected}")
