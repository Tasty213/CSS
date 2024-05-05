from ports.input.digital.digital_input import DigitalInput


class DistanceSensor(DigitalInput):
    @property
    def state(self):
        if self.enabled.state and self.power_supply.state >= 20:
            return self.environment.distance
        else:
            return 0
