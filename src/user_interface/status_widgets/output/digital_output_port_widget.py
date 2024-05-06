from user_interface.status_widgets.output.output_port_widget import OutputPortWidget


class DigitalOutputPortWidget(OutputPortWidget):
    def generate_label_text(self):
        return f"{self.port_name} {"On" if self.state == 1 else "Off"}"

    @OutputPortWidget.state.setter
    def state(self, value):
        self._state = int(value)
        self.setText(self.generate_label_text())
