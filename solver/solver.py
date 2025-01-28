import sympy as sp
from typing import List, Tuple
import numpy as np
from scipy import optimize

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
        self.solutions = []
        
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
        self.solutions = []
        # Convert strings to sympy expressions
        try:
            f1 = sp.sympify(func1_str, locals=self.safe_functions)
            f2 = sp.sympify(func2_str, locals=self.safe_functions)
        except sp.SympifyError:
            return []

        # Create equation f1 - f2 = 0
        equation = f1 - f2

        # check zero solution
        equation = sp.simplify(equation)
        if equation.subs(self.x, 0) == 0:
            self.solutions.append(0)

        # Try symbolic solving first
        try:
            if equation.is_polynomial():
                self.solutions.append(sp.solve(equation, self.x))
            else:
                # For non-polynomial equations, use numerical solving
                # Note: Currently Only log10 and sqrt are supported
                self.solutions.append(self._solve_numerical(equation))
        except:
            # Fallback to numerical solving
                self.solutions.append(self._solve_numerical(equation))
        
        return self.solutions
        

    def _solve_numerical(self, equation) -> List[float]:
        """Solve equation numerically using scipy optimize."""
        # NOTE: log10 and sqrt are the only supported functions currently
        # if log is in equation set range to x > 0
        if sp.log in equation.atoms(sp.Function):
            x_range = np.linspace(1e-10, 100, 1000)
        elif sp.sqrt in equation.atoms(sp.Function):
            x_range = np.linspace(0, 100, 1000)
        else:
            x_range = np.linspace(-100, 100, 1000)
        
        # Convert sympy expression to numpy function
        f = sp.lambdify(self.x, equation, modules=['numpy'])
        
        # Find sign changes to get initial guesses
        y_vals = f(x_range)
        sign_changes = np.where(np.diff(np.signbit(y_vals)))[0]

        for idx in sign_changes:
            x_guess = x_range[idx]
            try:
                sol = optimize.fsolve(f, x_guess)[0]
                if -10 <= sol <= 10 and abs(f(sol)) < 1e-10:
                    self.solutions.append(round(float(sol), 5))
            except:
                continue
                
        return sorted(list(set(self.solutions)))