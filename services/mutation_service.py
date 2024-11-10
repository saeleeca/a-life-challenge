import random
from models import Genome, CreatureType

class MutationService:  
    # Set Up Singleton Implementation
    _instance = None
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
            'creature_type': self._mutate_creature_type
        }

        self.mutation_rates = {
            'color': 0.1,
            'max_energy': 0.1,
            'can_move': 0.001,
            'creature_type': 0.00001
        }

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
            reproduction_rate=genome.get_reproduction_rate()
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
