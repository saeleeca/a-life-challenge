from models import CreatureType
from services.naming_service import OrganismNameGenerator


class Species:
    _naming_service = OrganismNameGenerator()
    _index = 0  # Tracks species index/ids internally
    def __init__(self, genome: 'Genome', day: int, world, parent_id: int=None):
        self._base_genome = genome
        self._name: str = self.generate_name()
        self._is_active: bool = True
        # Need a special condition for setting up the base species which
        # is done before creating any organisms
        if day == 0:
            self._population: int = 0
        else:
            self._population: int = 1
        self._max_population: int = self._population
        self._day_created: int = day
        self._day_extinct: int | None = None
        self._world = world
        self._id: int = Species._index   # Stores its index, used as parent_id when creating children species
        Species._index += 1
        self._parent_id: int | None = parent_id # Points to the index of its predecessor

    def get_id(self) -> int:
        """Returns the id"""
        return self._id

    @classmethod
    def reset(cls, new_index: int = 0):
        """Resets the class index. Used when resetting or loading a new game"""
        cls._index = new_index

    def get_predecessor_id(self) -> int:
        """Returns the parent_id, if it exists otherwise returns its own id"""
        return self._parent_id if self._parent_id is not None else self._id

    def generate_name(self) -> str:
        """Generates a name str using the naming service"""
        creature_type = self._base_genome.get_creature_type()
        if creature_type == CreatureType.CARNIVORE:
            return self._naming_service.generate_carnivore_name()
        elif creature_type == CreatureType.PASSIVE:
            return self._naming_service.generate_passive_name()
        else:
            return self._naming_service.generate_herbivore_name()

    def is_same_species(self, genome: 'Genome') -> bool:
        """Compares this base genome with genome and returns a bool"""
        if self._world.get_day() == 0:
            return True
        return self._base_genome.get_difference(genome) < .30 # 30% difference

    def inc_population(self):
        """Increases this species population, updating is_active and max pop"""
        if not self._is_active:
            self._is_active = True
        self._population += 1
        self._max_population = max(self._max_population, self._population)

    def dec_population(self):
        """Decreases this species population, updating is_active and day_extinct"""
        self._population -= 1
        if self._population == 0:
            self._is_active = False
            self._day_extinct = self._world.get_day()

    def get_name(self) -> str:
        """Returns the name"""
        return self._name

    def is_extinct(self) -> bool:
        """Returns is_extinct bool"""
        return self._is_active == False

    def get_data(self) -> dict:
        """Returns a dictionary with the data to be rendered in the UI"""
        if self._is_active:
            days_active = self._world.get_day() - self._day_created
        else:
            days_active = self._day_extinct - self._day_created

        return {
            "Name": self._name,
            "Status": "Active" if self._is_active else "Extinct",
            "Day Created": self._day_created,
            "Days Active": days_active,
            "Population": self._population,
            "Max Population": self._max_population,
            "Genome": self._base_genome.get_data()
        }
