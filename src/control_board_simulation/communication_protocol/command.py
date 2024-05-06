from dataclasses import dataclass
from control_board_simulation.control_codes import ControlCodes
from control_board_simulation.communication_protocol.message import Message


@dataclass
class Command(Message):
    SEQUENCE_NUMBER_REGEX = r"^\d+$"
    control_code: ControlCodes
    sequence_number: int
    arguments: list[str]

    @staticmethod
    def from_command(command: str):
        Message.validate(command)
        command = Message.remove_control_characters(command)
        components = command.split(" ")
        control_code = ControlCodes(components[0])
        sequence_number = components[1]

        if len(components) > 2:
            arguments = components[2:]
        else:
            arguments = []

        return Command(
            control_code=control_code,
            sequence_number=sequence_number,
            arguments=arguments,
        )
