from PySide6 import QtWidgets


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle("CSS Tech Test")
        self.resize(500, 300)
