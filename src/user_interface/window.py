from PySide6 import QtWidgets

from control_board_simulation.control_board import ControlBoard


class Window(QtWidgets.QDialog):
    def __init__(self, control_board: ControlBoard, parent=None):
        super(Window, self).__init__(parent)

        self.control_board = control_board
        self.setWindowTitle("CSS Tech Test")
        self.resize(500, 300)
        self.send_command_button = self.create_button("Send Command", self.send_command)
        self.command_input_box = self.create_line_edit("Input command")
        self.command_output_box = QtWidgets.QTextBrowser()

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.command_output_box, 0, 0)
        mainLayout.addWidget(self.command_input_box, 1, 0)
        mainLayout.addWidget(self.send_command_button, 1, 1)

        self.setLayout(mainLayout)

    def send_command(self):
        input_command = self.command_input_box.text()
        self.command_input_box.clear()
        self.command_output_box.append(f"User: {input_command}")
        output = self.control_board.submit_command(input_command + "\n")
        output_without_newline = output.replace("\n", "")
        self.command_output_box.append(f"Control: {output_without_newline}")

    def create_button(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def create_line_edit(self, placeholder_text=""):
        text_box = QtWidgets.QLineEdit()
        text_box.setPlaceholderText(placeholder_text)
        return text_box
