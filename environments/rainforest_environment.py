from environments import Environment

class RainforestEnvironment(Environment):
    def __init__(self):
        super().__init__('Rainforest', 0.008, 0.02, 0.02,
                         1.2, 1.0, 1.0,1.0,(159, 196, 166))
