from organism import Organism

class PassiveOrganism(Organism):
    def move(self, row: int, col: int, world) -> None:
        """Passive organisms do not move. Overwrites parent organism."""
        pass

    def eat(self, food: 'Organism', world) -> None:
        """Passive organisms do not eat. Overwrites parent organism."""
        pass

    def passive_check_neighbors(self):
        """Function to check if a cell is occupied. The returned count is used in determining if an organism
            lives/dies/reproduces."""
        from main import ROWS
        from main import COLS
        count = 0
        # upper left
        if (self._row + 1 in range(ROWS) and self._col - 1 in range(COLS) and
                isinstance(self._world.get_cell(self._row + 1 , self._col - 1), PassiveOrganism)):
            count += 1
        # upper mid
        if self._row + 1 in range(ROWS) and isinstance(self._world.get_cell(self._row + 1 , self._col), PassiveOrganism):
            count += 1
        # upper right
        if (self._row + 1 in range(ROWS) and self._col + 1 in range(COLS) and
                isinstance(self._world.get_cell(self._row + 1 , self._col + 1), PassiveOrganism)):
            count += 1
        # mid left
        if self._col - 1 in range(COLS) and isinstance(self._world.get_cell(self._row, self._col - 1), PassiveOrganism):
            count += 1
        # mid right
        if self._col + 1 in range(COLS) and isinstance(self._world.get_cell(self._row, self._col + 1), PassiveOrganism):
            count += 1
        # lower left
        if (self._row - 1 in range(ROWS) and self._col - 1 in range(COLS) and
                isinstance(self._world.get_cell(self._row - 1 , self._col - 1), PassiveOrganism)):
            count += 1
        # lower mid
        if (self._row - 1 in range(ROWS) and
                isinstance(self._world.get_cell(self._row - 1 , self._col), PassiveOrganism)):
            count += 1
        # lower right
        if (self._row - 1 in range(ROWS) and self._col + 1 in range(COLS) and
                isinstance(self._world.get_cell(self._row - 1 , self._col + 1), PassiveOrganism)):
            count += 1
        print(count)
        return count

    def reproduce(self, row: int, col: int) -> 'Organism':
        """Reproduces and returns the offspring if there are exactly 3 neighbors."""
        count = self.passive_check_neighbors()
        if count == 3:
            return self.__class__(self._genome.reproduce(), row, col)
        pass

    def choose_action(self):
        """Organism will die if it has less than 2 or greater than 3 neighbors."""
        count = self.passive_check_neighbors()

        # Any live cell with fewer than two live neighbours dies, as if by underpopulation
        if count < 2:
            self._world.kill_organism(self._row, self._col)
            # Any live cell with more than three live neighbours dies, as if by overpopulation
        elif count > 3:
            self._world.kill_organism(self._row, self._col)
            # Any live cell with two or three live neighbours lives on to the next generation
        else:
            pass





