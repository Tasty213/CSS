from PySide6 import QtWidgets

from user_interface.status_widgets.output.analogue_output_port_widget import (
    AnalogueOutputPortWidget,
)
from user_interface.status_widgets.output.digital_output_port_widget import (
    DigitalOutputPortWidget,
)


class ControlBoxStatusWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ControlBoxStatusWidget, self).__init__(parent)
        layout = QtWidgets.QGridLayout()

        self.power_indicator = self.create_circle_label("Power Off")
        layout.addWidget(self.power_indicator, 0, 0)

        digital_outputs_layout = self.create_digital_outputs_layout()
        layout.addLayout(digital_outputs_layout, 1, 0)

        analogue_outputs_layout = self.create_analogue_outputs_layout()
        layout.addLayout(analogue_outputs_layout, 2, 0)

        self.setLayout(layout)

    def create_digital_outputs_layout(self):
        digital_outputs_layout = QtWidgets.QHBoxLayout()
        self.digital_outputs = [
            DigitalOutputPortWidget("Light Sensor"),
            DigitalOutputPortWidget("Motion Sensor"),
            DigitalOutputPortWidget("Light Level"),
            DigitalOutputPortWidget("Distance"),
        ]

        for digital_output in self.digital_outputs:
            digital_outputs_layout.addWidget(digital_output)

        return digital_outputs_layout

    def create_analogue_outputs_layout(self):
        analogue_outputs_layout = QtWidgets.QHBoxLayout()
        self.analogue_outputs = [
            AnalogueOutputPortWidget("Light Sensor"),
            AnalogueOutputPortWidget("Motion Sensor"),
            AnalogueOutputPortWidget("Light Level"),
            AnalogueOutputPortWidget("Distance"),
        ]

        for analogue_output in self.analogue_outputs:
            analogue_outputs_layout.addWidget(analogue_output)

        return analogue_outputs_layout

    def create_circle_label(self, text):
        label = QtWidgets.QLabel(text, self)
        label.move(100, 100)
        label.resize(80, 80)
        label.setStyleSheet("border: 3px solid blue; border-radius: 40px;")
        return label
