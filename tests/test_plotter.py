import pytest
import numpy as np
import matplotlib
import math
from plotter.plotter import FunctionPlotter

matplotlib.use("Agg")  # Ensure tests run without a GUI

@pytest.fixture
def plotter():
    return FunctionPlotter()

def test_basic_plotting(plotter):
    """Test plotting of valid functions"""
    plotter.plot("x", "2*x", solutions=[])
    lines = [line for line in plotter.ax.lines 
            if line.get_label() in {'Function 1', 'Function 2'}]
    assert len(lines) == 2
    assert lines[0].get_color() == 'blue'
    assert lines[1].get_color() == 'green'

def test_solution_annotation(plotter):
    """Test plotting with solutions"""
    plotter.plot("x", "2*x", solutions=[0])
    assert len(plotter.ax.collections) == 1  # Scatter plot
    assert len(plotter.ax.texts) == 1        # Annotations

def test_nan_handling(plotter):
    """Test handling of invalid function domains"""
    plotter.plot("log10(x)", "sqrt(x)", solutions=[])
    lines = [line for line in plotter.ax.lines 
            if line.get_label() in {'Function 1', 'Function 2'}]
    
    # Check log10 (first function)
    log_y = lines[0].get_ydata()
    assert np.isnan(log_y[:200]).all()  # First 200 points (x < 0)
    
    # Check sqrt (second function)
    sqrt_y = lines[1].get_ydata()
    assert np.isnan(sqrt_y[:200]).all()  # First 200 points (x < 0)

def test_empty_solutions(plotter):
    """Test plotting without solutions"""
    plotter.plot("x**2", "x+2", solutions=[])
    assert len(plotter.ax.collections) == 0
    assert len(plotter.ax.texts) == 0

def test_error_handling(plotter):
    """Test invalid function plotting"""
    plotter.plot("invalid syntax", "x", solutions=[])
    lines = [line for line in plotter.ax.lines 
            if line.get_label() in {'Function 1', 'Function 2'}]
    assert np.all(np.isnan(lines[0].get_ydata()))

def test_high_value_handling(plotter):
    """Test plotting with extreme values"""
    plotter.plot("1e6*x", "1e6*(x-1)", solutions=[1])
    lines = [line for line in plotter.ax.lines 
            if line.get_label() in {'Function 1', 'Function 2'}]
    assert abs(lines[0].get_ydata()[-1]) > 1e6

def test_constant_functions(plotter):
    """Test plotting constant functions"""
    plotter.plot("5", "5", solutions=[])
    lines = [line for line in plotter.ax.lines 
            if line.get_label() in {'Function 1', 'Function 2'}]
    assert np.allclose(lines[0].get_ydata(), 5)