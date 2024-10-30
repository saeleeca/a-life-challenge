from models import Organism, PassiveOrganism

class HerbivoreOrganism(Organism):
    def __init__(self, genome, row, col, world):
        super().__init__(genome, row, col, world)
        # Set custom values for the Herbivore. 
        self._move_energy_expenditure = 1
        self._food_energy = 10
        self._base_energy_expenditure = 1
        self._food_type = PassiveOrganism  
        self._reproduction_ratio = 1.5
        

    def choose_action(self):
        """Herbivore checks adjacent cells for passive organisms, eats if found, 
        moves if no food, and dies if out of energy."""
        
        # Step 1: Check adjacent cells for food
        food_found, food_row, food_col = self._world.get_adjacent_food(self._row, self._col, self._food_type)

        if food_found:
            # Step 2: Eat the food if found            
            self.eat(self._world.get_cell(food_row, food_col)) 
        
        # Step 3: Move randomly if no food found and can move
        if self._genome.get_can_move():
            self.random_move()            
        
        # Step 4: Calculate baseline energy loss. Die if out of energy.
        self._energy -= self._base_energy_expenditure
        if self._energy <= 0:
            self._world.kill_organism(self._row, self._col)

        # Step 5: Check if sufficient energy and space to reproduce
        self.check_if_can_reproduce()

    def eat(self, food: 'Organism') -> None:
        """Increases energy when consuming passive organisms."""
        self._energy += food.get_food_energy()  # Gain the energy of the food
        self._world.kill_organism(food._row, food._col)  # Remove the food from the world

    def random_move(self):
        """Move to a random adjacent empty cell."""
        empty_found, empty_row, empty_col = self._world.get_empty_neighbor(self._row, self._col, True)
        if empty_found:
            self.move(empty_row, empty_col)

    def check_if_can_reproduce(self) -> bool:
        empty_found, empty_row, empty_col = self._world.get_empty_neighbor(self._row, self._col, True)
        if (self._energy >= (self._reproduction_ratio * self._genome.get_max_energy()) and empty_found):
            self.reproduce(empty_row, empty_col)

    