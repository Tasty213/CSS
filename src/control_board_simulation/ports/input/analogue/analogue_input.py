from abc import abstractmethod
from control_board_simulation.environment import Environment
from control_board_simulation.ports.output.analogue_output import AnalogueOutput
from control_board_simulation.ports.output.digital_output import DigitalOutput
from control_board_simulation.ports.port import Port


class AnalogueInput(Port):
    def __init__(
        self,
        environment: Environment,
        enabled: DigitalOutput,
        power_supply: AnalogueOutput,
    ):
        self.environment = environment
        self.enabled = enabled
        self.power_supply = power_supply
        super().__init__()

    @property
    @abstractmethod
    def state(self) -> int:
        pass

    @state.setter
    def state(self, value):
        raise NotImplementedError()
