from environments import Environment

class DesertEnvironment(Environment):
    def __init__(self):
        super().__init__('Desert',0.01, 0.02, 0.04,
                         0.05, 0.1, 0.5,0.8, (235, 223, 120))
