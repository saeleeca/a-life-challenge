class Organism:
    def __init__(self, genome, row: int, col: int):
        self._genome = genome
        self._energy: int = self._genome.get_max_energy()
        self._row: int = row
        self._col: int = col

    def move(self, row: int, col: int, world) -> None:
        """Updates the Organisms row and col"""
        if row == self._row and col == self._col:
            return
        world.move(self._row, self._col, row, col)
        self._energy -= 1
        self._row = row
        self._col = col

    def get_genome(self):
        return self._genome

    def get_color(self):
        return self._genome.get_color()

    def get_energy(self) -> int:
        return self._energy

    def get_location(self) -> (int, int):
        """Returns a tuple with the location (row, col)"""
        return self._row, self._col

    def eat(self, food: 'Organism', world) -> None:
        """Consumes the food"""
        # This might work for herbivore/carnivore but not passive
        row, col = food.get_location()
        self._energy += food.get_energy()
        world.kill_organism(row, col)

    def reproduce(self, row: int, col: int) -> 'Organism':
        """Reproduces and returns the offspring"""
        return self.__class__(self._genome.reproduce(), row, col)

    def choose_action(self, world):
        """Depends on type of Organism"""
        pass