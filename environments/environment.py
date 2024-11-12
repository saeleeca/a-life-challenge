class Environment:
    def __init__(self, environment_type: str, passive_max_energy_mod: float, herbivore_max_energy_mod: float,
                 carnivore_max_energy_mod: float, fungi_max_energy_mod: float, energy_rate_mod: float, passive_reproduction_rate_mod:float,
                 herbivore_reproduction_rate_mod, carnivore_reproduction_rate_mod, fungi_reproduction_rate_mod, color):
        self._environment_type = environment_type
        self._passive_max_energy_mod = passive_max_energy_mod
        self._herbivore_max_energy_mod = herbivore_max_energy_mod
        self._carnivore_max_energy_mod = carnivore_max_energy_mod
        self._fungi_max_energy_mod = fungi_max_energy_mod
        self._energy_rate_mod = energy_rate_mod
        self._passive_reproduction_rate_mod = passive_reproduction_rate_mod
        self._herbivore_reproduction_rate_mod = herbivore_reproduction_rate_mod
        self._carnivore_reproduction_rate_mod = carnivore_reproduction_rate_mod
        self._fungi_reproduction_rate_mod = fungi_reproduction_rate_mod
        self._color = color

    def get_environment_type(self):
        """Return the type of environment."""
        return self._environment_type

    def get_passive_max_energy_mod(self):
        """Return the modifier, as a percentage, for passive max energy."""
        return self._passive_max_energy_mod

    def get_herbivore_max_energy_mod(self):
        """Return the modifier, as a percentage, for herbivore max energy."""
        return self._herbivore_max_energy_mod

    def get_carnivore_max_energy_mod(self):
        """Return the modifier, as a percentage, for carnivore max energy."""
        return self._carnivore_max_energy_mod

    def get_fungi_max_energy_mod(self):
        """Return the modifier, as a percentage, for fungi max energy."""
        return self._fungi_max_energy_mod

    def get_energy_rate_mod(self):
        """Return the modifier, as a percentage, for energy rate."""
        return self._energy_rate_mod

    def get_environment_color(self):
        """Return the color of the environment."""
        return self._color

    def get_energy_rate(self):
        """Return the energy rate of the environment based on the modification."""
        return int(10 * self._energy_rate_mod)

    def get_passive_reproduction_rate_mod(self):
        """Return the passive reproduction rate modifier of the environment."""
        return self._passive_reproduction_rate_mod

    def get_herbivore_reproduction_rate_mod(self):
        """Return the herbivore reproduction rate modifier of the environment."""
        return self._herbivore_reproduction_rate_mod

    def get_carnivore_reproduction_rate_mod(self):
        """Return the carnivore reproduction rate modifier of the environment."""
        return self._carnivore_reproduction_rate_mod

    def get_fungi_reproduction_rate_mod(self):
        """Return the fungi reproduction rate modifier of the environment."""
        return self._fungi_reproduction_rate_mod