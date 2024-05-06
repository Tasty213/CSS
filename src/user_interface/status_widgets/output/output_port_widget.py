from PySide6 import QtWidgets


class OutputPortWidget(QtWidgets.QLabel):
    def __init__(self, port_name: str, parent=None):
        self._state = 0
        self.port_name = port_name
        label_text = self.generate_label_text()
        super(OutputPortWidget, self).__init__(label_text, parent)

        self.move(100, 100)
        self.resize(80, 80)
        self.setStyleSheet("border: 3px solid blue; border-radius: 40px;")

    @property
    def state(self):
        return self._state

    def set_state(self, value):
        self.state = value

    def generate_label_text(self):
        raise NotImplementedError()
