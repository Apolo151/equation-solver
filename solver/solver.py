import sympy as sp
from typing import List, Tuple

class EquationSolver:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.safe_functions = {
            'log10': sp.log,
            'sqrt': sp.sqrt,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
        }
        
    def solve(self, func1_str: str, func2_str: str, x_range: Tuple[float, float] = (-10, 10)
              ) -> List[float]:
        """
        Find intersection points between two functions using SymPy
        
        Args:
            func1_str (str): First function string
            func2_str (str): Second function string
            x_range (tuple): Search range for solutions
            num_guesses (int): Not used with sympy implementation
            
        Returns:
            list: x-values of intersection points within range
        """
        # Convert strings to sympy expressions
        try:
            f1 = sp.sympify(func1_str, locals=self.safe_functions)
            f2 = sp.sympify(func2_str, locals=self.safe_functions)
        except sp.SympifyError:
            return []

        # Create equation f1 - f2 = 0
        equation = f1 - f2

        # Solve symbolically
        try:
            solutions = sp.solve(equation, self.x)
        except sp.PolynomialError:
            # Fall back to numerical solving for non-polynomial equations
            solutions = sp.nsolve(equation, self.x, 0, verify=False)

        # Convert to float and filter solutions
        valid_solutions = []
        for sol in solutions:
            try:
                x_val = float(sol.evalf())
                if (x_range[0] <= x_val <= x_range[1] and 
                    not any(abs(x_val - s) < 1e-5 for s in valid_solutions)):
                    valid_solutions.append(round(x_val, 5))
            except (TypeError, ValueError):
                continue

        return sorted(valid_solutions)