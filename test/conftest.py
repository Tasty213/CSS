import pytest

from control_board_simulation.control_board import ControlBoard
from control_board_simulation.environment import Environment


@pytest.fixture
def control_board_off():
    return ControlBoard(
        Environment(light=False, light_level=0, movement=False, distance=0)
    )


@pytest.fixture
def control_board_on(control_board_off: ControlBoard):
    control_board_off.submit_command("^P 00 1\n")
    return control_board_off
