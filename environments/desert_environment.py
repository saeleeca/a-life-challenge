from environments import Environment

class DesertEnvironment(Environment):
    def __init__(self):
        super().__init__('Desert',0.001, 0.02, 0.04,
                         0.5, "yellow")
