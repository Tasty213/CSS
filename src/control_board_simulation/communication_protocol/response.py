from dataclasses import dataclass
from control_board_simulation.communication_protocol.message import Message
from control_board_simulation.control_codes import ControlCodes
from control_board_simulation.status_code import StatusCode


@dataclass
class Response(Message):
    sequence_number: int
    control_code: ControlCodes
    status_code: StatusCode
    arguments: list[str]

    @staticmethod
    def from_control_board_response(response: str):
        if response == "^ERR\n":
            return Response(
                sequence_number=0, control_code="", status_code=StatusCode.ERROR
            )

        response = Response.remove_control_characters(response)
        components = response.split(" ")

        control_code = ControlCodes(components[0])
        sequence_number = components[1]
        status_code = components[2]
        arguments = components[3:] if len(components) > 2 else []

        return Response(
            sequence_number=sequence_number,
            control_code=control_code,
            status_code=status_code,
            arguments=arguments,
        )

    def __str__(self):
        arguments = [str(argument) for argument in self.arguments]
        arguments = " " + " ".join(arguments) if len(arguments) > 0 else ""
        return f"^{self.control_code} {self.sequence_number} {self.status_code}{arguments}\n"
