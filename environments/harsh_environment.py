from environments import Environment
import random

class HarshEnvironment(Environment):
    def __init__(self, world):
        super().__init__('Harsh',0.004, 0.01, 0.02, 0.004,
                         0.1, 0.01, 0.2,0.3, 0.01,"white", world)
        self.last_weather_change_day = 0  # Keeps track of the last day the weather was changed
        self.weather_change_interval = random.randint(2,20)  # Choose random day to change the weather
        self.current_weather = self.harsh_weather()  # Initialize with a random weather type

    def harsh_weather(self):
        """Randomly select a weather type based on predefined probabilities. Returns a weather event as a string"""
        weather_event = random.choices(
            ['Harsh', 'Freezing', 'Cloudburst', 'Gale'],  # Possible weather events
            weights=[0.4, 0.2, 0.2, 0.2],  # Corresponding probabilities for normal, rainy, and stormy
            k=1  # One event per change
        )[0]
        return weather_event

    def change_weather_if_needed(self):
        """Change the weather if it's time to do so. Returns the current weather."""
        current_day = self.get_day_enviro()  # Get the current day from the World instance

        # If enough days have passed since the last weather change
        if current_day >= self.last_weather_change_day + self.weather_change_interval:
            self.current_weather = self.harsh_weather()  # Set a new weather type
            self.last_weather_change_day = current_day  # Update the last weather change day
            self.weather_change_interval = random.randint(2, 20)  # Pick a new random interval for the next change
        return self.current_weather

    def get_passive_max_energy(self):
        """Return the maximum energy for passive organisms based on grid size and weather.
        In normal harsh weather or gales the modifier stays the same.
        In cloudburst weather the passive organism thrives slightly more so its corresponding energy is increased
        In freezing weather the passive can not gain as much energy and thus its max energy is decreased.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Cloudburst':
            adjusted_modifier = round(float(self._passive_max_energy_mod * 1.1),4)
        elif self.current_weather == 'Freezing':
            adjusted_modifier = round(float(self._passive_max_energy_mod * 0.5),4)
        else:
            adjusted_modifier = self._passive_max_energy_mod

        # Return the max energy as an int based on grid size
        return int(self._rows * self._cols * adjusted_modifier)

    def get_herbivore_max_energy(self):
        """Return the maximum energy for herbivore organisms based on grid size and weather.
        In normal harsh weather the modifier stays the same.
        In all other weather the herbivore can not gain as much energy and thus its max energy is decreased.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Harsh':
            adjusted_modifier = self._herbivore_max_energy_mod
        else:
            adjusted_modifier = round(float(self._herbivore_max_energy_mod * 0.5),4)

        # Return the max energy as an int based on grid size
        return int(self._rows * self._cols * adjusted_modifier)

    def get_carnivore_max_energy(self):
        """Return the maximum energy for carnivore organisms based on grid size and weather.
        In normal harsh weather the modifier stays the same.
        In all other weather the carnivore can not gain as much energy and its max energy is decreased differing
        amounts with Freezing being most severe and Cloudburst being least.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Freezing':
            adjusted_modifier = round(float(self._carnivore_max_energy_mod * 0.5),4)
        elif self.current_weather == 'Cloudburst':
            adjusted_modifier = round(float(self._carnivore_max_energy_mod * 0.1),4)
        elif self.current_weather == 'Gale':
            adjusted_modifier = round(float(self._carnivore_max_energy_mod * 0.3),4)
        else:
            adjusted_modifier = self._carnivore_max_energy_mod

        # Return the max energy as an int based on grid size
        return int(self._rows * self._cols * adjusted_modifier)

    def get_fungi_max_energy(self):
        """Return the maximum energy for fungi organisms based on grid size and weather.
        In normal harsh weather or gales the modifier stays the same.
        In cloudburst weather the fungi organism thrives slightly more so its corresponding energy is increased
        In freezing weather the fungi can not gain as much energy and thus its max energy is decreased.
        """

        # First check for weather change
        self.change_weather_if_needed()

        # Adjust the modifier based on weather conditions and round to 4 decimal places
        if self.current_weather == 'Cloudburst':
            adjusted_modifier = round(float(self._fungi_max_energy_mod * 1.1),4)
        elif self.current_weather == 'Freezing':
            adjusted_modifier = round(float(self._fungi_max_energy_mod * 0.5),4)
        else:
            adjusted_modifier = self._fungi_max_energy_mod

        # Return the max energy as an int based on grid size
        return int(self._rows * self._cols * adjusted_modifier)

    def get_weather(self):
        """Return the current weather."""
        return self.current_weather