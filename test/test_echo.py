import pytest

from control_board import ControlBoard


def test_echo_with_power_off(control_board_off: ControlBoard):
    response = control_board_off.submit_command("^E 00\n")

    assert response == "^E 00 OK_ OFF\n"


def test_echo_with_power_on(control_board_on: ControlBoard):
    response = control_board_on.submit_command("^E 01\n")

    assert response == "^E 01 OK_ ON\n"


def test_echo_errors_without_carret(control_board_off: ControlBoard):
    assert control_board_off.submit_command("E 01\n") == "^ERR\n"


def test_echo_errors_without_newline(control_board_off: ControlBoard):
    assert control_board_off.submit_command("^E 01") == "^ERR\n"


@pytest.mark.parametrize(
    "input_code,expected_output",
    [
        ("^E 01\n", "^E 01 OK_ OFF\n"),
        ("^E 02\n", "^E 02 OK_ OFF\n"),
        ("^E 03\n", "^E 03 OK_ OFF\n"),
    ],
)
def test_copies_sequence_number(
    control_board_off: ControlBoard, input_code, expected_output
):
    assert control_board_off.submit_command(input_code) == expected_output


def test_invalid_sequence_number_returns_error(control_board_off: ControlBoard):
    assert control_board_off.submit_command("E \n") == "^ERR\n"
