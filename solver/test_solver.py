import pytest
import math
from solver import EquationSolver

@pytest.fixture
def solver():
    return EquationSolver()

def test_linear_intersection(solver):
    f1 = "x"
    f2 = "2*x - 1"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 1
    assert math.isclose(solutions[0], 1.0, rel_tol=1e-3)

def test_quadratic_intersection(solver):
    f1 = "x**2"
    f2 = "x"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 2
    assert 0.0 in solutions
    assert 1.0 in solutions

def test_logarithmic_intersection(solver):
    f1 = "log10(x)"
    f2 = "0"
    solutions = solver.solve(f1, f2, x_range=(0.1, 10))
    assert len(solutions) == 1
    assert math.isclose(solutions[0], 1.0, rel_tol=1e-3)

def test_trigonometric_intersection(solver):
    f1 = "math.sin(x)"
    f2 = "0"
    solutions = solver.solve(f1, f2, x_range=(-5, 5))
    assert len(solutions) == 3
    assert -math.pi in pytest.approx(solutions, abs=1e-3)
    assert 0.0 in solutions
    assert math.pi in pytest.approx(solutions, abs=1e-3)

def test_no_solutions(solver):
    f1 = "x + 2"
    f2 = "x + 5"
    solutions = solver.solve(f1, f2)
    assert len(solutions) == 0

def test_edge_cases(solver):
    # Test division by zero handling
    f1 = "1/x"
    f2 = "0"
    solutions = solver.solve(f1, f2, x_range=(-2, 2))
    assert len(solutions) == 0
