from abc import ABC, abstractmethod


class Port(ABC):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    @state.setter
    @abstractmethod
    def state(self, value):
        pass
