from command import Command
from control_codes import ControlCodes
from input_type import InputType
from power_state import PowerState


class ControlBoard:
    def __init__(self, digital_inputs=2, analogue_inputs=2):
        self.digital_inputs = [0 for _ in list(range(0, digital_inputs))]
        self.analogue_inputs = [0 for _ in list(range(0, analogue_inputs))]
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
        input_type = command.arguments[0][0]
        input_address_hex = command.arguments[0][1:3]
        input_address = int(input_address_hex, base=16)

        match input_type:
            case InputType.DIGITAL:
                sensor_value = self.digital_inputs[input_address]
            case InputType.ANALOGUE:
                sensor_value = self.analogue_inputs[input_address]
                sensor_value = f"{sensor_value:#0{10}x}"[2:]
            case _:
                raise ValueError("Unkown sensor type parsed")

        return f"^{ControlCodes.INPUT} {command.sequence_number} OK_ {input_type}{input_address_hex} {sensor_value}\n"
