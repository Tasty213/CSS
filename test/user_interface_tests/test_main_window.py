from control_board_simulation.control_board import ControlBoard
from main_ui import Window
from pytestqt.qtbot import QtBot
from unittest.mock import MagicMock


def test_title(qtbot: QtBot, control_board_off: ControlBoard):
    window = Window(control_board_off)
    window.show()
    qtbot.addWidget(window)

    assert window.windowTitle() == "CSS Tech Test"


def test_submit_command_calls_control_box_simulation(
    qtbot: QtBot, control_board_off: ControlBoard
):
    control_board_off.submit_command = MagicMock(return_value="^ERR\n")
    window = Window(control_board_off)
    window.show()
    qtbot.addWidget(window)

    window.command_input_box.setText("test")
    window.send_command_button.click()

    control_board_off.submit_command.assert_called_once_with("test\n")
    assert window.command_input_box.placeholderText() == "Input command"
    assert window.command_input_box.text() == ""
    assert window.command_output_box.toPlainText() == "User: test\nControl: ^ERR"
