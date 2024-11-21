from services.mutation_service import MutationService
import random
class Organism:
    def __init__(self, genome, row: int, col: int, world, generation: int,
                 species):
        self._genome = genome
        self._energy: int = self._genome.get_max_energy()
        self._row: int = row
        self._col: int = col
        self._world = world
        self._birthday: int = self._world.get_day()
        self._generation: int = generation
        self._species = species

        self._mutation_service = MutationService()      # Singleton Instance
        # Custom / Organism-Specific Properties
        self._move_energy_expenditure = self._genome.get_move_energy_expenditure()   # Energy spend moving
        self._reproduction_energy_expenditure = self._genome.get_reproduction_energy_expenditure()
        self._food_energy = self._genome.get_food_energy()               # Energy given when eaten
        self._base_energy_expenditure = self._genome.get_base_energy_expenditure()   # Baseline energy expended per turn
        self._food_type = self._genome.get_food_type()              # Food class if a consumer   
        self._reproduction_ratio = self._genome.get_reproduction_ratio()      # how much energy surplus energy needed to reproduce



    def move(self, row: int, col: int) -> None:
        """Updates the Organisms row and col"""
        if row == self._row and col == self._col:
            return
        self._world.move(self._row, self._col, row, col)
        self._energy -= self._move_energy_expenditure
        self._row = row
        self._col = col

    def random_move(self):
        """Move to a random adjacent empty cell."""
        empty_found, empty_row, empty_col = self._world.get_empty_neighbor(self._row, self._col, True)
        if empty_found:
            self.move(empty_row, empty_col)

    def get_genome(self):
        return self._genome

    def get_color(self):
        return self._genome.get_color()

    def get_energy(self) -> int:
        return self._energy

    def set_energy(self, energy: int):
        """Sets energy. Currently used by eat organism method in world to set energy of eaten organism"""
        self._energy = energy

    def get_location(self) -> (int, int):
        """Returns a tuple with the location (row, col)"""
        return self._row, self._col
    
    def get_food_energy(self) -> int:
        return self._food_energy

    def get_species(self) -> 'Species':
        return self._species

    def set_species(self, species: 'Species'):
        self._species = species

    def eat(self, food: 'Organism') -> None:
        """Increases energy when consuming organisms."""
        self._energy += food.get_food_energy()  # Gain the energy of the food
        #self._world.kill_organism(food._row, food._col)  # Remove the food from the world
        food_energy = food.get_food_energy()
        self._world.eat_organism(food._row, food._col, food_energy)

    def check_if_can_reproduce(self) -> bool:
        empty_found, empty_row, empty_col = self._world.get_empty_neighbor(self._row, self._col, True)
        if (self._energy >= (self._reproduction_ratio * self._genome.get_max_energy()) and empty_found):
            self.reproduce(empty_row, empty_col)

    def reproduce(self, row: int, col: int) -> 'Organism':
        """Reproduces and returns the offspring if there are exactly 3 neighbors."""
        mutated_genome = self._mutation_service.mutate(self._genome)
        child_organism = self.__class__(mutated_genome, row, col, self._world,
                                        self._generation + 1, self._species)
        self._world.add_organism(child_organism, row, col)
        self._world.add_offspring()
        self._world.update_max_generation(self._generation + 1)
        return child_organism

    def choose_action(self):
        """Depends on type of Organism"""
        pass

    def seek_food(self):
        """
        Move to an empty cell that will make food adjacent if possible.
        Returns True if a move was made, False otherwise.
        """
        potential_moves = []
        max_rows, max_cols = len(self._world.get_world()), len(self._world.get_world()[0])

        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            next_row, next_col = self._row + dr, self._col + dc

            if 0 <= next_row < max_rows and 0 <= next_col < max_cols:
                if self._world.is_cell_empty(next_row, next_col):
                    # Simulate moving to this cell and check for food
                    food_found, r, c = self._world.get_adjacent_food(next_row, next_col, self._food_type)
                    if food_found:
                        potential_moves.append((next_row, next_col))

        # If any potential moves bring food within reach, choose one
        if potential_moves:
            target_row, target_col = random.choice(potential_moves)
            self.move(target_row, target_col)
            return True

        return False  # No beneficial moves found


    def get_birthday(self) -> int:
        """Returns the birthday"""
        return self._birthday

    def get_data(self) -> dict:
        """Returns a dictionary with the data to be rendered in the UI"""
        return {
            "Age": self._world.get_day() - self._birthday,
            "Species": self._species.get_name(),
            "Energy": self._energy,
            "Generation": self._generation,
            "Genome": self._genome.get_data()
        }