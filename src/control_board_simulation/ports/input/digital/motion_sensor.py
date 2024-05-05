from control_board_simulation.ports.input.digital.digital_input import DigitalInput


class MotionSensor(DigitalInput):
    @property
    def state(self):
        if self.enabled.state and self.power_supply.state >= 20:
            return int(self.environment.movement)
        else:
            return 0
