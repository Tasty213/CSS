from PySide6 import QtWidgets

from control_board_simulation.control_board import ControlBoard
from user_interface.control_board_model import ControlBoardModel
from user_interface.control_box_status_bar import ControlBoxStatusWidget


class Window(QtWidgets.QDialog):
    def __init__(self, control_board: ControlBoard, parent=None):
        super(Window, self).__init__(parent)

        self.control_board = control_board
        self.setWindowTitle("CSS Tech Test")
        self.resize(500, 300)
        self.send_command_button = self.create_button("Send Command", self.send_command)
        self.command_input_box = self.create_line_edit("Input command")
        self.command_output_box = QtWidgets.QTextBrowser()

        self.control_box_status = ControlBoxStatusWidget()

        self.control_board_model = ControlBoardModel(
            self.control_box_status.power_indicator.setText,
            self.control_box_status.digital_outputs[0].set_state,
            self.control_box_status.digital_outputs[1].set_state,
            self.control_box_status.digital_outputs[2].set_state,
            self.control_box_status.digital_outputs[3].set_state,
        )

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.control_box_status, 0, 0)
        mainLayout.addWidget(self.command_output_box, 1, 0)
        mainLayout.addWidget(self.command_input_box, 2, 0)
        mainLayout.addWidget(self.send_command_button, 2, 1)

        self.setLayout(mainLayout)

    def send_command(self):
        input_command = self.command_input_box.text()
        self.command_input_box.clear()
        self.command_output_box.append(f"User: {input_command}")
        input_command_with_newline = input_command + "\n"

        output = self.control_board.submit_command(input_command_with_newline)
        output_without_newline = output.replace("\n", "")
        self.command_output_box.append(f"Control: {output_without_newline}")

        self.control_board_model.update_model(input_command_with_newline, output)

    def create_button(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def create_line_edit(self, placeholder_text=""):
        text_box = QtWidgets.QLineEdit()
        text_box.setPlaceholderText(placeholder_text)
        return text_box

    def create_circle_label(self, text):
        label = QtWidgets.QLabel(text, self)
        label.move(100, 100)
        label.resize(80, 80)
        label.setStyleSheet("border: 3px solid blue; border-radius: 40px;")
        return label
