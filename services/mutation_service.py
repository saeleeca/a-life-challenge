import random
from models import Genome, CreatureType

class MutationService:  
    # Set Up Singleton Implementation
    _instance = None
    # Tracks current mutation rates
    _mutation_rates = {
        'color': 0.1,
        'max_energy': 0.1,
        'can_move': 0.001,
        'creature_type': 0.00001,
        'move_energy_expenditure': 0.05,
        'food_energy': 0.05,
        'base_energy_expenditure': 0.05,
        'reproduction_ratio': 0.05,
        'can_seek_food': 0.05,
        'can_hibernate': 0.1,
        'can_panic': 0.03
    }
    # Default mutation rates
    _mutation_starting_rates = _mutation_rates.copy()

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        """
        if not cls._instance:
            cls._instance = super(MutationService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.mutation_strategies = {
            'color': self._mutate_color,
            'max_energy': self._mutate_max_energy,
            'can_move': self._mutate_can_move,
            'creature_type': self._mutate_creature_type,
            'move_energy_expenditure': self._mutate_move_energy_expenditure,
            'food_energy': self._mutate_food_energy,
            'base_energy_expenditure': self._mutate_base_energy_expenditure,
            'reproduction_ratio': self._mutate_reproduction_ratio,
            'can_seek_food': self._mutate_can_seek_food,
            'can_hibernate': self._mutate_hibernate,
            'can_panic': self._mutate_panic
        }

        self.mutation_rates : dict = MutationService._mutation_rates

    def mutate(self, genome: Genome) -> Genome:
        """
        Perform mutations on a given genome. 
        Returns a new Genome instance with possible mutations.
        """
        new_genome = genome.__class__(
            color=genome.get_color(),
            creature_type=genome.get_creature_type(),
            max_energy=genome.get_max_energy(),
            can_move=genome.get_can_move(),
            reproduction_rate=genome.get_reproduction_rate(),
            reproduction_energy_expenditure=genome.get_reproduction_energy_expenditure(),
            move_energy_expenditure=genome.get_move_energy_expenditure(),
            base_energy_expenditure=genome.get_base_energy_expenditure(),
            food_energy=genome.get_food_energy(),
            food_type=genome.get_food_type(),
            reproduction_ratio=genome.get_reproduction_ratio(),
            can_seek_food=genome.get_can_seek_food()
        )

        for attribute, mutation_strategy in self.mutation_strategies.items():
            if random.random() < self.mutation_rates[attribute]:
                mutation_strategy(new_genome)

        return new_genome

    def _mutate_color(self, genome: Genome):
        """Mutates color by changing one of the RGB components randomly."""
        color = list(genome.get_color())
        for i in range(3):
            if random.random() < 0.33: 
                color[i] = min(255, max(0, color[i] + random.randint(-35, 35)))
        genome._color = tuple(color)

    def _mutate_max_energy(self, genome: Genome):
        """Mutates max_energy by adding a small random value."""
        max_energy = genome.get_max_energy()
        mutation = random.randint(-5, 5)
        genome._max_energy = max(1, max_energy + mutation)  # Ensure energy remains positive

    def _mutate_can_move(self, genome: Genome):
        """ Mutates the can_move attribute, toggling it."""
        genome._can_move = not genome.get_can_move()

    def _mutate_creature_type(self, genome: Genome):
        """Mutates the creature_type attribute, potentially changing the type of creature it is!"""
        possible_types = [creature for creature in CreatureType if creature != genome.get_creature_type()]
        new_type = random.choice(possible_types)
        genome._creature_type = new_type

    def _mutate_move_energy_expenditure(self, genome: Genome):
        """Mutates move_energy_expenditure by adding a small random value."""
        move_energy_expenditure = genome.get_move_energy_expenditure()
        mutation = random.randint(-1, 1)
        genome._move_energy_expenditure = max(1, move_energy_expenditure + mutation)

    def _mutate_food_energy(self, genome: Genome):
        """Mutates food_energy by adding a small random value."""
        food_energy = genome.get_food_energy()
        mutation = random.randint(-2, 2)
        genome._food_energy = max(1, food_energy + mutation)

    def _mutate_base_energy_expenditure(self, genome: Genome):
        """Mutates base_energy_expenditure by adding a small random value."""
        base_energy_expenditure = genome.get_base_energy_expenditure()
        mutation = random.randint(-1, 1)
        genome._base_energy_expenditure = max(1.0, base_energy_expenditure + mutation)

    def _mutate_reproduction_ratio(self, genome: Genome):
        """Mutates reproduction_ratio by adding a small random value."""
        reproduction_ratio = genome.get_reproduction_ratio()
        mutation = random.uniform(-0.1, 0.1)
        genome._reproduction_ratio = max(1.1, reproduction_ratio + mutation)

    def _mutate_can_seek_food(self, genome: Genome):
        """Mutates the can_seek_food attribute by flipping bool."""
        genome._can_seek_food = not genome._can_seek_food

    def _mutate_hibernate(self, genome: Genome):
        """Mutates the hibernate trait by flipping bool if panic is not already enabled"""
        if genome.get_can_panic():
            return  # Mutually exclusive
        genome._can_hibernate = not genome.get_can_hibernate()

    def _mutate_panic(self, genome: Genome):
        """Mutates the panic trait by flipping bool if hibernate is not already enabled."""
        if genome.get_can_hibernate():
            return  # Mutually exclusive
        genome._can_panic = not genome.get_can_panic()

    @classmethod
    def mutation_rate_modifier(cls, multiplier):
        """ Changes current mutation rates based on slider modifier"""
        for mutation_type in cls._mutation_rates:
            cls._mutation_rates[mutation_type] = cls._mutation_starting_rates[mutation_type] * multiplier