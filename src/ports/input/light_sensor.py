from ports.input.digital_input import DigitalInput


class LightSensor(DigitalInput):
    @property
    def state(self):
        if self.enabled.state and self.power_supply.state >= 20:
            return int(self.environment.light)
        else:
            return 0
