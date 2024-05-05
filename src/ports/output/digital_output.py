from ports.port import Port


class DigitalOutput(Port):
    def __init__(self):
        self._state = False
        super().__init__()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: str):
        if isinstance(value, str):
            self._state = value == "1"
        else:
            raise NotImplementedError()
