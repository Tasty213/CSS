import pytest

from control_board import ControlBoard
from environment import Environment


@pytest.fixture
def control_board_off():
    return ControlBoard(Environment(light=False, movement=False))


@pytest.fixture
def control_board_on(control_board_off: ControlBoard):
    control_board_off.submit_command("^P 00 1\n")
    return control_board_off
