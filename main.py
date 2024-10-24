import random
import pygame

from models import CreatureType, Genome, PassiveOrganism, HerbivoreOrganism, CarnivoreOrganism
from view.playbackUI import PlaybackState
from view.view import View
from world import World

ROWS = COLS = 60

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PLAY, PAUSE, STEP = 0, 1, 2
state = PAUSE
running = True
dt = 0

def create_genome(creature_type) -> Genome:
    if creature_type == CreatureType.PASSIVE:
        return Genome(GREEN, creature_type, 20, False)
    if creature_type == CreatureType.CARNIVORE:
        return Genome(RED, creature_type, 100, True)
    return Genome(BLUE, creature_type, 50, True)


def setup_life(world):
    for row in range(ROWS):
        for col in range(COLS):
            val = random.randint(0, 20)
            # 0-5 passive, 5-7 herbivore, 8 carnivore
            if val < 6:
                world.add_organism(PassiveOrganism(create_genome(CreatureType.PASSIVE), row, col, world), row, col)
            elif val < 8:
                world.add_organism(HerbivoreOrganism(create_genome(CreatureType.HERBIVORE), row, col, world), row, col)
            elif val == 8:
                 world.add_organism(CarnivoreOrganism(create_genome(CreatureType.CARNIVORE), row, col, world), row, col)

def process_cells(world):
    visited = set()
    for row in range(ROWS):
        for col in range(COLS):
            organism = world.get_cell(row, col)
            if organism and organism not in visited:
                visited.add(organism)
                organism.choose_action()


world = World(ROWS, COLS)
view = View(ROWS, COLS, world)
clock = pygame.time.Clock()

setup_life(world)
view.render_grid()
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                state = PAUSE
                view.update_playback_state(PlaybackState.PAUSE)
            elif event.key == pygame.K_o:
                state = PLAY
                view.update_playback_state(PlaybackState.PLAY)
            elif event.key == pygame.K_r:
                setup_life(world)
                view.render_grid()
            elif event.key == pygame.K_q:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_type = view.handle_click()
            if click_type == PlaybackState.PLAY:
                state = PLAY
            elif click_type == PlaybackState.PAUSE:
                state = PAUSE
            elif click_type == PlaybackState.RESET:
                setup_life(world)
                view.render_grid()
            elif click_type == PlaybackState.STEP:
                state = STEP
                process_cells(world)
                view.render_grid()
        elif event.type == pygame.MOUSEMOTION:
            view.handle_mouse_move()

    if state == PLAY:
        process_cells(world)
        view.render_grid()
    elif state == PAUSE:
        # screen.blit(text_surface, (0, 0))
        # pygame.display.update()
        pass
    pygame.display.flip()
    # limits FPS to 1
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(20)

pygame.quit()