from models import Organism

class PassiveOrganism(Organism):
    def move(self, row: int, col: int) -> None:
        """Passive organisms do not move. Overwrites parent organism."""
        pass

    def eat(self, food: 'Organism') -> None:
        """Passive organisms do not eat. Overwrites parent organism."""
        pass

    def passive_check_neighbors(self, row: int, col: int):
        """Function to check if a cell is occupied. The returned count is used in determining if an organism
            lives/dies/reproduces."""
        from main import ROWS
        from main import COLS
        count = 0
        # upper left
        if (row + 1 in range(ROWS) and col - 1 in range(COLS) and
                isinstance(self._world.get_cell(row + 1 , col - 1), PassiveOrganism)):
            count += 1
        # upper mid
        if row + 1 in range(ROWS) and isinstance(self._world.get_cell(row + 1 , col), PassiveOrganism):
            count += 1
        # upper right
        if (row + 1 in range(ROWS) and col + 1 in range(COLS) and
                isinstance(self._world.get_cell(row + 1 , col + 1), PassiveOrganism)):
            count += 1
        # mid left
        if col - 1 in range(COLS) and isinstance(self._world.get_cell(row, col - 1), PassiveOrganism):
            count += 1
        # mid right
        if col + 1 in range(COLS) and isinstance(self._world.get_cell(row, col + 1), PassiveOrganism):
            count += 1
        # lower left
        if (row - 1 in range(ROWS) and col - 1 in range(COLS) and
                isinstance(self._world.get_cell(row - 1 , col - 1), PassiveOrganism)):
            count += 1
        # lower mid
        if (row - 1 in range(ROWS) and
                isinstance(self._world.get_cell(row - 1 , col), PassiveOrganism)):
            count += 1
        # lower right
        if (row - 1 in range(ROWS) and col + 1 in range(COLS) and
                isinstance(self._world.get_cell(row - 1 , col + 1), PassiveOrganism)):
            count += 1
        return count

    def reproduce(self, row: int, col: int) -> 'Organism':
        """Reproduces and returns the offspring if there are exactly 3 neighbors."""
        return self.__class__(self._genome.reproduce(), row, col, self._world)

    def check_reproduction(self):
        """Checks 8 neighboring cells around original organism for empty cells. If an empty cell is found
        reproduction conditions are checked and if valid, reproduce is called."""
        from main import ROWS
        from main import COLS
        # upper left
        if self._row + 1 in range(ROWS) and self._col - 1 in range(COLS) and self._world.is_cell_empty(self._row + 1, self._col - 1):
            count = self.passive_check_neighbors(self._row + 1, self._col - 1)
            if count == 3:
                self.reproduce(self._row + 1, self._col - 1)
        # upper mid
        if self._row + 1 in range(ROWS) and self._world.is_cell_empty(self._row + 1, self._col):
            count = self.passive_check_neighbors(self._row + 1, self._col)
            if count == 3:
                self.reproduce(self._row + 1, self._col)
        # upper right
        if self._row + 1 in range(ROWS) and self._col + 1 in range(COLS) and self._world.is_cell_empty(self._row + 1, self._col + 1):
            count = self.passive_check_neighbors(self._row + 1, self._col + 1)
            if count == 3:
                self.reproduce(self._row + 1, self._col + 1)
        # mid left
        if self._col - 1 in range(COLS) and self._world.is_cell_empty(self._row, self._col - 1):
            count = self.passive_check_neighbors(self._row, self._col - 1)
            if count == 3:
                self.reproduce(self._row, self._col - 1)
        # mid right
        if self._col + 1 in range(COLS) and self._world.is_cell_empty(self._row, self._col + 1):
            count = self.passive_check_neighbors(self._row, self._col + 1)
            if count == 3:
                self.reproduce(self._row, self._col + 1)
        # lower left
        if self._row - 1 in range(ROWS) and self._col - 1 in range(COLS) and self._world.is_cell_empty(self._row - 1, self._col - 1):
            count = self.passive_check_neighbors(self._row - 1, self._col - 1)
            if count == 3:
                self.reproduce(self._row - 1, self._col - 1)
        # lower mid
        if self._row - 1 in range(ROWS) and self._world.is_cell_empty(self._row - 1, self._col):
            count = self.passive_check_neighbors(self._row - 1, self._col)
            if count == 3:
                self.reproduce(self._row - 1, self._col)
        # lower right
        if self._row - 1 in range(ROWS) and self._col + 1 in range(COLS) and self._world.is_cell_empty(self._row - 1, self._col + 1):
            count = self.passive_check_neighbors(self._row - 1, self._col + 1)
            if count == 3:
                self.reproduce(self._row - 1, self._col + 1)
        return

    def choose_action(self):
        """Organism will die if it has less than 2 or greater than 3 neighbors."""
        count = self.passive_check_neighbors(self._row, self._col)

        # Any live cell with fewer than two live neighbours dies, as if by underpopulation
        if count < 2:
            self._world.kill_organism(self._row, self._col)
            # Any live cell with more than three live neighbours dies, as if by overpopulation
        elif count > 3:
            self._world.kill_organism(self._row, self._col)
            # Any live cell with two or three live neighbours lives on to the next generation
        self.check_reproduction()
