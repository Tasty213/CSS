import pytest
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
    control_board_off.submit_command = MagicMock(return_value="^P 00 OK_\n")
    window = Window(control_board_off)
    window.show()
    qtbot.addWidget(window)

    window.command_input_box.setText("^P 00 1")
    window.send_command_button.click()

    control_board_off.submit_command.assert_called_once_with("^P 00 1\n")
    assert window.command_input_box.placeholderText() == "Input command"
    assert window.command_input_box.text() == ""
    assert (
        window.command_output_box.toPlainText() == "User: ^P 00 1\nControl: ^P 00 OK_"
    )


def test_power_indicator_defaults_off(qtbot: QtBot, control_board_off: ControlBoard):
    window = Window(control_board_off)
    window.show()
    qtbot.add_widget(window)

    assert window.control_box_status.power_indicator.text() == "Power Off"


def test_turning_on_box_switches_on_an_indicator(
    qtbot: QtBot, control_board_off: ControlBoard
):
    window = Window(control_board_off)
    window.show()
    qtbot.add_widget(window)

    window.command_input_box.setText("^P 00 1")
    window.send_command_button.click()

    assert window.control_box_status.power_indicator.text() == "Power On"

    window.command_input_box.setText("^P 00 1")
    window.send_command_button.click()

    assert window.control_box_status.power_indicator.text() == "Power On"

    window.command_input_box.setText("^P 00 0")
    window.send_command_button.click()

    assert window.control_box_status.power_indicator.text() == "Power Off"


@pytest.mark.parametrize(
    "address",
    [("00"), ("01"), ("02"), ("03")],
)
def test_turning_on_digital_output_switches_on_and_indicator(
    qtbot: QtBot, control_board_off: ControlBoard, address: str
):
    window = Window(control_board_off)
    window.show()
    qtbot.add_widget(window)

    window.command_input_box.setText("^P 00 1")
    window.send_command_button.click()
    window.command_input_box.setText(f"^O 01 DO{address} 1")
    window.send_command_button.click()

    assert "On" in window.control_box_status.digital_outputs[int(address)].text()


@pytest.mark.parametrize(
    "address",
    [("00"), ("01"), ("02"), ("03")],
)
def test_turning_on_analogue_output_adjusts_output(
    qtbot: QtBot, control_board_off: ControlBoard, address: str
):
    window = Window(control_board_off)
    window.show()
    qtbot.add_widget(window)

    window.command_input_box.setText("^P 00 1")
    window.send_command_button.click()
    window.command_input_box.setText(f"^O 01 AO{address} 000000FF")
    window.send_command_button.click()

    assert "25" in window.control_box_status.analogue_outputs[int(address)].text()


@pytest.mark.parametrize(
    "address",
    [(0), (1)],
)
def test_getting_analogue_input_plots_on_chart(
    qtbot: QtBot, control_board_off: ControlBoard, address: str
):
    window = Window(control_board_off)
    window.show()
    qtbot.add_widget(window)

    window.command_input_box.setText("^P 00 1")
    window.send_command_button.click()
    window.command_input_box.setText(f"^O 01 AO0{address + 2} 000000FF")
    window.send_command_button.click()
    window.command_input_box.setText(f"^O 01 DO0{address + 2} 1")
    window.send_command_button.click()
    window.command_input_box.setText(f"^I 01 AI0{address}")
    window.send_command_button.click()

    assert 0 in window.control_box_status.analogue_inputs[int(address)].y
