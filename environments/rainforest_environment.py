from environments import Environment
import random


class RainforestEnvironment(Environment):
    def __init__(self, world):
        super().__init__('Rainforest', 0.008, 0.02, 0.02,
                         1.2, 1.0, 1.0,1.0,(159, 196, 166), world)
        self.last_weather_change_day = 0  # Keeps track of the last day the weather was changed
        self.weather_change_interval = random.randint(10,50)  # Choose random day to change the weather
        self.current_weather = self.rainforest_weather()  # Initialize with a random weather type

    def rainforest_weather(self):
        """Randomly select a weather type based on predefined probabilities. Returns a weather event as a string"""
        weather_event = random.choices(
            ['Normal', 'Rainy', 'Stormy'],  # Possible weather events
            weights=[0.5, 0.3, 0.2],  # Corresponding probabilities for normal, rainy, and stormy
            k=1  # One event per change
        )[0]
        return weather_event

    def change_weather_if_needed(self):
        """Change the weather if it's time to do so. Returns the current weather."""
        current_day = self.get_day_enviro()  # Get the current day from the World instance

        # If enough days have passed since the last weather change
        if current_day >= self.last_weather_change_day + self.weather_change_interval:
            self.current_weather = self.rainforest_weather()  # Set a new weather type
            self.last_weather_change_day = current_day  # Update the last weather change day
            self.weather_change_interval = random.randint(10, 50)  # Pick a new random interval for the next change
        return self.current_weather

    def get_passive_max_energy(self):
        """Return the maximum energy for passive organisms based on grid size and weather.
        In normal weather the modifier stays the same.
        In rainy weather the passive organism thrives more so its corresponding energy is increased and in stormy
        weather the passive can not gain as much energy and thus its max energy is decreased.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Rainy':
            adjusted_modifier = round(float(self._passive_max_energy_mod * 1.1),4)
        elif self.current_weather == 'Stormy':
            adjusted_modifier = round(float(self._passive_max_energy_mod * 0.9),4)
        else:
            adjusted_modifier = self._passive_max_energy_mod

        # Return the max energy as an int based on grid size
        return int(self._rows * self._cols * adjusted_modifier)

    def get_herbivore_max_energy(self):
        """Return the maximum energy for herbivore organisms based on grid size and weather.
        In normal and rainy weather the modifier stays the same but in stormy weather herbivores find it more
        difficult to venture out to find plants and the max energy they can have decreases.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Stormy':
            adjusted_modifier = round(float(self._herbivore_max_energy_mod * 0.7),4)
        else:
            adjusted_modifier = self._herbivore_max_energy_mod

        # Return the max energy as an int based on grid size
        return int(self._rows * self._cols * adjusted_modifier)

    def get_carnivore_max_energy(self):
        """Return the maximum energy for carnivore organisms based on grid size and weather.
        In normal weather the modifier stays the same but in stormy and rainy weather carnivores find it
        more difficult to venture out to find herbivores and the max energy they can have decreases.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Normal':
            adjusted_modifier = self._herbivore_max_energy_mod
        else:
            adjusted_modifier = round(float(self._herbivore_max_energy_mod * 0.7),4)

        # Return the max energy as an int based on grid size
        return int(self._rows * self._cols * adjusted_modifier)

    def get_weather(self):
        """Return the current weather."""
        return self.current_weather