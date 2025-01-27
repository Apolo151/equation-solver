import pytest
from parser.parser import Parser

@pytest.fixture
def parser():
    return Parser()

# Valid Cases
def test_valid_basic_expression(parser):
    expr, errors = parser.parse("5 + x")
    assert not errors
    assert expr == "5+x"

def test_valid_complex_expression(parser):
    expr, errors = parser.parse("5*x^2 + sqrt(x)")
    assert not errors
    assert expr == "5*x**2+sqrt(x)"

def test_valid_log_function(parser):
    expr, errors = parser.parse("log10(x + 5)")
    assert not errors
    assert expr == "log10(x+5)"

def test_valid_parentheses(parser):
    expr, errors = parser.parse("(x + 2) * (x - 3)")
    assert not errors
    assert expr == "(x+2)*(x-3)"

def test_valid_power_expression(parser):
    expr, errors = parser.parse("x^2 + 3*x - 5")
    assert not errors
    assert expr == "x**2+3*x-5"

# Edge Cases
def test_whitespace_handling(parser):
    expr, errors = parser.parse("  5  * x   ^  2 + sqrt( x )  ")
    assert not errors
    assert expr == "5*x**2+sqrt(x)"

def test_empty_input(parser):
    expr, errors = parser.parse("")
    assert len(errors) == 1
    assert "Empty expression." in errors

def test_unsupported_identifier(parser):
    expr, errors = parser.parse("sin(x)")
    assert len(errors) == 1
    assert "Unsupported function or variable: 'sin'." in errors

def test_decimal_handling(parser):
    expr, errors = parser.parse("3.5 * x + 2.0")
    assert not errors
    assert expr == "3.5*x+2.0"

# Invalid Syntax Cases
def test_mismatched_parentheses(parser):
    expr, errors = parser.parse("(5 + x")
    assert len(errors) == 1
    assert "Expected ')' but got 'None'." in errors

def test_unexpected_token(parser):
    expr, errors = parser.parse("5 * x ^ + 3")
    assert len(errors) >= 1 #TODO: recheck this
    assert "Unexpected token: '+'." in errors

def test_invalid_characters(parser):
    expr, errors = parser.parse("5 * x $ 2")
    assert len(errors) == 1
    assert "Invalid characters in expression." in errors

def test_multiple_errors(parser):
    expr, errors = parser.parse("5 * x ^ + sqrt )")
    assert len(errors) > 1
    assert any("Unexpected token" in error for error in errors)

# Stress Tests
def test_large_input(parser):
    large_expr = "+".join(["x^2"] * 1000)
    expr, errors = parser.parse(large_expr)
    assert not errors

def test_nested_functions(parser):
    expr, errors = parser.parse("sqrt(log10(x))")
    assert not errors
    assert expr == "sqrt(log10(x))"

def test_multiple_operations(parser):
    expr, errors = parser.parse("x^2 * sqrt(x) + log10(x)")
    assert not errors
    assert expr == "x**2*sqrt(x)+log10(x)"

# Boundary Cases
def test_single_variable(parser):
    expr, errors = parser.parse("x")
    assert not errors
    assert expr == "x"

def test_single_number(parser):
    expr, errors = parser.parse("42")
    assert not errors
    assert expr == "42"

def test_single_function(parser):
    expr, errors = parser.parse("sqrt(4)")
    assert not errors
    assert expr == "sqrt(4)"

def test_minimal_expression(parser):
    expr, errors = parser.parse("x + 1")
    assert not errors
    assert expr == "x+1"
