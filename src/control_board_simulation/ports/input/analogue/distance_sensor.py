from control_board_simulation.ports.input.analogue.analogue_input import AnalogueInput


class DistanceSensor(AnalogueInput):
    @property
    def state(self):
        if self.enabled.state and self.power_supply.state >= 20:
            return self.environment.distance
        else:
            return 0
