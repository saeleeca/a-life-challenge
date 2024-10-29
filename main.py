import random
import pygame

from models import CreatureType, Genome, Organism, PassiveOrganism, HerbivoreOrganism, CarnivoreOrganism
from view import View
from world import World

ROWS, COLS = World.ROWS, World.COLS
GRID_SIZE = 10
WIDTH, HEIGHT = ROWS*GRID_SIZE, COLS*GRID_SIZE

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# pygame setup screen, clock, and relevant values.
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
PLAY, PAUSE = 0, 1
state = PLAY
running = True
font = pygame.font.Font(pygame.font.get_default_font(), 18)
text_surface = font.render("Paused - P to Pause/Resume - Q to Quit - R to Restart", True, "black")
dt = 0

def create_genome(creature_type, world) -> Genome:
    if creature_type == CreatureType.PASSIVE:
        return Genome(GREEN, creature_type, world.get_world_max_passive_energy(), False)
    if creature_type == CreatureType.CARNIVORE:
        return Genome(RED, creature_type, world.get_world_max_carnivore_energy(), True)
    return Genome(BLUE, creature_type, world.get_world_max_herbivore_energy(), True)


def setup_life(world):
    for row in range(ROWS):
        for col in range(COLS):
            val = random.randint(0, 20)
            # 0-5 passive, 5-7 herbivore, 8 carnivore
            if val < 6:
                world.add_organism(PassiveOrganism(create_genome(CreatureType.PASSIVE, world), row, col, world), row, col)
            elif 6< val < 8:
                world.add_organism(HerbivoreOrganism(create_genome(CreatureType.HERBIVORE, world), row, col, world), row, col)
            elif val == 8:
                 world.add_organism(CarnivoreOrganism(create_genome(CreatureType.CARNIVORE, world), row, col, world), row, col)

def process_cells(world):
    # moves organisms into next cell if empty
    # only to demonstrate ui and test
    visited = set()
    for row in range(ROWS):
        for col in range(COLS):
            organism = world.get_cell(row, col)
            if organism and organism not in visited:
                visited.add(organism)
                if isinstance(organism, (PassiveOrganism, HerbivoreOrganism, CarnivoreOrganism)):
                    organism.choose_action()
                # else:
                #     valr = random.randint(0, 12)
                #     valc = random.randint(0, 12)
                #     if valr > 6:
                #         next_row = row + 1
                #     elif valr > 0:
                #         next_row = row - 1
                #     else:
                #         next_row = row
                #     if valc > 6:
                #         next_col = col + 1
                #     elif valc > 0:
                #         next_col = col - 1
                #     else:
                #         next_col = col

                #     if row == next_row and col == next_col:
                #         continue
                #     # go out of bounds and remove
                #     if (next_row >= ROWS or next_col >= COLS or
                #         next_row <= -1 or next_col <= -1):
                #         world.kill_organism(row, col)

                #     elif world.is_cell_empty(next_row, next_col):
                #         organism.move(next_row, next_col)


world = World(ROWS, COLS)
view = View(WIDTH, HEIGHT, ROWS, COLS, world, screen, GRID_SIZE)

setup_life(world)
view.render_grid()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and state == PLAY:
                state = PAUSE
            elif event.key == pygame.K_p and state == PAUSE:
                state = PLAY
            elif event.key == pygame.K_r:
                world = World(ROWS, COLS)
                view = View(WIDTH, HEIGHT, ROWS, COLS, world, screen, GRID_SIZE)

                setup_life(world)
                view.render_grid()
            elif event.key == pygame.K_q:
                pygame.quit()

    if state == PLAY:
        process_cells(world)
        view.render_grid()
    elif state == PAUSE:
        screen.blit(text_surface, (0, 0))
        pygame.display.update()

    # limits FPS to 1
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(20)

pygame.quit()