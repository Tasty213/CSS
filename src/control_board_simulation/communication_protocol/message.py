import re


class Message:
    SEQUENCE_NUMBER_REGEX = r"^\d+$"

    @staticmethod
    def parse_sequence_number(number: str):
        if re.match(Message.SEQUENCE_NUMBER_REGEX, number):
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
