from environments import Environment

class HarshEnvironment(Environment):
    def __init__(self, world):
        super().__init__('Harsh',0.004, 0.01, 0.02,
                         0.1, 0.01, 0.2,0.3,"white", world)
