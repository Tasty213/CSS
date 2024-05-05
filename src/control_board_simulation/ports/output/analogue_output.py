from control_board_simulation.ports.port import Port


class AnalogueOutput(Port):
    def __init__(self):
        self._state = 0
        super().__init__()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: str):
        if isinstance(value, str):
            self._state = int(value, base=16)
        else:
            raise NotImplementedError()
