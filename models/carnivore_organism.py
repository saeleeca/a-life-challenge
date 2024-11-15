from models import Organism, HerbivoreOrganism

class CarnivoreOrganism(Organism):
    def __init__(self, genome, row, col, world, generation, species):
        super().__init__(genome, row, col, world, generation, species)
        # Set custom values for the Carnivore. 
        # self._move_energy_expenditure = 1.5
        # self._food_energy = 8
        # self._base_energy_expenditure = 1.5
        # self._food_type = HerbivoreOrganism
        # self._reproduction_ratio = 2.5
        
    def choose_action(self):
        if self._world.herbivore_count < self._low_food_threshold:
            # Conserve energy and avoid moving when herbivores are too few
            self._energy -= self._base_energy_expenditure // 2
        else:
            super().choose_action()  # Regular behavior if enough food is available

    def choose_action(self):
        """Carnivore checks adjacent cells for passive organisms, eats if found, 
        moves if no food, and dies if out of energy."""
        
        # Step 1: Check adjacent cells for food
        food_found, food_row, food_col = self._world.get_adjacent_food(self._row, self._col, self._food_type)

        # Step 2: Eat the food if found
        if food_found:                    
            self.eat(self._world.get_cell(food_row, food_col)) 
        
        # Step 3: Move randomly if no food found and can move and has enough energy
        else:
            if self._genome.get_can_move():
                self.random_move() 

        # Step 4: Calculate baseline energy loss. Die if out of energy.
        self._energy -= self._base_energy_expenditure
        if self._energy <= 0:
            self._world.kill_organism(self._row, self._col)
        
        # Step 5: Check if sufficient energy and space to reproduce
        self.check_if_can_reproduce()


