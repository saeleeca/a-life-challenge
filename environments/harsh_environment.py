from environments import Environment

class HarshEnvironment(Environment):
    def __init__(self):
        super().__init__('Harsh',0.004, 0.01, 0.02,
                         0.1, "white")
