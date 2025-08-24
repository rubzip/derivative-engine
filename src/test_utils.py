from src.expressions.basic import Expresion

def evaluate_derivative(expresion: Expresion, expected_derivative: callable, values: list[float], tol: float = 1e-6):
    derivative_exp = expresion.derivative().simplify()
    for x in values:
        actual = derivative_exp(x)
        expected = expected_derivative(x)
        if abs(actual - expected) > tol:
            raise ValueError(f"Failed on x={x}: Computed derivative={actual}, Expected derivative={expected}")
