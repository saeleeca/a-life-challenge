from models import Organism
from world import World

class PassiveOrganism(Organism):
    def __init__(self, genome, row, col, world):
        super().__init__(genome, row, col, world)

        # Set custom values for the Passive.
        self._reproduction_energy_expenditure = 3
        self._food_energy = 5

    def move(self, row: int, col: int) -> None:
        """Passive organisms do not move. Overwrites parent organism."""
        pass

    def eat(self, food: 'Organism') -> None:
        """Passive organisms do not eat. Overwrites parent organism."""
        pass

    def passive_check_neighbors(self, row: int, col: int):
        """Function to check if a cell is occupied. Takes the row and column coordinates and returns count.
        The returned count is used in determining if an organism lives/dies/reproduces.
        """
        ROWS, COLS = World.ROWS, World.COLS
        count = 0

        # Check each neighbor cell for passive organism
        # Upper left
        if (row + 1 in range(ROWS) and col - 1 in range(COLS) and
                isinstance(self._world.get_cell(row + 1 , col - 1), PassiveOrganism)):
            count += 1

        # Upper mid
        if row + 1 in range(ROWS) and isinstance(self._world.get_cell(row + 1 , col), PassiveOrganism):
            count += 1

        # Upper right
        if (row + 1 in range(ROWS) and col + 1 in range(COLS) and
                isinstance(self._world.get_cell(row + 1 , col + 1), PassiveOrganism)):
            count += 1

        # Mid left
        if col - 1 in range(COLS) and isinstance(self._world.get_cell(row, col - 1), PassiveOrganism):
            count += 1

        # Mid right
        if col + 1 in range(COLS) and isinstance(self._world.get_cell(row, col + 1), PassiveOrganism):
            count += 1

        # Lower left
        if (row - 1 in range(ROWS) and col - 1 in range(COLS) and
                isinstance(self._world.get_cell(row - 1 , col - 1), PassiveOrganism)):
            count += 1

        # Lower mid
        if (row - 1 in range(ROWS) and
                isinstance(self._world.get_cell(row - 1 , col), PassiveOrganism)):
            count += 1

        # Lower right
        if (row - 1 in range(ROWS) and col + 1 in range(COLS) and
                isinstance(self._world.get_cell(row - 1 , col + 1), PassiveOrganism)):
            count += 1
        return count

    def check_reproduction(self):
        """Checks 8 neighboring cells around original organism for empty cells. If an empty cell is found
        reproduction conditions are checked and if valid, reproduce is called."""
        ROWS, COLS = World.ROWS, World.COLS

        # Store coordinates of empty cells before reproducing
        empty_cells = []
        array_count = 0

        # Check each neighbor cell for an empty cell. If empty, check if reproduction is allowed.
        # If reproduction is allowed store the coordinates
        # Upper left
        if (self._row + 1 in range(ROWS) and self._col - 1 in range(COLS) and
                self._world.is_cell_empty(self._row + 1, self._col - 1)):
            count = self.passive_check_neighbors(self._row + 1, self._col - 1)
            if count == 3:
                empty_cells.append((self._row + 1, self._col - 1))

        # Upper mid
        if self._row + 1 in range(ROWS) and self._world.is_cell_empty(self._row + 1, self._col):
            count = self.passive_check_neighbors(self._row + 1, self._col)
            if count == 3:
                empty_cells.append((self._row + 1, self._col))

        # Upper right
        if (self._row + 1 in range(ROWS) and self._col + 1 in range(COLS) and
                self._world.is_cell_empty(self._row + 1, self._col + 1)):
            count = self.passive_check_neighbors(self._row + 1, self._col + 1)
            if count == 3:
                empty_cells.append((self._row + 1, self._col + 1))

        # Mid left
        if self._col - 1 in range(COLS) and self._world.is_cell_empty(self._row, self._col - 1):
            count = self.passive_check_neighbors(self._row, self._col - 1)
            if count == 3:
                empty_cells.append((self._row, self._col - 1))

        # Mid right
        if self._col + 1 in range(COLS) and self._world.is_cell_empty(self._row, self._col + 1):
            count = self.passive_check_neighbors(self._row, self._col + 1)
            if count == 3:
                empty_cells.append((self._row, self._col + 1))

        # Lower left
        if (self._row - 1 in range(ROWS) and self._col - 1 in range(COLS) and
                self._world.is_cell_empty(self._row - 1, self._col - 1)):
            count = self.passive_check_neighbors(self._row - 1, self._col - 1)
            if count == 3:
                empty_cells.append((self._row - 1, self._col - 1))

        # Lower mid
        if self._row - 1 in range(ROWS) and self._world.is_cell_empty(self._row - 1, self._col):
            count = self.passive_check_neighbors(self._row - 1, self._col)
            if count == 3:
                empty_cells.append((self._row - 1, self._col))

        # Lower right
        if (self._row - 1 in range(ROWS) and self._col + 1 in range(COLS) and
                self._world.is_cell_empty(self._row - 1, self._col + 1)):
            count = self.passive_check_neighbors(self._row - 1, self._col + 1)
            if count == 3:
                empty_cells.append((self._row - 1, self._col + 1))

        # Reproduction occurs in found empty cells that can reproduce
        while array_count < len(empty_cells):
            self.reproduce(empty_cells[array_count][0],empty_cells[array_count][1])
            array_count += 1
        return array_count

    def choose_action(self):
        """Organism will die if it has less than 2 or greater than 3 neighbors."""

        # Count nearby passive neighbors to determine if death or reproduction can occur
        count = self.passive_check_neighbors(self._row, self._col)

        # Any live cell with fewer than two or greater than 3 live neighbours dies, as if by underpopulation
        if count < 2 or count > 3:
            self._world.kill_organism(self._row, self._col)

        # Any live cell with two or three live neighbours lives on to the next generation.
        # Passive organisms lose energy via reproduction and will die once at 0 or less energy.
        else:
            energy_expended = self.check_reproduction()
            energy_expended *= self._reproduction_energy_expenditure
            self._energy -= energy_expended
            if self._energy <= 0:
                self._world.kill_organism(self._row, self._col)

