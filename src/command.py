import re
from control_codes import ControlCodes


class Command:
    SEQUENCE_NUMBER_REGEX = r"^\d+$"

    def __init__(self, command: str):
        self.validate(command)
        command = self.remove_control_characters(command)
        components = command.split(" ")
        self.control_code = ControlCodes(components[0])
        self.sequence_number = components[1]

        if len(components) > 2:
            self.arguments = components[2:]
        else:
            self.arguments = None

    def parse_control_number(self, number: str):
        if re.match(self.SEQUENCE_NUMBER_REGEX, number):
            return int(number)
        else:
            raise ValueError("Sequence number does not match regex ")

    @staticmethod
    def validate(command: str):
        if not command.startswith("^"):
            raise ValueError("Command does not start with '^'")
        elif not command.endswith("\n"):
            raise ValueError("Command does not end with '\\n'")

    @staticmethod
    def remove_control_characters(command: str):
        command = command.removeprefix("^")
        return command.removesuffix("\n")
