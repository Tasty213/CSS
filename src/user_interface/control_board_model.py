from typing import Callable
from control_board_simulation.communication_protocol.command import Command
from control_board_simulation.control_codes import ControlCodes
from control_board_simulation.communication_protocol.response import Response
from control_board_simulation.status_code import StatusCode


class ControlBoardModel:
    def __init__(self, set_power_state: Callable):
        self.power_on = False
        self.set_power_state = set_power_state

    def update_model(self, command: str, response: str):
        parsed_command = Command.from_command(command)
        parsed_response = Response.from_control_board_response(response)

        match parsed_response.control_code:
            case ControlCodes.ECHO:
                pass
            case ControlCodes.POWER:
                self.update_power_state(parsed_command, parsed_response)
            case ControlCodes.INPUT:
                pass
            case ControlCodes.OUTPUT:
                pass
            case _:
                raise ValueError(
                    f"Unimplemented Control Code {parsed_response.control_code}"
                )

    def update_power_state(self, command: Command, response: Response):
        if response.status_code != StatusCode.OK:
            return
        elif command.arguments[0] == "0" and self.power_on:
            self.power_on = False
        elif command.arguments[0] == "1" and not self.power_on:
            self.power_on = True

        new_state = "Power On" if self.power_on else "Power Off"
        self.set_power_state(new_state)
