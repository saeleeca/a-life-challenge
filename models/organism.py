from services.mutation_service import MutationService
class Organism:
    def __init__(self, genome, row: int, col: int, world, generation: int):
        self._genome = genome
        self._energy: int = self._genome.get_max_energy()
        self._row: int = row
        self._col: int = col
        self._world = world
        self._birthday: int = self._world.get_day()
        self._generation: int = generation

        self._mutation_service = MutationService()      # Singleton Instance
        # Custom / Organism-Specific Properties
        self._move_energy_expenditure = 1   # Energy spend moving
        self._food_energy = 1               # Energy given when eaten
        self._base_energy_expenditure = 1   # Baseline energy expended per turn
        self._food_type = None              # Food class if a consumer   
        self._reproduction_ratio = 1.0      # how much energy surplus energy needed to reproduce



    def move(self, row: int, col: int) -> None:
        """Updates the Organisms row and col"""
        if row == self._row and col == self._col:
            return
        self._world.move(self._row, self._col, row, col)
        self._energy -= self._move_energy_expenditure
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
    
    def get_food_energy(self) -> int:
        return self._food_energy

    def eat(self, food: 'Organism') -> None:
        """Consumes the food"""
        # This might work for herbivore/carnivore but not passive
        row, col = food.get_location()
        self._energy += food.get_energy()
        self._world.kill_organism(row, col)

    def reproduce(self, row: int, col: int) -> 'Organism':
        """Reproduces and returns the offspring if there are exactly 3 neighbors."""
        mutated_genome = self._mutation_service.mutate(self._genome)
        child_organism = self.__class__(mutated_genome, row, col, self._world,
                                        self._generation + 1)
        self._world.add_organism(child_organism, row, col)
        return child_organism

    def choose_action(self):
        """Depends on type of Organism"""
        pass

    def get_birthday(self) -> int:
        """Returns the birthday"""
        return self._birthday

    def get_data(self) -> dict:
        """Returns a dictionary with the data to be rendered in the UI"""
        return {
            "Age": self._world.get_day() - self._birthday,
            "Energy": self._energy,
            "Generation": self._generation
        }