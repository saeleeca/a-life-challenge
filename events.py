from world import *
import pygame
from models import (CreatureType, Genome, MeteoriteObject, Species)
# from main import clock

# Screen shake variables
shake_intensity = 10
shake_duration = 10  # in frames

# Clock for controlling frame rate
clock = pygame.time.Clock()

def apply_shake(offset, view):
    """Applies the screen shake offset to the display."""
    view.get_screen().blit(view.get_screen(), offset)

def shake_screen(view):
    """Generates a random offset for the screen shake."""
    for _ in range(shake_duration):
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        apply_shake((offset_x, offset_y), view)
        pygame.display.flip()
        clock.tick(60)

def meteor(world, view):
    """
    Takes world and view objects, obliterating a random 20x20 space in the world and then updates view.
    """
    # Randomly select a starting row and column within the 50x50 grid
    start_row = random.randint(0, 30)
    start_col = random.randint(0, 30)

    DARK_SILVER = (90, 90, 90)

    # Iterate over the 20x20 area and kill organisms
    for row in range(start_row, start_row + 20):
        for col in range(start_col, start_col + 20):

            # kills organism if organism exists
            world.kill_organism(row, col)

            # Adds a meteorite object on the position of the grid
            world.add_organism(
                MeteoriteObject(Genome(DARK_SILVER, CreatureType.OBJECT, 0, False, 0,
                      0, 0, 0, 0, MeteoriteObject, 0),
                row, col, world, 0, MeteoriteObject), row, col)

    shake_screen(view)
    view.update()


