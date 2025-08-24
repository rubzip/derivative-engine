from src.parser import parse


def main(n_tries: int = 10):
    while True:
        expr_str = input("function to derivate: ")
        if 'exit()' in expr_str:
            break

        try:
            expr = parse(expr_str)
            derivative = expr.derivative()
            for _ in range(n_tries):
                derivative = derivative.simplify()
            print(derivative)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main(10)
