import pytest
from control_board import ControlBoard
from port_direction import PortDirection
from port_type import PortType


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


@pytest.mark.parametrize(
    "address",
    [("00"), ("01")],
)
def test_sensors_need_power(control_board_off: ControlBoard, address):
    control_board_off.environment.light = True
    control_board_off.environment.movement = True
    assert (
        control_board_off.submit_command(f"^I 01 DI{address}\n")
        == f"^I 01 OK_ DI{address} 0\n"
    )
    control_board_off.submit_command("^P 00 1\n")
    control_board_off.submit_command(f"^O 01 DO{address} 1\n")
    assert (
        control_board_off.submit_command(f"^I 01 DI{address}\n")
        == f"^I 01 OK_ DI{address} 0\n"
    )
    control_board_off.submit_command(f"^O 01 AO{address} 00000014\n")
    assert (
        control_board_off.submit_command(f"^I 01 DI{address}\n")
        == f"^I 01 OK_ DI{address} 1\n"
    )
    control_board_off.submit_command("^P 00 0\n")
    assert (
        control_board_off.submit_command(f"^I 01 DI{address}\n")
        == f"^I 01 OK_ DI{address} 0\n"
    )


@pytest.mark.parametrize(
    "address,power_level,expected",
    [
        ("00", "00000014", "1"),
        ("00", "00000013", "0"),
        ("00", "00000015", "1"),
        ("00", "FFFFFFFF", "1"),
        ("00", "00000000", "0"),
    ],
)
def test_sensors_need_enough_power(
    control_board_on: ControlBoard, address, power_level, expected
):
    control_board_on.environment.light = True
    control_board_on.environment.movement = True
    control_board_on.submit_command(f"^O 01 DO{address} 1\n")
    control_board_on.submit_command(f"^O 01 AO{address} {power_level}\n")
    assert (
        control_board_on.submit_command(f"^I 01 DI{address}\n")
        == f"^I 01 OK_ DI{address} {expected}\n"
    )


def test_get_input_value_after_change_digital(control_board_on: ControlBoard):
    control_board_on.ports.get(PortType.DIGITAL).get(PortDirection.INPUT)[0] = 1
    assert control_board_on.submit_command("^I 01 DI00\n") == "^I 01 OK_ DI00 1\n"
    control_board_on.ports.get(PortType.DIGITAL).get(PortDirection.INPUT)[0] = 0
    assert control_board_on.submit_command("^I 02 DI00\n") == "^I 02 OK_ DI00 0\n"


def test_get_input_value_after_change_analogue(control_board_on: ControlBoard):
    control_board_on.environment.light_level = 99545
    control_board_on.submit_command("^O 01 DO00 1\n")
    control_board_on.submit_command("^O 01 AO00 00000014\n")
    assert (
        control_board_on.submit_command("^I 01 AI00\n") == "^I 01 OK_ AI00 000184d9\n"
    )
    control_board_on.environment.light_level = 0
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
