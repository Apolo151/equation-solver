import numpy as np
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt

class FunctionPlotter:
    def __init__(self):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self._init_plot()
        self.safe_dict = {
            'math': math,
            'log10': math.log10,
            'sqrt': math.sqrt,
            'np': np
        }

    def _init_plot(self):
        """Initialize empty plot with labels"""
        self.ax.clear()
        self.ax.set_title("Function Plot")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

    def _safe_eval(self, func_str, x_values):
        """Safely evaluate function over an array of x values"""
        y = np.zeros_like(x_values)
        for i, x in enumerate(x_values):
            try:
                y[i] = eval(func_str, {"__builtins__": None}, 
                           {**self.safe_dict, "x": x})
            except:
                y[i] = np.nan
        return y

    def plot(self, func1_str, func2_str, solutions=[]):
        """
        Plot two functions and their intersection points
        
        Args:
            func1_str (str): Validated function 1 string
            func2_str (str): Validated function 2 string
            solutions (list): x-values of intersection points
        """
        self._init_plot()
        
        # Generate x values
        x = np.linspace(-10, 10, 400)
        x_fine = np.linspace(-10, 10, 4000)  # For better solution visualization
        
        # Evaluate functions
        y1 = self._safe_eval(func1_str, x)
        y2 = self._safe_eval(func2_str, x)

        # Plot functions
        self.ax.plot(x, y1, label='Function 1', color='blue')
        self.ax.plot(x, y2, label='Function 2', color='green')

        # Plot solutions if they exist
        if solutions:
            for sol_x in solutions:
                try:
                    sol_y = self._safe_eval(func1_str, np.array([sol_x]))[0]
                    if not np.isnan(sol_y):
                        self.ax.plot(sol_x, sol_y, 'ro', markersize=8)
                        self.ax.annotate(
                            f'({sol_x:.2f}, {sol_y:.2f})',
                            (sol_x, sol_y),
                            textcoords="offset points",
                            xytext=(10,-10),
                            ha='center'
                        )
                except:
                    continue

        # Set dynamic axis limits
        y_combined = np.concatenate([y1[~np.isnan(y1)], y2[~np.isnan(y2)]])
        if len(y_combined) > 0:
            y_min = np.nanmin(y_combined) - 1
            y_max = np.nanmax(y_combined) + 1
            self.ax.set_ylim(y_min, y_max)

        self.ax.legend()
        self.canvas.draw()
