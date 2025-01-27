import re
from typing import List, Tuple

class Parser:
    def __init__(self):
        self.tokens = []  # Tokens from the input expression
        self.errors = []  # List of errors encountered during parsing
        self.current_token = None
        self.pos = 0
    
    def basic_validation(self, expression: str) -> bool:
        """Performs basic validation on the input expression."""
        if not expression:
            self.errors.append("Empty expression.")
            return False
        if not re.match(r"^[0-9a-zA-Z\s\.\*\-\+\^\/\(\)]+$", expression):
            # special characters not allowed
            self.errors.append("Invalid characters in expression.")
            return False
        return True

    def tokenize(self, expression: str) -> List[str]:
        """Tokenizes the input expression."""
        token_pattern = re.compile(r"\s*(\d+\.\d+|\d+|\w+|\*\*|\^|[()+\-*/])\s*")
        tokens = token_pattern.findall(expression)
        return tokens

    def parse(self, expression: str) -> Tuple[str, List[str]]:
        """Parses the given mathematical expression."""
        expression = expression.replace(" ", "")
        self.errors = []
        # basic initial validation
        self.basic_validation(expression)
        if self.errors:
            return "", self.errors
        self.tokens = self.tokenize(expression)
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

        try:
            result = self.expression()
            if self.current_token is not None:
                self.errors.append("Unexpected token at the end.")
                return "", self.errors
            return result, self.errors
        except SyntaxError as e:
            self.errors.append(str(e))
            return "", self.errors

    def advance(self):
        """Advances to the next token."""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, expected_token: str):
        """Matches and consumes the current token if it matches the expected token."""
        if self.current_token == expected_token:
            self.advance()
        else:
            raise SyntaxError(f"Expected '{expected_token}' but got '{self.current_token}'.")

    def expression(self) -> str:
        """Parses an expression."""
        term_value = self.term()
        while self.current_token in {"+", "-"}:
            operator = self.current_token
            self.advance()
            right_term = self.term()
            term_value += operator + right_term
        return term_value

    def term(self) -> str:
        """Parses a term."""
        factor_value = self.factor()
        while self.current_token in {"*", "/"}:
            operator = self.current_token
            self.advance()
            right_factor = self.factor()
            factor_value += operator + right_factor
        return factor_value

    def factor(self) -> str:
        """Parses a factor."""
        base_value = self.base()
        while self.current_token == "^":
            self.advance()
            exponent = self.base()
            #base_value = f"pow({base_value}, {exponent})"
            base_value = f"{base_value}**{exponent}"
        return base_value

    def base(self) -> str:
        """Parses a base."""
        if self.current_token == "(":
            self.match("(")
            expr = self.expression()
            self.match(")")
            return f"({expr})"
        elif self.current_token.isdigit() or self.is_float(self.current_token):
            num = self.current_token
            self.advance()
            return num
        elif self.current_token.isidentifier():
            identifier = self.current_token
            self.advance()
            if identifier == "sqrt" or identifier == "log10":
                self.match("(")
                arg = self.expression()
                self.match(")")
                return f"{identifier}({arg})"
            elif identifier == "x":
                return identifier
            else:
                raise SyntaxError(f"Unsupported function or variable: '{identifier}'.")
        else:
            error_message = f"Unexpected token: '{self.current_token}'."
            self.errors.append(error_message)
            self.advance()
            return ""
        
    def is_float(self, token: str) -> bool:
        """Checks if a token is a valid floating-point number."""
        try:
            float(token)
            return True
        except ValueError:
            return False
