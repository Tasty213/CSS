from user_interface.status_widgets.output.output_port_widget import OutputPortWidget


class AnalogueOutputPortWidget(OutputPortWidget):
    def generate_label_text(self):
        return f"{self.port_name} {self.state}"

    @OutputPortWidget.state.setter
    def state(self, value):
        self._state = int(value, base=16)
        self.setText(self.generate_label_text())
