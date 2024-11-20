from enum import Enum

class CreatureType(Enum):
    PASSIVE = 1
    HERBIVORE = 2
    CARNIVORE = 3
    FUNGI = 4

class Genome:
    def __init__(self, color: (int, int, int), creature_type: CreatureType,
        max_energy: int, can_move: bool, reproduction_rate: float, reproduction_energy_expenditure: int, move_energy_expenditure: int, base_energy_expenditure: float,
                 food_energy: int, food_type: type, reproduction_ratio: int, can_seek_food: bool = False,
                 can_hibernate: bool = False, can_panic: bool = False, movement_iterations:int = 1):
        self._color: (int, int, int) = color
        self._creature_type: CreatureType = creature_type
        self._max_energy: int = max_energy
        self._can_move: bool = can_move
        self._reproduction_rate: float = reproduction_rate
        self._reproduction_energy_expenditure: int = reproduction_energy_expenditure
        self._move_energy_expenditure: int = move_energy_expenditure
        self._base_energy_expenditure: int = base_energy_expenditure
        self._food_energy: int = food_energy
        self._food_type: type = food_type
        self._reproduction_ratio: int = reproduction_ratio
        self._can_seek_food: bool = can_seek_food           
        self._can_hibernate: bool = can_hibernate
        self._can_panic: bool = can_panic
        self._movement_iterations:int = movement_iterations # defaults to 1

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
    
    def get_reproduction_energy_expenditure(self) -> int:
        return self._reproduction_energy_expenditure
    
    def get_move_energy_expenditure(self) -> int:
        return self._move_energy_expenditure

    def get_base_energy_expenditure(self) -> int:
        return self._base_energy_expenditure

    def get_food_energy(self) -> int:
        return self._food_energy

    def get_food_type(self) -> type:
        return self._food_type

    def get_reproduction_ratio(self) -> int:
        return self._reproduction_ratio
    
    def get_can_seek_food(self) -> bool:
        return self._can_seek_food
    
    def get_can_hibernate(self) -> bool:
        return self._can_hibernate

    def get_can_panic(self) -> bool:
        return self._can_panic
    
    def get_movement_iterations(self) -> int:
        return self._movement_iterations

    def set_movement_iterations(self, value: int):
        self._movement_iterations = max(1, value)  # Ensure it's at least 1

    def reproduce(self) -> 'Genome':
        return self.__class__(self._color, self._creature_type,
                              self._max_energy, self._can_move, self._reproduction_rate)

    def get_data(self) -> dict:
        """Returns a dictionary with the data to be rendered in the UI"""
        # Convert creature type constant to string
        creature_type = self._creature_type
        if creature_type == CreatureType.CARNIVORE:
            creature_type_str = "Carnivore"
        elif creature_type == CreatureType.HERBIVORE:
            creature_type_str = "Herbivore"
        elif creature_type == CreatureType.FUNGI:
            creature_type_str = "Fungi"
        else:
            creature_type_str = "Passive"

        return {
            "Color": self._color,
            "Creature Type": creature_type_str,
            "Max Energy": self._max_energy,
            "Can Move": self._can_move,
            "Reproduction Rate": self._reproduction_rate,
        }

    def get_difference(self, other: 'Genome'):
        # Creature type can never be the same
        if self._creature_type != other._creature_type:
            return 100
        # compare color
        r1, g1, b1 = self._color
        r2, g2, b2 = other._color
        color_dif = ((abs(r2 - r1) + abs(g2 - g1) + abs(b2 - b1)) / 3) / 255
        move_dif = 0 if self._can_move == other._can_move else .33
        max_energy1, max_energy2 = self._max_energy, other._max_energy
        max_energy_dif = (abs(max_energy1 - max_energy2) / max(max_energy1, max_energy2))

        return (color_dif + move_dif + max_energy_dif) / 3