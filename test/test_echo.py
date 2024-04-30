def test_echo_with_power_off(controll_board_off):
    response = controll_board_off.submit_command("E 00")

    assert response == "E 00 OK_ OFF"


def test_echo_with_power_on(controll_board_on):
    response = controll_board_on.submit_command("E 01")

    assert response == "E 00 OK_ ON"
