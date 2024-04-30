import pytest
from control_board import ControlBoard


@pytest.mark.parametrize(
    "input_code,expected_output",
    [
        ("^I 01 DI00\n", "^I 01 OK_ DI00 0\n"),
        ("^I 01 DI01\n", "^I 01 OK_ DI01 0\n"),
        ("^I 01 AI00\n", "^I 01 OK_ AI00 00000000\n"),
        ("^I 01 AI01\n", "^I 01 OK_ AI01 00000000\n"),
    ],
)
def test_get_input_value(control_board_on: ControlBoard, input_code, expected_output):
    assert control_board_on.submit_command(input_code) == expected_output


def test_get_input_value_after_change_digital(control_board_on: ControlBoard):
    control_board_on.digital_inputs[0] = 1
    assert control_board_on.submit_command("^I 01 DI00\n") == "^I 01 OK_ DI00 1\n"
    control_board_on.digital_inputs[0] = 0
    assert control_board_on.submit_command("^I 02 DI00\n") == "^I 02 OK_ DI00 0\n"


def test_get_input_value_after_change_analogue(control_board_on: ControlBoard):
    control_board_on.analogue_inputs[0] = 99545
    assert (
        control_board_on.submit_command("^I 01 AI00\n") == "^I 01 OK_ AI00 000184d9\n"
    )
    control_board_on.analogue_inputs[0] = 0
    assert (
        control_board_on.submit_command("^I 02 AI00\n") == "^I 02 OK_ AI00 00000000\n"
    )


@pytest.mark.parametrize(
    "input_code,expected_output",
    [
        ("^I 01 AI02\n", "^I 01 RNG\n"),
        ("^I 01 AI14\n", "^I 01 RNG\n"),
        ("^I 01 DI14\n", "^I 01 RNG\n"),
        ("^I 01 DI20\n", "^I 01 RNG\n"),
    ],
)
def test_get_out_of_range_input_analogue(
    control_board_on: ControlBoard, input_code, expected_output
):
    assert control_board_on.submit_command(input_code) == expected_output
