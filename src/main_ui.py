from PySide6 import QtWidgets

from control_board_simulation.control_board import ControlBoard
from control_board_simulation.environment import Environment
from user_interface.window import Window

if __name__ == "__main__":
    import sys

    environment = Environment(light=False, light_level=0, movement=False, distance=0)
    control_board = ControlBoard(environment)

    app = QtWidgets.QApplication(sys.argv)
    window = Window(control_board)
    window.show()
    sys.exit(app.exec_())
