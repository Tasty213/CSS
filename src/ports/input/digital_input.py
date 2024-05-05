from abc import abstractmethod
from environment import Environment
from ports.output.digital_output import DigitalOutput
from ports.port import Port


class DigitalInput(Port):
    def __init__(self, environment: Environment, powerSupply: DigitalOutput):
        self.environment = environment
        self.power_supply = powerSupply
        super().__init__()

    @property
    @abstractmethod
    def state(self) -> int:
        pass

    @state.setter
    def state(self, value):
        raise NotImplementedError()
