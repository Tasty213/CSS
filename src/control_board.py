from command import Command
from control_codes import ControlCodes
from power_state import PowerState


class ControlBoard:
    def __init__(self):
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
