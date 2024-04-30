import pytest

from control_board import ControlBoard


@pytest.fixture
def controll_board_off():
    return ControlBoard()


@pytest.fixture
def controll_board_on(controll_board_off: ControlBoard):
    controll_board_off.submit_command("P 00 1")
    return ControlBoard()
