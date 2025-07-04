# main.py

import sys
from pkg.calculator import Calculator


def main():
    calculator = Calculator()
    expression = "3+7*2"
    try:
        result = calculator.evaluate(expression)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()