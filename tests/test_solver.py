import pytest
import math
import numpy as np
from solver.solver import EquationSolver

@pytest.fixture
def solver():
    return EquationSolver()

# Main Cases
def test_linear_intersection(solver):
    """Test intersection of linear functions."""
    f1 = "x"
    f2 = "2*x-1"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 1
    assert math.isclose(solutions[0], 1.0, rel_tol=1e-3)

def test_quadratic_intersection(solver):
    """Test intersection of quadratic and linear functions."""
    f1 = "x**2"
    f2 = "x"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 2
    assert 0.0 in solutions
    assert 1.0 in solutions

def test_logarithmic_intersection(solver):
    """Test intersection involving logarithmic functions."""
    f1 = "log10(x)"
    f2 = "0"
    solutions = solver.solve(f1, f2, x_range=(0.1, 10))
    assert len(solutions) == 1
    assert math.isclose(solutions[0], 1.0, rel_tol=1e-3)

def test_no_solutions(solver):
    """Test case where no intersections exist."""
    f1 = "x + 2"
    f2 = "x + 5"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 0

# Edge Cases
def test_division_by_zero(solver):
    """Test handling of division by zero."""
    f1 = "1/x"
    f2 = "0"
    solutions = solver.solve(f1, f2, x_range=(-2, 2))
    assert len(solutions) == 0

def test_large_exponents(solver):
    """Test intersection with large exponents."""
    f1 = "x**10"
    f2 = "x**5"
    solutions = solver.solve(f1, f2, x_range=(-10, 10))
    assert len(solutions) == 2
    assert 0.0 in solutions
    assert 1.0 in solutions

def test_constant_functions(solver):
    """Test intersection of constant functions."""
    f1 = "5"
    f2 = "5"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 0  # Parallel lines, no intersection

def test_identical_functions(solver):
    """Test intersection of identical functions."""
    f1 = "x**2"
    f2 = "x**2"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 0  # Infinite intersections, treated as no unique solution

def test_nested_functions(solver):
    """Test intersection involving nested functions."""
    f1 = "log10(sqrt(x))"
    f2 = "0"
    solutions = solver.solve(f1, f2, x_range=(-5, 5))
    assert len(solutions) > 0  # At least one intersection exists

def test_invalid_input(solver):
    """Test handling of invalid input."""
    f1 = "invalid_function(x)"
    f2 = "x"
    with pytest.raises(Exception):
        solver.solve(f1, f2)

def test_large_x_range(solver):
    """Test intersection over a large x-range."""
    f1 = "x**3"
    f2 = "x"
    solutions = solver.solve(f1, f2, x_range=(-100, 100))
    assert len(solutions) == 3
    assert -1.0 in solutions
    assert 0.0 in solutions
    assert 1.0 in solutions

def test_multiple_roots(solver):
    """Test intersection with multiple roots."""
    f1 = "x**3 - 6*x**2 + 11*x - 6"
    f2 = "0"
    solutions = solver.solve(f1, f2, x_range=(-10, 10))
    assert len(solutions) == 3
    assert 1.0 in solutions
    assert 2.0 in solutions
    assert 3.0 in solutions

def test_asymptotic_functions(solver):
    """Test intersection of functions with asymptotes."""
    f1 = "1/(x-1)"
    f2 = "1/(x+1)"
    solutions = solver.solve(f1, f2, x_range=(-10, 10))
    assert len(solutions) == 0  # No intersection due to asymptotes

def test_complex_functions(solver):
    """Test intersection of complex functions."""
    f1 = "x**2"
    f2 = "E**x"
    solutions = solver.solve(f1, f2, x_range=(-1, 1))
    print(solutions)
    assert len(solutions) == 1

def test_zero_crossings(solver):
    """Test intersection at zero crossings."""
    f1 = "x"
    f2 = "-x"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 1
    assert 0.0 in solutions

def test_near_misses(solver):
    """Test functions that nearly intersect but don't."""
    f1 = "x + 0.0001"
    f2 = "x"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 0  # No intersection due to slight offset

def test_large_coefficients(solver):
    """Test intersection with large coefficients."""
    f1 = "1e6*x"
    f2 = "1e6*x + 1"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 0  # Parallel lines, no intersection

def test_small_coefficients(solver):
    """Test intersection with small coefficients."""
    f1 = "0.00001*x"
    f2 = "0.00001*x**2"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 2
    assert 0.0 in solutions
    assert 1.0 in solutions