from control_board_simulation.control_board import ControlBoard
from control_board_simulation.environment import Environment

if __name__ == "__main__":
    environment = Environment(light=False, light_level=0, movement=False, distance=0)
    control_board = ControlBoard(environment)

    while True:
        command = input("Enter command: ") + "\n"
        result = control_board.submit_command(command)
        print(result)
