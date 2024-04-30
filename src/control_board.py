class ControlBoard:
    def __init__(self):
        pass

    def submit_command(self, command: str):
        return self.echo(command)

    def echo(self, command: str):
        return "E 00 OK_ OFF"
