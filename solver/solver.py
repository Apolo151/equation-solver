import sympy as sp
import numpy as np
from scipy import optimize
from typing import List, Tuple, Optional

class EquationSolver:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.safe_functions = {
            'log10': lambda x: sp.log(x, 10),
            'exp': sp.exp,
            'sqrt': sp.sqrt,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
        }
        self.numeric_density = 1000  # Points per unit interval
        
    def solve(self, 
             func1_str: str, 
             func2_str: str, 
             x_range: Tuple[float, float] = (-10, 10)
             ) -> List[float]:
        """
        Find intersection points between two functions
        
        Args:
            func1_str: Valid function string for f1(x)
            func2_str: Valid function string for f2(x)
            x_range: Search range for solutions (min, max)
            
        Returns:
            List of x-values within x_range where f1(x) = f2(x)
        """
        try:
            f1 = sp.sympify(func1_str, locals=self.safe_functions)
            f2 = sp.sympify(func2_str, locals=self.safe_functions)
        except (sp.SympifyError, TypeError) as e:
            raise ValueError(f"Invalid function string: {str(e)}") from None

        equation = sp.simplify(f1 - f2)
        solutions = self._symbolic_solve(equation, x_range)
        
        if not solutions:
            solutions = self._numeric_solve(equation, x_range)
            
        return self._clean_solutions(solutions, x_range)

    def _symbolic_solve(self, 
                      equation: sp.Expr, 
                      x_range: Tuple[float, float]
                      ) -> List[float]:
        """Attempt symbolic solution with range filtering"""
        try:
            symbolic_sols = sp.solve(equation, self.x)
            return [
                float(sol.evalf()) 
                for sol in symbolic_sols 
                if sol.is_real and x_range[0] <= sol <= x_range[1]
            ]
        except (NotImplementedError, TypeError):
            return []

    def _numeric_solve(self, 
                     equation: sp.Expr, 
                     x_range: Tuple[float, float]
                     ) -> List[float]:
        """Numerical solution with adaptive sampling"""
        f = sp.lambdify(self.x, equation, modules=['numpy'])
        total_points = int((x_range[1] - x_range[0]) * self.numeric_density)
        x_vals = np.linspace(x_range[0], x_range[1], total_points)
        
        try:
            y_vals = f(x_vals)
        except (ValueError, ZeroDivisionError):
            return []

        # Find potential crossing points
        sign_changes = np.where(np.diff(np.signbit(y_vals)))[0]
        solutions = []
        
        for idx in sign_changes:
            try:
                sol = optimize.fsolve(
                    f, 
                    x_vals[idx],
                    xtol=1e-8,
                    full_output=True
                )[0][0]
                if x_range[0] <= sol <= x_range[1]:
                    solutions.append(sol)
            except (RuntimeWarning, optimize.nonlin.NoConvergence):
                continue
                
        return solutions

    def _clean_solutions(self, 
                       raw_solutions: List[float], 
                       x_range: Tuple[float, float]
                       ) -> List[float]:
        """Deduplicate and validate solutions"""
        unique_solutions = []
        for sol in sorted(raw_solutions):
            # Check precision and range
            if not np.isclose(sol, 0, atol=1e-12):
                sol = round(sol, 8)
                
            if (x_range[0] <= sol <= x_range[1] and 
                not any(np.isclose(sol, s, atol=1e-6) for s in unique_solutions)):
                unique_solutions.append(sol)
                
        return unique_solutions