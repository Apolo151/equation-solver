import re
import math

class Parser:
    def __init__(self):
        self.allowed_chars = r"x0-9+\-*/().^ log10sqrt "
        self.supported_ops = ["+", "-", "*", "/", "^", "log10", "sqrt"]

    def parse(self, func_str):
        """Parse and validate a function string."""
        errors = []
        parsed_func = func_str.strip()

        # Check for empty input
        if not parsed_func:
            errors.append("Function cannot be empty.")
            return None, errors

        # Replace shorthand operators
        parsed_func = parsed_func.replace("^", "**")

        # Validate allowed characters
        if not re.match(f"^[{self.allowed_chars}]+$", parsed_func):
            errors.append("Invalid characters detected.")

        # Validate parentheses balance
        if parsed_func.count("(") != parsed_func.count(")"):
            errors.append("Mismatched parentheses.")

        # Detect unsupported operations
        if "log(" in parsed_func or "ln(" in parsed_func:
            errors.append("Only log10() is supported.")
        
        # Validate function syntax (example)
        try:
            # Test evaluation with x=1 (dummy check)
            x = 1
            y = eval(parsed_func, {"math": math}, {"x": x})
            print("func: ", parsed_func)
            print("res: ", y)
        except Exception as e:
            errors.append(f"Invalid syntax: {str(e)}")

        return parsed_func, errors