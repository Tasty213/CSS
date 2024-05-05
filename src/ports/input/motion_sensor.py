from ports.input.digital_input import DigitalInput


class MotionSensor(DigitalInput):
    @property
    def state(self):
        if self.power_supply.state:
            return int(self.environment.movement)
        else:
            return 0
