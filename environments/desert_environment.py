from environments import Environment
import random

class DesertEnvironment(Environment):
    def __init__(self, world):
        super().__init__('Desert',0.03, 0.04, 0.06,
                         0.05, 0.1, 0.5,0.8, (235, 223, 120), world)
        self.last_weather_change_day = 0  # Keeps track of the last day the weather was changed
        self.weather_change_interval = random.randint(5,10)  # Choose random day to change the weather
        self.current_weather = self.desert_weather()  # Initialize with a random weather type

    def desert_weather(self):
        """Randomly select a weather type based on predefined probabilities. Returns a weather event as a string"""
        weather_event = random.choices(
            ['Normal', 'Extreme Heat'],  # Possible weather events
            weights=[0.7, 0.3],  # Corresponding probabilities for normal, rainy, and stormy
            k=1  # One event per change
        )[0]
        return weather_event

    def change_weather_if_needed(self):
        """Change the weather if it's time to do so. Returns the current weather."""
        current_day = self.get_day_enviro()  # Get the current day from the World instance

        # If enough days have passed since the last weather change
        if current_day >= self.last_weather_change_day + self.weather_change_interval:
            self.current_weather = self.desert_weather()  # Set a new weather type
            self.last_weather_change_day = current_day  # Update the last weather change day
            self.weather_change_interval = random.randint(10, 50)  # Pick a new random interval for the next change
        return self.current_weather

    def get_adjusted_max_energy(self, organism_mod):
        """Return the modifier, as a percentage, for all max energy. In normal weather the modifier stays the
        same for all organisms and in extreme heat all organisms suffer and can not gain as much energy and
        thus max energy is decreased.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Extreme Heat':
            adjusted_modifier = round(float(organism_mod * 0.5),4)
        else:
            adjusted_modifier = organism_mod

        # Return the max energy as an int based on grid size
        return adjusted_modifier

    def get_passive_max_energy(self):
        """Return the maximum energy for passive organisms based on grid size and weather."""
        adjusted_modifier = self.get_adjusted_max_energy(self._passive_max_energy_mod)
        return int(self._rows * self._cols * adjusted_modifier)

    def get_herbivore_max_energy(self):
        """Return the maximum energy for herbivore organisms based on grid size and weather."""
        adjusted_modifier = self.get_adjusted_max_energy(self._herbivore_max_energy_mod)
        return int(self._rows * self._cols * adjusted_modifier)

    def get_carnivore_max_energy(self):
        """Return the maximum energy for carnivore organisms based on grid size and weather."""
        adjusted_modifier = self.get_adjusted_max_energy(self._carnivore_max_energy_mod)
        return int(self._rows * self._cols * adjusted_modifier)

    def get_weather(self):
        """Return the current weather."""
        return self.current_weather