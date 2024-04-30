import pytest
from control_board import ControlBoard


@pytest.mark.parametrize(
    "input_code,expected_output",
    [
        ("^I 01 D00\n", "^I 01 OK_ D00 0\n"),
        ("^I 01 D01\n", "^I 01 OK_ D01 0\n"),
        ("^I 01 A00\n", "^I 01 OK_ A00 00000000\n"),
        ("^I 01 A01\n", "^I 01 OK_ A01 00000000\n"),
    ],
)
def test_get_input_value(control_board_on: ControlBoard, input_code, expected_output):
    assert control_board_on.submit_command(input_code) == expected_output


def test_get_input_value_after_change_digital(control_board_on: ControlBoard):
    control_board_on.digital_inputs[0] = 1
    assert control_board_on.submit_command("^I 01 D00\n") == "^I 01 OK_ D00 1\n"
    control_board_on.digital_inputs[0] = 0
    assert control_board_on.submit_command("^I 02 D00\n") == "^I 02 OK_ D00 0\n"


def test_get_input_value_after_change_analogue(control_board_on: ControlBoard):
    control_board_on.analogue_inputs[0] = 99545
    assert control_board_on.submit_command("^I 01 A00\n") == "^I 01 OK_ A00 000184d9\n"
    control_board_on.analogue_inputs[0] = 0
    assert control_board_on.submit_command("^I 02 A00\n") == "^I 02 OK_ A00 00000000\n"
