from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QListWidget, QHBoxLayout, QGroupBox, QFormLayout
from PySide2.QtCore import QSize
from parser.parser import Parser
from solver.solver import EquationSolver
from plotter.plotter import FunctionPlotter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Solver and Plotter")
        self.parser = Parser()  # Initialize parser
        self.solver = EquationSolver()
        self.plotter = FunctionPlotter()

        # Main layout
        main_layout = QHBoxLayout()

        # Left side - Input forms and error lists
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # Function 1 GroupBox
        func1_group = QGroupBox("Function 1")
        func1_layout = QVBoxLayout()
        self.func1_input = QLineEdit()
        func1_layout.addWidget(self.func1_input)
        self.func1_errors = QListWidget()
        func1_layout.addWidget(self.func1_errors)
        func1_group.setLayout(func1_layout)
        left_layout.addWidget(func1_group)

        # Function 2 GroupBox
        func2_group = QGroupBox("Function 2")
        func2_layout = QVBoxLayout()
        self.func2_input = QLineEdit()
        func2_layout.addWidget(self.func2_input)
        self.func2_errors = QListWidget()
        func2_layout.addWidget(self.func2_errors)
        func2_group.setLayout(func2_layout)
        left_layout.addWidget(func2_group)

        # Solve and Plot button
        self.solve_plot_button = QPushButton("Solve and Plot")
        self.solve_plot_button.clicked.connect(self.solveAndPlot)
        left_layout.addWidget(self.solve_plot_button)

        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget, 1)  # Stretch factor 1

        # Right side - Plot canvas
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.plotter.canvas)
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 1)  # Stretch factor 1

        # Set main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setMinimumSize(QSize(480, 320))
        self.setMaximumSize(QSize(1280, 720))

    def solveAndPlot(self):
        func1 = self.func1_input.text()
        func2 = self.func2_input.text()
        # Clear error lists
        self.func1_errors.clear()
        self.func2_errors.clear()

        # Parse and validate Function 1
        parsed_func1, errors1 = self.parser.parse(func1)
        for error in errors1:
            self.func1_errors.addItem(error)

        # Parse and validate Function 2
        parsed_func2, errors2 = self.parser.parse(func2)
        for error in errors2:
            self.func2_errors.addItem(error)

        # Proceed to solve and plot if inputs are valid
        if not errors1 and not errors2:
            try:
                solutions = self.solver.solve(parsed_func1, parsed_func2)
                if solutions:
                    self.plotter.plot(parsed_func1, parsed_func2, solutions)
                else:
                    self.plotter.plot(parsed_func1, parsed_func2)
                    self.func1_errors.addItem("No intersections found")
            except Exception as e:
                self.func1_errors.addItem("Plotting error")
                self.func2_errors.addItem(str(e))


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())