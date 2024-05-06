from PySide6 import QtWidgets

from user_interface.output_port_widget import OutputPortWidget


class ControlBoxStatusWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ControlBoxStatusWidget, self).__init__(parent)
        layout = QtWidgets.QGridLayout()

        digital_outputs_layout = QtWidgets.QHBoxLayout()
        self.digital_outputs = [
            OutputPortWidget("Light Sensor"),
            OutputPortWidget("Motion Sensor"),
            OutputPortWidget("Light Level"),
            OutputPortWidget("Distance"),
        ]

        for digital_output in self.digital_outputs:
            digital_outputs_layout.addWidget(digital_output)

        layout.addLayout(digital_outputs_layout, 0, 0)
        self.setLayout(layout)

    def create_circle_label(self, text):
        label = QtWidgets.QLabel(text, self)
        label.move(100, 100)
        label.resize(80, 80)
        label.setStyleSheet("border: 3px solid blue; border-radius: 40px;")
        return label
