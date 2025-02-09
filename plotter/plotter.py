import numpy as np
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FunctionPlotter:
    def __init__(self):
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self._init_plot()
        
    def _init_plot(self):
        """Initialize plot without creating extra Line2D objects"""
        self.ax.clear()
        self.ax.set_title("Function Plot")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        
        # Set spines at origin instead of using axhline/axvline
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')

    def _safe_eval(self, func_str, x_values):
        """Return NaN for invalid evaluations"""
        y = np.full_like(x_values, np.nan, dtype=float)
        for i, x in enumerate(x_values):
            try:
                y[i] = eval(func_str, {"__builtins__": None}, {
                    'x': x,
                    'sqrt': math.sqrt,
                    'log10': math.log10,
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan
                })
            except:
                pass
        return y

    def plot(self, func1_str, func2_str, solutions=[]):
        """Plot with proper error handling and solution markers"""
        self._init_plot()
        x = np.linspace(-10, 10, 400)
        
        # Plot functions
        y1 = self._safe_eval(func_str=func1_str, x_values=x)
        y2 = self._safe_eval(func_str=func2_str, x_values=x)
        self.ax.plot(x, y1, label='Function 1', color='blue')
        self.ax.plot(x, y2, label='Function 2', color='green')

        # Plot solutions as scatter points
        if solutions:
            sol_x = []
            sol_y = []
            for s in solutions:
                try:
                    y_val = self._safe_eval(func1_str, np.array([s]))[0]
                    if not np.isnan(y_val):
                        sol_x.append(s)
                        sol_y.append(y_val)
                except:
                    continue
            if sol_x:
                self.ax.scatter(sol_x, sol_y, color='red', s=60, zorder=5)
                for x_val, y_val in zip(sol_x, sol_y):
                    self.ax.annotate(
                        f"({x_val:.2f}, {y_val:.2f})",
                        (x_val, y_val),
                        textcoords="offset points",
                        xytext=(10, -10),
                        ha='center'
                    )

        # Set dynamic axis limits
        y_combined = np.concatenate([y1[~np.isnan(y1)], y2[~np.isnan(y2)]])
        if len(y_combined) > 0:
            y_pad = 0.1 * (np.nanmax(y_combined) - np.nanmin(y_combined))
            self.ax.set_ylim(np.nanmin(y_combined) - y_pad, 
                            np.nanmax(y_combined) + y_pad)
        
        self.ax.legend()
        self.canvas.draw()