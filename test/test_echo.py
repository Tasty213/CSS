import pytest


def test_echo_with_power_off(controll_board_off):
    response = controll_board_off.submit_command("^E 00\n")

    assert response == "E 00 OK_ OFF"


def test_echo_with_power_on(controll_board_on):
    response = controll_board_on.submit_command("^E 01\n")

    assert response == "E 01 OK_ ON"


def test_echo_errors_without_carret(controll_board_off):
    with pytest.raises(ValueError):
        controll_board_off.submit_command("E 01\n")


def test_echo_errors_without_newline(controll_board_off):
    with pytest.raises(ValueError):
        controll_board_off.submit_command("^E 01")
