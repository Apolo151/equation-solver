import pytest
import numpy as np
import math
from plotter.plotter import FunctionPlotter

@pytest.fixture
def plotter():
    return FunctionPlotter()

# def test_basic_plotting(plotter):
#     """Test basic function plotting with valid inputs"""
#     plotter.plot("x", "2*x", solutions=[])
    
#     # Verify two lines are plotted
#     assert len(plotter.ax.lines) == 2
    
#     # Verify line colors and labels
#     line1, line2 = plotter.ax.lines
#     assert line1.get_color() == 'blue'
#     assert line2.get_color() == 'green'
#     assert line1.get_label() == 'Function 1'
#     assert line2.get_label() == 'Function 2'
    
#     # Verify data accuracy
#     x_data = line1.get_xdata()
#     assert np.allclose(line1.get_ydata(), x_data)
#     assert np.allclose(line2.get_ydata(), 2*x_data)

# def test_solution_annotation(plotter):
#     """Test solution point annotation"""
#     solutions = [0.0, 2.0]
#     plotter.plot("x**2", "2*x", solutions=solutions)
    
#     # Verify points and annotations
#     points = plotter.ax.collections[0]
#     annotations = plotter.ax.texts
    
#     assert len(points.get_offsets()) == 2
#     assert len(annotations) == 2
    
#     # Verify annotation positions
#     for sol, text in zip(solutions, annotations):
#         x, y = text.get_position()
#         assert math.isclose(x, sol, abs_tol=1e-3)
#         assert math.isclose(y, sol**2, abs_tol=1e-3)
#         assert f"({sol:.2f}" in text.get_text()

# def test_nan_handling(plotter):
#     """Test invalid function domains"""
#     plotter.plot("log10(x)", "sqrt(x)", solutions=[])
    
#     # Get both function lines
#     line1, line2 = plotter.ax.lines
    
#     # Verify log10 NaN handling
#     log_x = line1.get_xdata()[:100]  # First 100 points
#     log_y = line1.get_ydata()[:100]
#     assert np.all(log_x <= 0)  # Default linspace includes x<=0
#     assert np.all(np.isnan(log_y))
    
#     # Verify sqrt NaN handling
#     sqrt_x = line2.get_xdata()[:100]
#     sqrt_y = line2.get_ydata()[:100]
#     assert np.all(sqrt_x < 0)
#     assert np.all(np.isnan(sqrt_y))

# def test_empty_solutions(plotter):
#     """Test plotting without solutions"""
#     plotter.plot("x", "x+1", solutions=[])
    
#     # Verify no annotations
#     assert len(plotter.ax.collections) == 0
#     assert len(plotter.ax.texts) == 0
    
#     # Verify lines still exist
#     assert len(plotter.ax.lines) == 2

# def test_error_handling(plotter):
#     """Test invalid function plotting"""
#     plotter.plot("invalid syntax", "x", solutions=[])
    
#     # First line should be invalid function
#     line = plotter.ax.lines[0]
#     assert np.all(np.isnan(line.get_ydata()))

# def test_dynamic_axis_scaling(plotter):
#     """Test automatic y-axis limits adjustment"""
#     plotter.plot("x**2", "-x**2", solutions=[0])
    
#     y_min, y_max = plotter.ax.get_ylim()
#     assert y_min < -1
#     assert y_max > 1
#     assert abs(y_min - y_max) > 2

# def test_high_value_handling(plotter):
#     """Test plotting with extreme values"""
#     plotter.plot("1e6*x", "1e6*(x-1)", solutions=[1])
#     line1, line2 = plotter.ax.lines
    
#     # Verify data scaling
#     assert np.nanmax(line1.get_ydata()) > 1e6
#     assert np.nanmin(line2.get_ydata()) < -1e6
    
#     # Verify solution annotation
#     point = plotter.ax.collections[0].get_offsets()[0]
#     assert math.isclose(point[0], 1.0, rel_tol=1e-6)

# def test_discontinuous_functions(plotter):
#     """Test plotting functions with discontinuities"""
#     plotter.plot("1/(x-1)", "tan(x)", solutions=[])
    
#     # Verify NaN insertion at discontinuities
#     line1, line2 = plotter.ax.lines
#     assert np.any(np.isnan(line1.get_ydata()))
#     assert np.any(np.isnan(line2.get_ydata()))

# def test_constant_functions(plotter):
#     """Test plotting constant functions"""
#     plotter.plot("5", "5", solutions=[])
#     line1, line2 = plotter.ax.lines
    
#     # Verify horizontal lines
#     assert np.allclose(line1.get_ydata(), 5)
#     assert np.allclose(line2.get_ydata(), 5)

# def test_legend_entries(plotter):
#     """Test legend creation and labels"""
#     plotter.plot("x", "x**2", solutions=[0,1])
#     legend = plotter.ax.get_legend()
    
#     # Verify legend existence and labels
#     assert legend is not None
#     labels = [text.get_text() for text in legend.get_texts()]
#     assert labels == ['Function 1', 'Function 2']