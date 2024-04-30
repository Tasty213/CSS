from control_codes import ControlCodes


class Command:
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
