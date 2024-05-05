from ports.input.digital_input import DigitalInput


class LightSensor(DigitalInput):
    @property
    def state(self):
        if self.power_supply.state:
            return int(self.environment.light)
        else:
            return 0
