from PySide2.QtWidgets import QApplication
from gui.main_window import MainWindow


# Create the application instance
app = QApplication([])

window = MainWindow()
window.show()

app.exec_()

