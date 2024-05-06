from control_board_simulation.communication_protocol.command import Command
from control_board_simulation.communication_protocol.response import Response
from control_board_simulation.control_codes import ControlCodes
from control_board_simulation.environment import Environment
from control_board_simulation.port_direction import PortDirection
from control_board_simulation.port_type import PortType
from control_board_simulation.ports.input.analogue.distance_sensor import DistanceSensor
from control_board_simulation.ports.input.analogue.light_level_sensor import (
    LightLevelSensor,
)
from control_board_simulation.ports.input.digital.light_sensor import LightSensor
from control_board_simulation.ports.input.digital.motion_sensor import MotionSensor
from control_board_simulation.ports.output.analogue_output import AnalogueOutput
from control_board_simulation.ports.output.digital_output import DigitalOutput
from control_board_simulation.ports.port import Port
from control_board_simulation.power_state import PowerState
from control_board_simulation.status_code import StatusCode


class ControlBoard:
    def __init__(
        self,
        environment: Environment,
    ):
        self.environment = environment
        digital_outputs = [
            DigitalOutput(),
            DigitalOutput(),
            DigitalOutput(),
            DigitalOutput(),
        ]
        analogue_outputs = [
            AnalogueOutput(),
            AnalogueOutput(),
            AnalogueOutput(),
            AnalogueOutput(),
        ]
        self.ports = {
            PortType.ANALOGUE: {
                PortDirection.INPUT: [
                    LightLevelSensor(
                        environment, digital_outputs[2], analogue_outputs[2]
                    ),
                    DistanceSensor(
                        environment, digital_outputs[3], analogue_outputs[3]
                    ),
                ],
                PortDirection.OUTPUT: analogue_outputs,
            },
            PortType.DIGITAL: {
                PortDirection.INPUT: [
                    LightSensor(environment, digital_outputs[0], analogue_outputs[0]),
                    MotionSensor(environment, digital_outputs[1], analogue_outputs[1]),
                ],
                PortDirection.OUTPUT: digital_outputs,
            },
        }
        self.power_state = PowerState.OFF

    def submit_command(self, command: str) -> str:
        try:
            parsed_command = Command.from_command(command)
        except ValueError:
            return f"^{StatusCode.ERROR}\n"

        match parsed_command.control_code:
            case ControlCodes.ECHO:
                return self.echo(parsed_command)
            case ControlCodes.POWER:
                return self.power(parsed_command)
            case ControlCodes.INPUT:
                return self.input(parsed_command)
            case ControlCodes.OUTPUT:
                return self.output(parsed_command)
            case _:
                raise ValueError(
                    f"Unimplemented Control Code {parsed_command.control_code}"
                )

    def echo(self, command: Command) -> Response:
        response = Response(
            sequence_number=command.sequence_number,
            control_code=command.control_code,
            status_code=StatusCode.OK,
            arguments=[self.power_state],
        )
        return str(response)

    def power(self, command: Command) -> Response:
        match command.arguments[0]:
            case "0":
                self.power_state = PowerState.OFF
                for output in self.ports.get(PortType.DIGITAL).get(
                    PortDirection.OUTPUT
                ):
                    output.state = "0"
            case "1":
                self.power_state = PowerState.ON

        response = Response(
            sequence_number=command.sequence_number,
            control_code=ControlCodes.POWER,
            status_code=StatusCode.OK,
            arguments=[],
        )

        return str(response)

    def input(self, command: Command) -> Response:
        port_type = command.arguments[0][0]
        port_direction = command.arguments[0][1]
        port_address_hex = command.arguments[0][2:4]
        port_address = int(port_address_hex, base=16)

        try:
            sensor_value = self.get_value_from_input_or_output(
                port_direction, port_type, port_address
            )
            response = Response(
                sequence_number=command.sequence_number,
                control_code=ControlCodes.INPUT,
                status_code=StatusCode.OK,
                arguments=[
                    f"{port_type}{port_direction}{port_address_hex}",
                    sensor_value,
                ],
            )
        except IndexError:
            response = Response(
                sequence_number=command.sequence_number,
                control_code=ControlCodes.INPUT,
                status_code=StatusCode.RANGE,
                arguments=[],
            )

        return str(response)

    def output(self, command: Command) -> Response:
        port_type = command.arguments[0][0]
        port_address_hex = command.arguments[0][2:4]
        port_address = int(port_address_hex, base=16)
        value_to_set = command.arguments[1]

        try:
            self.set_output_value(port_type, port_address, value_to_set)
            response = Response(
                sequence_number=command.sequence_number,
                control_code=ControlCodes.OUTPUT,
                status_code=StatusCode.OK,
                arguments=[],
            )
        except IndexError:
            response = Response(
                sequence_number=command.sequence_number,
                control_code=ControlCodes.OUTPUT,
                status_code=StatusCode.RANGE,
                arguments=[],
            )

        return str(response)

    def get_value_from_input_or_output(self, port_direction, port_type, port_address):
        sensor_value = self.ports.get(port_type).get(port_direction)[port_address]

        if isinstance(sensor_value, Port):
            sensor_value = sensor_value.state

        if port_type == PortType.ANALOGUE:
            sensor_value = f"{sensor_value:#0{10}x}"[2:]

        return sensor_value

    def set_output_value(self, port_type, port_address, value):
        port = self.ports.get(port_type).get(PortDirection.OUTPUT)[port_address]
        port.state = value
