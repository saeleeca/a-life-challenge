from models import Organism, PassiveOrganism

class HerbivoreOrganism(Organism):
    def __init__(self, genome, row, col, world, generation, species):
        super().__init__(genome, row, col, world, generation, species)
        # Set custom values for the Herbivore. 
        self._move_energy_expenditure = 1
        self._food_energy = 20
        self._base_energy_expenditure = 0.9
        self._food_type = PassiveOrganism
        self._reproduction_ratio = 1.4
        

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


