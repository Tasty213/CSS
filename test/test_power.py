from control_board import ControlBoard


def test_power_on(control_board_off: ControlBoard):
    assert control_board_off.submit_command("^P 00 1\n") == "^P 00 OK_\n"
    assert control_board_off.submit_command("^E 01\n") == "^E 01 OK_ ON\n"

    assert control_board_off.submit_command("^P 02 0\n") == "^P 02 OK_\n"
    assert control_board_off.submit_command("^E 03\n") == "^E 03 OK_ OFF\n"
