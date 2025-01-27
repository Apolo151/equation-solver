import pytest
import numpy as np
from plotter.plotter import FunctionPlotter

@pytest.fixture
def plotter():
    return FunctionPlotter()

def test_basic_plotting(plotter):
    """Test plotting of valid functions"""
    plotter.plot("x", "2*x", solutions=[])
    assert len(plotter.ax.lines) == 2
    assert plotter.ax.get_title() == "Function Plot"

def test_solution_annotation(plotter):
    """Test plotting with solutions"""
    plotter.plot("x", "2*x", solutions=[0])
    assert len(plotter.ax.collections) == 1  # Points
    assert len(plotter.ax.texts) == 1        # Annotations

def test_nan_handling(plotter):
    """Test handling of invalid function domains"""
    plotter.plot("log10(x)", "sqrt(x)", solutions=[])
    y1 = plotter.ax.lines[0].get_ydata()
    assert np.isnan(y1[:100]).all()  # First 100 points (x < 0) should be NaN

def test_empty_solutions(plotter):
    """Test plotting without solutions"""
    plotter.plot("x**2", "x+2", solutions=[])
    assert len(plotter.ax.collections) == 0
    assert len(plotter.ax.texts) == 0

def test_error_handling(plotter):
    """Test invalid function plotting"""
    plotter.plot("invalid syntax", "x", solutions=[])
    y1 = plotter.ax.lines[0].get_ydata()
    assert np.isnan(y1).all()
