import random
from environments import NormalEnvironment, HarshEnvironment, DesertEnvironment, RainforestEnvironment
from models import Species


def set_world_type():
    val = random.randint(0, 20)
    if val < 8:
        return NormalEnvironment()
    elif val < 12:
        return HarshEnvironment()
    elif val < 16:
        return DesertEnvironment()
    else:
        return RainforestEnvironment()


class World:
    ROWS, COLS = 50, 50
    def __init__(self):
        self._world: list[list[object]] = \
            [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self._species: list[Species] = []
        self._environment = set_world_type()
        self._passive_energy_mod = self._environment.get_passive_max_energy_mod()
        self._herbivore_energy_mod = self._environment.get_herbivore_max_energy_mod()
        self._carnivore_energy_mod = self._environment.get_carnivore_max_energy_mod()
        self._day: int = 0
        self._population: int = 0
        self._deaths: int = 0
        self._offsprings: int = 0
        self._max_generation: int = 0

    def kill_organism(self, row: int, col: int) -> None:
        """Sets the row col to None"""
        organism = self._world[row][col]
        if organism:
            organism.get_species().dec_population()
            self._deaths += 1
            self._population -= 1
        self._world[row][col] = None

    def move(self, rowA: int, colA: int, rowB: int, colB: int) -> None:
        """Moves the organism from a to b"""
        if rowA == rowB and colA == colB:
            return
        self._world[rowB][colB] = self._world[rowA][colA]
        self._world[rowA][colA] = None

    def add_organism(self, organism, row: int, col :int) -> None:
        """Adds the organism to self._world"""
        self._world[row][col] = organism
        self._population += 1

        # Check if the organism is a new species
        parent_species = organism.get_species()
        genome = organism.get_genome()
        if self._day != 0 and not parent_species.is_same_species(genome):
            # Different species from parent, but first check other
            # species before creating a new one
            for species in self._species:
                if species == parent_species:
                    continue
                # Found another species that it belongs to so add it there and increase population statistics
                if species.is_same_species(genome):
                    organism.set_species(species)
                    species.inc_population()
                    return

            # Doesn't belong to any existing species, so create a new one
            new_species = Species(genome, self._day, self)
            self._species.append(new_species)
            organism.set_species(new_species)
        else:
            # Not a new species, so just update population
            parent_species.inc_population()

    def is_cell_empty(self, row: int, col: int) -> bool:
        """Returns if the world contains an object at row, col"""
        return self._world[row][col] is None

    def get_cell(self, row: int, col: int):
        """Returns the object in the world at row, col"""
        return self._world[row][col]

    def get_world(self) -> list[list[object]]:
        """Returns the 2d world array"""
        return self._world

    def get_empty_neighbor(self, row: int, col: int, is_random: bool) -> (bool, int, int):
        """
        Returns either the first or a random empty neighbor cell if there is one
        bool- for if there is an empty neighbor, int for row, int for col
        """
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, -1), (1, 0), (1, 1)]

        if(is_random):
            random.shuffle(neighbors)

        for r, c in neighbors:
            check_row, check_col = r + row, c + col
            if (check_row < 0 or check_row >= len(self._world) or
                    check_col < 0 or check_col >= len(self._world[0])):
                continue

            if not self._world[check_row][check_col]:
                return True, check_row, check_col
        return False, 0, 0

    def get_adjacent_food(self, row: int, col: int, food_type) -> (bool, int, int):
            """Checks adjacent cells for the specified food type."""
            neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

            for dr, dc in neighbors:
                check_row, check_col = row + dr, col + dc

                # Check if within bounds and if cell contains the specified food type
                if (0 <= check_row < len(self._world) and 
                    0 <= check_col < len(self._world[0])):

                    cell = self.get_cell(check_row, check_col)
                    if isinstance(cell, food_type):
                        return True, check_row, check_col

            return False, 0, 0

    def get_world_max_passive_energy(self):
        """Gets maximum passive energy based on the environment."""
        return int(self.ROWS * self.COLS * self._passive_energy_mod)

    def get_world_max_herbivore_energy(self):
        """Gets maximum herbivore energy based on the environment."""
        return int(self.ROWS * self.COLS * self._herbivore_energy_mod)

    def get_world_max_carnivore_energy(self):
        """Gets maximum carnivore energy based on the environment."""
        return int(self.ROWS * self.COLS * self._carnivore_energy_mod)

    def get_environment(self):
        """Gets the environment"""
        return self._environment

    def inc_day(self):
        self._day += 1

    def get_day(self) -> int:
        return self._day

    def reset(self):
        """Resets the world"""
        self.__init__()

    def set_base_species(self, base_species: list[Species]):
        for species in base_species:
            self._species.append(species)

    def get_species_data(self, index) -> dict:
        """Returns a list with the species data to be rendered in the UI"""
        index = index % len(self._species)
        return self._species[index].get_data()

    def get_data(self) -> dict:
        """Returns a dictionary with the data to be rendered in the UI"""
        return {
            "Days": self._day,
            "Population": self._population,
            "Deaths": self._deaths,
            "No. of Species": len(self._species),
            "No. of mutations": 7,
            "Total Offspring": self._offsprings,
            "Generations (max)": self._max_generation,
            "World Type": self.get_environment().get_environment_type()
        }

    def add_offspring(self):
        """Increments the counter for total offspring produced"""
        self._offsprings += 1

    def update_max_generation(self, generation):
        """Updates the current max generation of all species"""
        self._max_generation = max(self._max_generation, generation)