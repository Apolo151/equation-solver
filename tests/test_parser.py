import pytest
from parser.parser import Parser

def test_valid_function():
    parser = Parser()
    func, errors = parser.parse("5*x**3 + log10(x)")
    assert not errors
    assert func == "5*x**3 + log10(x)"

def test_invalid_syntax():
    parser = Parser()
    func, errors = parser.parse("5*x^ + 2")
    assert len(errors) > 0
    assert "Invalid syntax" in errors[0]

def test_unsupported_operator():
    parser = Parser()
    func, errors = parser.parse("sin(x)")
    assert "Invalid characters detected." in errors[0]
