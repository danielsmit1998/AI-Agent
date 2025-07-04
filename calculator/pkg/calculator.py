class Calculator:
    def evaluate(self, expression):
        if not expression:
            return None
        try:
            return eval(expression)
        except Exception:
            raise ValueError("Invalid expression")