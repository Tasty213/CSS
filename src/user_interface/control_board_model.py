from typing import Callable
from control_board_simulation.communication_protocol.command import Command
from control_board_simulation.control_codes import ControlCodes
from control_board_simulation.communication_protocol.response import Response
from control_board_simulation.port_direction import PortDirection
from control_board_simulation.port_type import PortType
from control_board_simulation.status_code import StatusCode


class ControlBoardModel:
    def __init__(
        self,
        set_power_state: Callable,
        set_light_sensor_state: Callable,
        set_motion_sensor_state: Callable,
        set_light_level_sensor_state: Callable,
        set_distance_sensor_state: Callable,
    ):
        self.power_on = False
        self.set_power_state = set_power_state
        self.set_light_sensor_state = set_light_sensor_state
        self.set_motion_sensor_state = set_motion_sensor_state
        self.set_light_level_sensor_state = set_light_level_sensor_state
        self.set_distance_sensor_state = set_distance_sensor_state

        self.ports = {
            PortType.DIGITAL: {
                PortDirection.OUTPUT: [
                    self.set_light_sensor_state,
                    self.set_motion_sensor_state,
                    self.set_light_level_sensor_state,
                    self.set_distance_sensor_state,
                ],
            },
        }

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
                self.update_output_state(parsed_command, parsed_response)
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

    def update_output_state(self, command: Command, response: Response):
        if response.status_code != StatusCode.OK:
            return
        port_type = command.arguments[0][0]
        port_address_hex = command.arguments[0][2:4]
        port_address = int(port_address_hex, base=16)
        value_to_set = command.arguments[1]
        set_output_value = self.ports.get(port_type).get(PortDirection.OUTPUT)[
            port_address
        ]

        set_output_value(value_to_set)
