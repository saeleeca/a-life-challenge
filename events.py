from world import *
import pygame
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
    Takes world and view objects, obliterating a random 10x10 space in the world and then updates view.
    """
    # Randomly select a starting row and column within the 50x50 grid
    start_row = random.randint(0, 30)
    start_col = random.randint(0, 30)

    # Iterate over the 10x10 area and kill organisms
    for row in range(start_row, start_row + 20):
        for col in range(start_col, start_col + 20):
            world.kill_organism(row, col)

    shake_screen(view)
    view.update()


