import pytest

from control_board_simulation.control_board import ControlBoard


@pytest.mark.parametrize(
    "command,expected",
    [
        ("^O 01 AO00 00000000\n", "^O 01 OK_\n"),
        ("^O 01 AO01 00000000\n", "^O 01 OK_\n"),
        ("^O 01 AO04 00000000\n", "^O 01 RNG\n"),
        ("^O 01 DO00 00000000\n", "^O 01 OK_\n"),
        ("^O 01 DO01 00000000\n", "^O 01 OK_\n"),
        ("^O 01 DO04 00000000\n", "^O 01 RNG\n"),
    ],
)
def test_ouput_returns_correct_response(
    control_board_on: ControlBoard, command, expected
):
    assert control_board_on.submit_command(command) == expected


@pytest.mark.parametrize(
    "address,value",
    [
        ("AO01", "00000000"),
        ("AO01", "000000ff"),
        ("AO01", "35aec24d"),
        ("AO01", "ffffffff"),
        ("AO00", "00000000"),
        ("AO00", "000000ff"),
        ("AO00", "35aec24d"),
        ("AO00", "ffffffff"),
    ],
)
def test_set_output(control_board_on: ControlBoard, address, value):
    control_board_on.submit_command(f"^O 01 {address} {value}\n")
    actual = control_board_on.submit_command(f"^I 02 {address}\n")

    assert actual == f"^I 02 OK_ {address} {value}\n"
