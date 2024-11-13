from models import Organism, PassiveOrganism
import random


class FungiOrganism(Organism):
    def __init__(self, genome, row, col, world, generation, species):
        super().__init__(genome, row, col, world, generation, species)

        # Set custom values for the Fungi.
        self._reproduction_energy_expenditure = 5
        self._base_energy_expenditure = 1.0
        self._food_energy = 5
        self._food_type = PassiveOrganism
        self._reproduction_ratio = 2
        # self._genome.set_creature_type() = 4

    def move(self, row: int, col: int) -> None:
        """Fungi organisms do not move. Overwrites parent organism."""
        pass

    def eat(self, food: 'Organism') -> None:
        """Increases energy when consuming passive organisms."""
        self._energy += food.get_food_energy()  # Gain the energy of the food
        self._world.kill_organism(food._row, food._col)  # Remove the food from the world

    def check_if_can_reproduce(self) -> bool:
        """Fungi Organism checks for empty neighbors and uses the ratio and energy to determine reproduction"""
        empty_found, empty_row, empty_col = self._world.get_empty_neighbor(self._row, self._col, True)
        if (self._energy >= (self._reproduction_ratio * self._genome.get_max_energy()) and empty_found):
            self.reproduce(empty_row, empty_col)

    def energy_absorption(self):
        """Fungi Organisms can only gain energy by consumption"""
        pass

    def energy_reduction(self):
        """Fungi Organism stored energy declines intermittently. Currently based on hardcoded rate"""
        if random.random() < 0.5:
            self._energy -= max(1, 1+self._world.get_environment().get_energy_rate())
        return

    def choose_action(self):
        """Fungi checks adjacent cells for passive organisms, eats if found,
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
        self.check_if_can_reproduce()