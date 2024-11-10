class Species:
    def __init__(self, genome: 'Genome', day: int, world):
        self._base_genome = genome
        self._name = self.generate_name()
        self._is_active = True
        # Need a special condition for setting up the base species which
        # is done before creating any organisms
        if day == 0:
            self._population = 0
        else:
            self._population = 1
        self._max_population = 0
        self._day_created = day
        self._day_extinct = None
        self._world = world

    def generate_name(self) -> str:
        return "Species Name"

    def is_same_species(self, genome: 'Genome') -> bool:
        if self._world.get_day() == 0:
            return True
        return self._base_genome.get_similarity(genome) > 0

    def inc_population(self):
        self._population += 1
        self._max_population = max(self._max_population, self._population)

    def dec_population(self):
        self._population -= 1
        if self._population == 0:
            self._is_active = False
            self._day_extinct = self._world.get_day()

    def get_name(self):
        return self._name

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