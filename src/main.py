from control_board import ControlBoard


if __name__ == "__main__":
    control_board = ControlBoard()

    while True:
        command = input("Enter command: ") + "\n"
        result = control_board.submit_command(command)
        print(result)
