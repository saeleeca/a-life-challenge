from world import *

def meteor(world, view):
    # Randomly select a starting row and column within the 50x50 grid
    start_row = random.randint(0, 40)
    start_col = random.randint(0, 40)

    # Iterate over the 10x10 area and kill organisms
    for row in range(start_row, start_row + 10):
        for col in range(start_col, start_col + 10):
            world.kill_organism(row, col)

    view.update()


