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

    @state.setter
    def state(self, value):
        self._state = value
        self.setText(self.generate_label_text())

    def set_state(self, value):
        self.state = int(value)

    def generate_label_text(self):
        return f"{self.port_name} {"On" if self.state == 1 else "Off"}"
