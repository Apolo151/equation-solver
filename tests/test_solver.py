import pytest
import math
import numpy as np
from solver.solver import EquationSolver

@pytest.fixture
def solver():
    return EquationSolver()

# Core functionality tests
def test_symbolic_polynomial_solution(solver):
    """Test exact symbolic solution for polynomial equation"""
    solutions = solver.solve("x**2 - 4", "0", (-5, 5))
    assert sorted(solutions) == pytest.approx([-2.0, 2.0])

def test_numerical_fallback(solver):
    """Test numerical fallback for non-symbolic solution"""
    solutions = solver.solve("sin(x)", "x/2", (-5, 5))
    expected = [-1.895494, 0.0, 1.895494]
    assert solutions == pytest.approx(expected, rel=1e-4)

def test_mixed_symbolic_numeric(solver):
    """Test combination of symbolic and numeric roots"""
    solutions = solver.solve("x*(sin(x)-0.5)", "0", (-5, 5))
    assert 0.0 in solutions
    assert any(abs(s - math.pi/6) < 0.01 for s in solutions)

# Edge case tests
def test_asymptotic_behavior(solver):
    """Test function with vertical asymptote"""
    solutions = solver.solve("1/(x-1)", "1", (-2, 2))
    assert solutions == pytest.approx([2.0])

# Precision and numerical stability tests
def test_near_zero_solutions(solver):
    """Test solutions near zero"""
    solutions = solver.solve("1e-8*x", "1e-8", (-1, 1))
    assert solutions == pytest.approx([1.0])

def test_extreme_value_range(solver):
    """Test large value handling"""
    solutions = solver.solve("1e-15*x", "1e-15", (-1e20, 1e20))
    assert solutions == pytest.approx([1.0])

def test_solution_deduplication(solver):
    """Test solution cleaning logic"""
    raw = [0.0, 0.0, 1.0000001, 1.0000002, 2.0]
    cleaned = solver._clean_solutions(raw, (-5, 5))
    assert cleaned == pytest.approx([0.0, 1.0, 2.0])

# Special function tests
def test_composite_function(solver):
    """Test nested function solution with sqrt and log10"""
    solutions = solver.solve("sqrt(log10(x + 1))", "0.5 * x", (0, 5))
    
    assert len(solutions) == 1
    for s in solutions:
        # Ensure x + 1 > 0 for log10
        assert s + 1 > 0
        # Check if sqrt(log10(x + 1)) == 0.5 * x
        assert np.isclose(
            math.sqrt(math.log10(s + 1)), 
            0.5 * s, 
            atol=1e-6
        )

def test_logarithmic_identity(solver):
    """Test log10 implementation"""
    solutions = solver.solve("log10(x)", "2", (1, 1000))
    assert solutions == pytest.approx([100.0])

# Boundary condition tests
def test_range_exclusion(solver):
    """Test solution filtering by range"""
    solutions = solver.solve("x", "0", (1, 10))
    assert len(solutions) == 0

def test_boundary_solutions(solver):
    """Test solutions at range boundaries"""
    solutions = solver.solve("(x-1)*(x-5)", "0", (1, 5))
    assert sorted(solutions) == pytest.approx([1.0, 5.0])

# Error condition tests
def test_invalid_equation(solver):
    """Test invalid input handling"""
    with pytest.raises(NameError):
        solver.solve("invalid_function(x)", "0", (-10, 10))

def test_non_real_solutions(solver):
    """Test filtering of complex roots"""
    solutions = solver.solve("x**2 + 1", "0", (-5, 5))
    assert len(solutions) == 0

# Performance stress tests
def test_high_degree_polynomial(solver):
    """Test 10th-degree polynomial solution"""
    coeffs = np.poly(np.arange(1, 11))
    poly_expr = "+".join(f"({c}*x**{i})" 
                       for i, c in enumerate(coeffs[::-1]))
    solutions = solver.solve(poly_expr, "0", (-15, 15))
    assert len(solutions) == 10
    assert all(np.isclose(np.polyval(coeffs, s), 0, atol=1e-6) 
               for s in solutions)

def test_extreme_density_requirements(solver):
    """Test adaptive sampling with sharp features"""
    solver.numeric_density = 5000  # Points per unit
    solutions = solver.solve("tan(x)", "1e6*(x % 0.000001)", (-1, 1))
    assert len(solutions) > 100