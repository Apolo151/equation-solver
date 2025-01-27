import pytest
import math
from parser.parser import Parser

@pytest.fixture
def parser():
    return Parser()

# Valid Cases
def test_valid_function(parser):
    func, errors = parser.parse("5*x**3 + log10(x)")
    assert not errors
    assert func == "5*x**3+log10(x)"

def test_valid_sqrt(parser):
    func, errors = parser.parse("sqrt(x+2)")
    assert not errors

def test_valid_parentheses(parser):
    func, errors = parser.parse("(x + 2)*(x - 3)")
    assert not errors

def test_valid_multiple_operators(parser):
    func, errors = parser.parse("x**2 + 3*x - 5/(sqrt(x))")
    assert not errors

def test_valid_complex_function(parser):
    func, errors = parser.parse("(sqrt(x) + log10(x**2)) / (5 - x)")
    assert not errors

# Edge Cases
def test_empty_input(parser):
    func, errors = parser.parse("")
    assert len(errors) == 1
    assert "Function cannot be empty." in errors[0]

def test_whitespace_handling(parser):
    func, errors = parser.parse(" 5 * x ** 2 + log10( x ) ")
    assert not errors
    assert func == "5*x**2+log10(x)"

def test_operator_replacement(parser):
    func, errors = parser.parse("x^2")
    assert not errors
    assert func == "x**2"

# Invalid Syntax Cases
def test_invalid_syntax(parser):
    func, errors = parser.parse("5*x^ + 2")
    assert len(errors) > 0
    assert "Invalid syntax" in errors[0]

def test_mismatched_parentheses(parser):
    func, errors = parser.parse("(5*x + 2")
    assert len(errors) == 1
    assert "Mismatched parentheses" in errors[0]
    
    func, errors = parser.parse("5*x + 2)")
    assert len(errors) == 1
    assert "Mismatched parentheses" in errors[0]

def test_invalid_characters(parser):
    func, errors = parser.parse("x$2 + 5")
    assert len(errors) == 1
    assert "Invalid characters detected." in errors[0]

def test_malformed_function_calls(parser):
    func, errors = parser.parse("log10x")
    assert len(errors) == 1
    assert "Invalid syntax" in errors[0]

def test_case_sensitivity(parser):
    func, errors = parser.parse("Log10(x)")
    assert len(errors) == 1
    assert "Invalid characters detected." in errors[0]

def test_exponential_notation(parser):
    func, errors = parser.parse("1.2e-5*x")
    assert len(errors) == 1
    assert "Invalid characters detected." in errors[0]

def test_invalid_mixed_operators(parser):
    func, errors = parser.parse("x**+2")
    assert len(errors) == 1
    assert "Invalid syntax" in errors[0]

def test_invalid_decimal(parser):
    func, errors = parser.parse("5.2.3*x")
    assert len(errors) == 1
    assert "Invalid syntax" in errors[0]

# Function Validation
def test_unsupported_operator(parser):
    func, errors = parser.parse("sin(x)")
    assert len(errors) == 1
    assert "Invalid characters detected." in errors[0]

def test_nested_functions(parser):
    func, errors = parser.parse("sqrt(log10(x))")
    assert not errors

def test_log10_with_parameters(parser):
    func, errors = parser.parse("log10(x, 2)")
    assert len(errors) == 1
    assert "Invalid syntax" in errors[0]

def test_implicit_multiplication(parser):
    func, errors = parser.parse("5x")
    assert len(errors) == 1
    assert "Invalid syntax" in errors[0]

# Stress Tests
def test_long_input(parser):
    long_func = "x+" + "x+"*500 + "x"
    func, errors = parser.parse(long_func)
    assert not errors

def test_multiple_errors(parser):
    func, errors = parser.parse("sin(x) + 5*x^")
    assert len(errors) >= 2
    assert any("Invalid characters" in e for e in errors)
    assert any("Invalid syntax" in e for e in errors)

# Boundary Cases
def test_minimal_valid(parser):
    func, errors = parser.parse("x")
    assert not errors

def test_max_operators(parser):
    func, errors = parser.parse("x++++++++x")
    assert len(errors) == 1
    assert "Invalid syntax" in errors[0]