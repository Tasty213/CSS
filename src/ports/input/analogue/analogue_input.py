from abc import abstractmethod
from environment import Environment
from ports.output.analogue_output import AnalogueOutput
from ports.output.digital_output import DigitalOutput
from ports.port import Port


class DigitalInput(Port):
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
