import numpy as np
from scipy.optimize import fsolve
import math

class EquationSolver:
    def __init__(self):
        self.safe_dict = {
            'math': math,
            'log10': math.log10,
            'sqrt': math.sqrt
        }
        
    def solve(self, func1_str, func2_str, x_range=(-10, 10), num_guesses=100):
        """
        Find intersection points between two functions
        
        Args:
            func1_str (str): Validated function 1 string
            func2_str (str): Validated function 2 string
            x_range (tuple): Search range for solutions
            num_guesses (int): Number of initial guesses
            
        Returns:
            list: x-values of intersection points
        """
        # Create lambda functions with safe evaluation
        f1 = lambda x: eval(func1_str, {"__builtins__": None}, {**self.safe_dict, "x": x})
        f2 = lambda x: eval(func2_str, {"__builtins__": None}, {**self.safe_dict, "x": x})
        diff = lambda x: f1(x) - f2(x)

        solutions = []
        x_guesses = np.linspace(x_range[0], x_range[1], num_guesses)
        
        for guess in x_guesses:
            try:
                sol = fsolve(diff, guess, full_output=True)
                if sol[2] == 1:  # Check if solution converged
                    x = sol[0][0]
                    # Verify solution is within range and not duplicate
                    if (x_range[0] <= x <= x_range[1] and 
                        not any(np.isclose(x, s, atol=1e-5) for s in solutions)):
                        solutions.append(round(x, 5))
            except:
                continue

        return sorted(list(set(solutions)))