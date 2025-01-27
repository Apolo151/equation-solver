import re
import math

class Parser:
    def __init__(self):
        # Define allowed characters and supported operations
        self.allowed_chars = r"x0-9+\-*/().^ log10sqrt"
        self.supported_ops = ["+", "-", "*", "/", "^", "log10", "sqrt"]
        self.safe_dict = {
            "math": math,
            "log10": math.log10,
            "sqrt": math.sqrt,
        }

    def parse(self, func_str):
        """Parse and validate a function string."""
        errors = []
        parsed_func = func_str.strip()

        # Remove whitespace
        parsed_func = parsed_func.replace(" ", "")

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
        unsupported_ops = re.findall(r"(log\(|ln\(|sin\(|cos\(|tan\()", parsed_func)
        if unsupported_ops:
            errors.append(f"Unsupported operations detected: {', '.join(set(unsupported_ops))}")
        
        if errors:
            return None, errors

        # Validate function syntax
        try:
            # Preprocess log10 and sqrt to use math functions
            parsed_test = re.sub(r"log10\(", "math.log10(", parsed_func)
            parsed_test = re.sub(r"sqrt\(", "math.sqrt(", parsed_test)
            # Test evaluation with x=1 (dummy check)
            x = 1
            eval(parsed_test, {"__builtins__": None}, {**self.safe_dict, "x": x})
            print("func", parsed_test)
        except Exception as e:
            errors.append(f"Invalid syntax: {str(e)}")
            print("func", parsed_test)


        # Return parsed function and errors
        return parsed_func, errors