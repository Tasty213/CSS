from command import Command
from control_codes import ControlCodes
from port_direction import PortDirection
from port_type import PortType
from power_state import PowerState


class ControlBoard:
    def __init__(
        self, digital_inputs=2, analogue_inputs=2, digital_outputs=2, analogue_outputs=2
    ):
        self.ports = {
            PortType.ANALOGUE: {
                PortDirection.INPUT: [0 for _ in list(range(0, analogue_inputs))],
                PortDirection.OUTPUT: [0 for _ in list(range(0, analogue_outputs))],
            },
            PortType.DIGITAL: {
                PortDirection.INPUT: [0 for _ in list(range(0, digital_inputs))],
                PortDirection.OUTPUT: [0 for _ in list(range(0, digital_outputs))],
            },
        }
        self.power_state = PowerState.OFF

    def submit_command(self, command: str):
        try:
            parsed_command = Command(command)
        except ValueError:
            return "^ERR\n"

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

    def echo(self, command: Command):
        return f"^E {command.sequence_number} OK_ {self.power_state}\n"

    def power(self, command: Command):
        match command.arguments[0]:
            case "0":
                self.power_state = PowerState.OFF
            case "1":
                self.power_state = PowerState.ON

        return f"^{ControlCodes.POWER} {command.sequence_number} OK_\n"

    def input(self, command: Command):
        port_type = command.arguments[0][0]
        port_direction = command.arguments[0][1]
        port_address_hex = command.arguments[0][2:4]
        port_address = int(port_address_hex, base=16)

        try:
            sensor_value = self.get_value_from_input_or_output(
                port_direction, port_type, port_address
            )
        except IndexError:
            return f"^{ControlCodes.INPUT} {command.sequence_number} RNG\n"

        return f"^{ControlCodes.INPUT} {command.sequence_number} OK_ {port_type}{port_direction}{port_address_hex} {sensor_value}\n"

    def output(self, command: Command):
        port_type = command.arguments[0][0]
        port_address_hex = command.arguments[0][2:4]
        port_address = int(port_address_hex, base=16)
        value_to_set = command.arguments[1]

        try:
            self.set_output_value(port_type, port_address, value_to_set)
        except IndexError:
            return f"^{ControlCodes.OUTPUT} {command.sequence_number} RNG\n"

        return f"^{ControlCodes.OUTPUT} {command.sequence_number} OK_\n"

    def get_value_from_input_or_output(self, port_direction, port_type, port_address):
        sensor_value = self.ports.get(port_type).get(port_direction)[port_address]

        if port_type == PortType.ANALOGUE:
            sensor_value = f"{sensor_value:#0{10}x}"[2:]

        return sensor_value

    def set_output_value(self, port_type, port_address, value):
        if port_type == PortType.ANALOGUE:
            value = int(value, base=16)
        self.ports.get(port_type).get(PortDirection.OUTPUT)[port_address] = value
