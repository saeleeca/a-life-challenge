from models import Organism


class MeteoriteObject(Organism):
    def __init__(self, genome, row, col, world, generation, species):
        super().__init__(genome, row, col, world, generation, species)

        # How many days the meteorites will stay on the field
        self._timer = 50


    def choose_action(self):
        """Timer function to remove meteorites when timer is up"""

        # Reduces the timer set until 0, then the meteorites disappear
        self._timer -= 1
        if self._timer <= 0:
            self._world.kill_organism(self._row, self._col)