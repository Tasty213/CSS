from PySide6 import QtWidgets

from control_board_simulation.control_board import ControlBoard
from control_board_simulation.environment import RealisticEnvironment
from user_interface.window import Window

if __name__ == "__main__":
    import sys

    environment = RealisticEnvironment()
    control_board = ControlBoard(environment)

    app = QtWidgets.QApplication(sys.argv)
    window = Window(control_board)
    window.show()
    sys.exit(app.exec())
