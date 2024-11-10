import random
from environments import Environment, NormalEnvironment, HarshEnvironment, DesertEnvironment, RainforestEnvironment

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
        self._environment: Environment = set_world_type()
        self._environment_type = Environment.get_environment_type(self._environment)
        self._passive_energy_mod = Environment.get_passive_max_energy_mod(self._environment)
        self._herbivore_energy_mod = Environment.get_herbivore_max_energy_mod(self._environment)
        self._carnivore_energy_mod = Environment.get_carnivore_max_energy_mod(self._environment)
        self._energy_rate = Environment.get_energy_rate(self._environment) # how much can be absorbed per cycle
        self._environment_color = Environment.get_environment_color(self._environment)
        self._day: int = 0

    def kill_organism(self, row: int, col: int) -> None:
        """Sets the row col to None"""
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

    def get_background_environment_color(self):
        """Gets background color of the environment"""
        return self._environment_color

    def get_energy_rate(self):
        """Gets energy rate based on the environment"""
        return self._energy_rate

    def get_environment_type(self):
        """Gets the type of environment"""
        return self._environment_type

    def inc_day(self):
        self._day += 1

    def get_day(self) -> int:
        return self._day

    def reset(self):
        """Resets the world"""
        self.__init__()

    def get_species_data(self) -> list:
        """Returns a list with the species data to be rendered in the UI"""
        # Hardcoded for now. Will use self._species once implemented
        return [
            {"Genome": {"Color": (255, 0, 0),
             "Creature Type": "Carnivore",
             "Max Energy": 500,
             "Can Move": "True"},
             "Status": "Active",
             "Population": 100,
             "Max Population": 390,
             "Day Created": 0,
             "Days Active": 360
             },
            {"Genome": {"Color": (0, 0, 255),
             "Creature Type": "Herbivore",
             "Max Energy": 500,
             "Can Move": "True"},
             "Status": "Active",
             "Population": 400,
             "Max Population": 600,
             "Day Created": 0,
             "Days Active": 360
             },
            {"Genome": {"Color": (0, 255, 0),
             "Creature Type": "Passive",
             "Max Energy": 500,
             "Can Move": "False"},
             "Status": "Active",
             "Population": 800,
             "Max Population": 1000,
             "Day Created": 0,
             "Days Active": 360
             }
        ]
