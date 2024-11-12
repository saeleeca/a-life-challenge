from models import Organism, PassiveOrganism
import random


class FungiOrganism(Organism):
    def __init__(self, genome, row, col, world, generation, species):
        super().__init__(genome, row, col, world, generation, species)

        # Set custom values for the Passive.
        self._reproduction_energy_expenditure = 5
        self._base_energy_expenditure = 2
        self._food_energy = 5
        self._food_type = PassiveOrganism
        self._reproduction_ratio = 2

    def move(self, row: int, col: int) -> None:
        """Fungi organisms do not move. Overwrites parent organism."""
        pass

    def eat(self, food: 'Organism') -> None:
        """Increases energy when consuming passive organisms."""
        self._energy += food.get_food_energy()  # Gain the energy of the food
        self._world.kill_organism(food._row, food._col)  # Remove the food from the world

    def passive_check_neighbors(self, row: int, col: int):
        """Function to check if a cell is occupied. Takes the row and column coordinates and returns count.
        The returned count is used in determining if an organism lives/dies/reproduces.
        """
        ROWS, COLS = self._world.ROWS, self._world.COLS
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
        ROWS, COLS = self._world.ROWS, self._world.COLS

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

        # Reproduction occurs in found empty cells that can reproduce depending on reproduction rate
        # Check reproduction rate
        if random.random() < self._genome.get_reproduction_rate():
            while array_count < len(empty_cells):
                self.reproduce(empty_cells[array_count][0],empty_cells[array_count][1])
                array_count += 1
        return array_count

    def energy_reduction(self):
        """Passive Organism stored energy declines intermittently. Currently based on hardcoded rate"""
        if random.random() < 0.5:
            self._energy -= max(1, 1+self._world.get_environment().get_energy_rate())
        return

    def choose_action(self):
        """Herbivore checks adjacent cells for passive organisms, eats if found,
        moves if no food, and dies if out of energy."""

        # Step 1: Check adjacent cells for food
        food_found, food_row, food_col = self._world.get_adjacent_food(self._row, self._col, self._food_type)

        if food_found:
            # Step 2: Eat the food if found
            self.eat(self._world.get_cell(food_row, food_col))

            # Step 3: Calculate baseline energy loss. Die if out of energy.
        self._energy -= self._base_energy_expenditure
        if self._energy <= 0:
            self._world.kill_organism(self._row, self._col)

        # Step 4: Check if sufficient energy and space to reproduce
        self.check_reproduction()

    # def check_if_can_reproduce(self) -> bool:
    #     empty_found, empty_row, empty_col = self._world.get_empty_neighbor(self._row, self._col, True)
    #     if (self._energy >= (self._reproduction_ratio * self._genome.get_max_energy()) and empty_found):
    #         self.reproduce(empty_row, empty_col)