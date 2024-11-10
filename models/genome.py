from enum import Enum

class CreatureType(Enum):
    PASSIVE = 1
    HERBIVORE = 2
    CARNIVORE = 3

class Genome:
    def __init__(self, color: (int, int, int), creature_type: CreatureType,
        max_energy: int, can_move: bool, reproduction_rate: float):
        self._color: (int, int, int) = color
        self._creature_type: CreatureType = creature_type
        self._max_energy: int = max_energy
        self._can_move: bool = can_move
        self._reproduction_rate: float = reproduction_rate

    def get_color(self) -> (int, int, int):
        return self._color

    def get_creature_type(self) -> CreatureType:
        return self._creature_type

    def get_max_energy(self) -> int:
        return self._max_energy

    def get_can_move(self) -> bool:
        return self._can_move

    def get_reproduction_rate(self) -> float:
        return self._reproduction_rate

    def reproduce(self) -> 'Genome':
        return self.__class__(self._color, self._creature_type,
                              self._max_energy, self._can_move)

    def get_data(self) -> dict:
        """Returns a dictionary with the data to be rendered in the UI"""
        # Convert creature type constant to string
        creature_type = self._creature_type
        if creature_type == CreatureType.CARNIVORE:
            creature_type_str = "Carnivore"
        elif creature_type == CreatureType.HERBIVORE:
            creature_type_str = "Herbivore"
        else:
            creature_type_str = "Passive"

        return {
            "Color": self._color,
            "Creature Type": creature_type_str,
            "Max Energy": self._max_energy,
            "Can Move": self._can_move,
        }
