import random
from environments import NormalEnvironment, HarshEnvironment, DesertEnvironment, RainforestEnvironment
from models import Species, CreatureType

def set_world_type(world):
    """Sets the type of environment for the simulation"""
    val = random.randint(0, 20)
    if val < 8:
        return NormalEnvironment(world)
    elif val < 12:
        return HarshEnvironment(world)
    elif val < 16:
        return DesertEnvironment(world)
    else:
        return RainforestEnvironment(world)


class World:
    ROWS, COLS = 50, 50
    def __init__(self):
        self._world: list[list[object]] = \
            [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self._species: list[Species] = []
        # used to store filtered species list when requested. resets
        # to None if active_species changes
        self._active_species_list = None
        self._environment = set_world_type(self)
        self._day: int = 0
        self._active_species = 0
        self._population: int = 0
        self._deaths: int = 0
        self._offsprings: int = 0
        self._max_generation: int = 0

    def kill_organism(self, row: int, col: int) -> None:
        """Sets the row col to None"""
        organism = self._world[row][col]
        if organism and organism.get_genome().get_creature_type() != CreatureType.OBJECT:
            organism.get_species().dec_population()
            self._deaths += 1
            self._population -= 1
            if organism.get_species().is_extinct():
                self._active_species -= 1
                self._active_species_list = None
        self._world[row][col] = None

    def eat_organism(self, row: int, col: int, food_energy) -> None:
        """Reduces organism energy by the amount of food energy gained by predator and kills it if energy is 0 or
        less. Also rounds energy values."""
        organism = self._world[row][col]
        if organism:
            energy = round(organism.get_energy(),4)
            energy -= food_energy
            energy = round(energy,4)
            if energy <= 0:
                self.kill_organism(row, col)
            else:
                organism.set_energy(energy)


    def move(self, rowA: int, colA: int, rowB: int, colB: int) -> None:
        """Moves the organism from a to b"""
        if rowA == rowB and colA == colB:
            return
        self._world[rowB][colB] = self._world[rowA][colA]
        self._world[rowA][colA] = None

    def add_organism(self, organism, row: int, col :int) -> None:
        """Adds the organism to self._world"""

        self._world[row][col] = organism
        if organism.get_genome().get_creature_type() == CreatureType.OBJECT: return
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
                # Found another species that it belongs to so add it there
                if species.is_same_species(genome):
                    organism.set_species(species)
                    # Organism is added to an extinct species that now becomes
                    # active
                    if species.is_extinct():
                        self._active_species += 1
                        self._active_species_list = None
                    species.inc_population()
                    return
            # Doesn't belong to any existing species, so create a new one
            new_species = Species(genome, self._day, self, parent_species.get_id())
            self._species.append(new_species)
            organism.set_species(new_species)
            self._active_species += 1   # new species always increases active
            self._active_species_list = None
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

    def get_environment(self):
        """Gets the environment"""
        return self._environment

    def inc_day(self):
        """Increments the day"""
        self._day += 1

    def get_day(self) -> int:
        """Returns the day"""
        return self._day

    def reset(self):
        """Resets the world"""
        self.__init__()
        Species.reset()

    def load(self):
        """Additional step needed to set Species _index after new World load"""
        Species.reset(len(self._species))

    def set_base_species(self, base_species: list[Species]):
        """Additional step needed before game starts, called from setup_life"""
        for species in base_species:
            self._species.append(species)
        self._active_species = len(base_species)

    def get_species_data(self, index: int, filter_active: bool) -> dict:
        """Returns the species dict to be rendered in the UI"""
        if filter_active:
            if not self._active_species_list:
                self._active_species_list = [s for s in self._species
                                             if not s.is_extinct()]
            # Make sure there are active species, otherwise return {}
            # (don't need to check this for non-filtered list because there
            # should always be base species in the list)
            if len(self._active_species_list):
                index = index % len(self._active_species_list)
                return self._active_species_list[index].get_data()
            return {}
        index = index % len(self._species)
        return self._species[index].get_data()

    def get_data(self) -> dict:
        """Returns a dictionary with the data to be rendered in the UI"""
        return {
            "Days": self._day,
            "Population": self._population,
            "Deaths": self._deaths,
            "No. of Species Total": len(self._species),
            "No. of Species Active": self._active_species,
            "Total Offspring": self._offsprings,
            "Generations (max)": self._max_generation,
            "World Type": self.get_environment().get_environment_type(),
            "Weather": self.get_environment().get_weather()
        }

    def add_offspring(self):
        """Increments the counter for total offspring produced"""
        self._offsprings += 1

    def update_max_generation(self, generation):
        """Updates the current max generation of all species"""
        self._max_generation = max(self._max_generation, generation)