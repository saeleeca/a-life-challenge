import random
import pygame
import pickle

import events
from models import (CreatureType, Genome, PassiveOrganism, HerbivoreOrganism,
                    CarnivoreOrganism, FungiOrganism, Species)
from services.mutation_service import MutationService
from view.constants import ButtonEvent
from view.view import View
from world import World
from services import mutation_service

ROWS, COLS = World.ROWS, World.COLS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (150, 75, 0)

PLAY, PAUSE, STEP = 0, 1, 2
state = PAUSE
running = True
dt = 0

# Settings
iterations_per_frame = 1
iterations = 0
fps = 120   # Used in Delta time.
time_since_last_update = 0 # For simulation speed
speed_threshold = 50 # For simulation speed
speed_slider = 50 # For simulation speed
mutation_slider = 1 # For mutation rate

def create_genome(creature_type, world) -> Genome:
    if creature_type == CreatureType.PASSIVE:
        return Genome(GREEN, creature_type, world.get_environment().get_passive_max_energy(), False, world.get_environment().get_passive_reproduction_rate_mod())
    if creature_type == CreatureType.CARNIVORE:
        return Genome(RED, creature_type, world.get_environment().get_carnivore_max_energy(), True, world.get_environment().get_carnivore_reproduction_rate_mod())
    if creature_type == CreatureType.FUNGI:
        return Genome(BROWN, creature_type, world.get_environment().get_fungi_max_energy(), False, world.get_environment().get_fungi_reproduction_rate_mod())
    return Genome(BLUE, creature_type, world.get_environment().get_herbivore_max_energy(), True, world.get_environment().get_herbivore_reproduction_rate_mod())

def setup_life(world):
    # Create 4 base species
    passive_species = Species(create_genome(CreatureType.PASSIVE, world),
                              0, world)
    herbivore_species = Species(create_genome(CreatureType.HERBIVORE, world),
                                0, world)
    carnivore_species = Species(create_genome(CreatureType.CARNIVORE, world),
                                0, world)
    fungi_species = Species(create_genome(CreatureType.FUNGI, world),
                                0, world)
    world.set_base_species([passive_species, herbivore_species, carnivore_species, fungi_species])

    for row in range(ROWS):
        for col in range(COLS):
            val = random.randint(0, 100)
            # 0-5 passive, 5-7 herbivore, 8 carnivore, 9-11 fungi
            if val < 30:
                world.add_organism(PassiveOrganism(create_genome(CreatureType.PASSIVE, world), row, col, world, 1, passive_species), row, col)
            elif 30 <= val <= 38:
                world.add_organism(HerbivoreOrganism(create_genome(CreatureType.HERBIVORE, world), row, col, world, 1, herbivore_species), row, col)
            elif 39 <= val <= 42:
                 world.add_organism(CarnivoreOrganism(create_genome(CreatureType.CARNIVORE, world), row, col, world, 1, carnivore_species), row, col)
            elif val == 50:
                world.add_organism(FungiOrganism(create_genome(CreatureType.FUNGI, world), row, col, world, 1, fungi_species), row, col)

def process_cells(world):
    visited = set()
    day = world.get_day()
    for row in range(ROWS):
        for col in range(COLS):
            organism = world.get_cell(row, col)
            if (organism and (organism not in visited) and
                    (day == 0 or day != organism.get_birthday())):
                visited.add(organism)
                organism.choose_action()

    world.inc_day()


def start_game():
    """ Starts the current simulation if state is PAUSE"""
    global state
    state = PLAY
    view.update_playback_state(ButtonEvent.PLAY)

def pause_game():
    """ Pauses the current simulation if state is PLAY"""
    global state
    state = PAUSE
    view.update_playback_state(ButtonEvent.PAUSE)

def reset_game():
    """ Reinitializes new world and view object to reset simulation"""
    global world
    global view
    global state
    global iterations
    iterations = 0
    # Always start at Pause state
    state = PAUSE
    view.update_playback_state(ButtonEvent.PAUSE)

    world.reset()
    setup_life(world)
    view.update()

def step_game():
    """ Pauses current simulation to step forward one frame of gameloop"""
    global state
    state = STEP
    view.update_playback_state(ButtonEvent.PAUSE)

def save_game():
    """ Saves current data to specified file """
    global world

    # Save data using pickle
    with open("world_save.pkl", "wb") as file:
        pickle.dump(world, file)
    print("Data saved successfully!")

def load_game():
    """ Loads a previously saved pickle file"""
    global world
    global view

    # Attempts to open file called "world_save"
    try:
        with open("world_save.pkl", 'rb') as file:
            savedWorld = pickle.load(file)

            # Overwrites current world and view object before updating view
            world = savedWorld
            world.load()    # Updates the Species index to match savedWorld
            view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game, save_game, load_game, slider_fns, meteor)
            view.update()
    except:
        print("File not found! Try saving first.")

def change_iteration_value(new_value):
    """Updates iterations per frame (used with slider)"""
    global iterations_per_frame
    global iterations
    # Make sure new value isn't less than iterations
    # otherwise update never triggers
    if new_value < iterations:
        iterations = new_value - 1
    iterations_per_frame = new_value

def change_speed(new_value):
    """Increases and decreases the speed of the simulation independently of delta time"""
    global speed_threshold
    global speed_slider
    # Take the difference between previous slider position and new position
    # Each step will be 0.9 instead of 1 to prevent reaching 0 at max speed
    adjusted_speed_threshold = round(abs(speed_slider - new_value) * 0.9, 4)
    # Add the adjusted threshold to the speed threshold to make it slow down
    if new_value < speed_slider:
        speed_threshold = round(speed_threshold + adjusted_speed_threshold, 4)
        speed_slider = new_value
    # Subtract the adjusted threshold to the speed threshold to make it speed up
    elif new_value > speed_slider:
        speed_threshold = round(speed_threshold - adjusted_speed_threshold, 4)
        speed_slider = new_value

def change_mutation_rate(multiplier):
    """Increases and decreases the rate of mutations"""
    global mutation_slider
    if mutation_slider < multiplier:
        mutation_service.MutationService.mutation_rate_modifier(multiplier)
        mutation_slider = multiplier
    elif mutation_slider > multiplier:
        mutation_service.MutationService.mutation_rate_modifier(multiplier)
        mutation_slider = multiplier

def meteor():
    """Helper function that wipes a 20x20 grid of the map with a meteor"""
    global view
    events.meteor(world, view)
    view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game, save_game, load_game, slider_fns, meteor)
    view.update()

# Add slider fn here, then retrieve and pass to the Slider in settingsUI
slider_fns = {"iterations": change_iteration_value, "speed": change_speed, "mutation": change_mutation_rate}


world = World()
view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game,
            save_game, load_game, slider_fns, meteor)
clock = pygame.time.Clock()

setup_life(world)
view.update()
#pygame.display.flip()


# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            # Press p to pause and unpause simulation
            if event.key == pygame.K_p and state == PLAY:
                pause_game()
            elif event.key == pygame.K_p and state == PAUSE:
                start_game()

            # Press r to restart simulation
            elif event.key == pygame.K_r:
                reset_game()

            # Press q to quit simulation
            elif event.key == pygame.K_q:
                pygame.quit()

            # Press s to save, brings up file explorer to name file
            elif event.key == pygame.K_s:
                save_game()

            # Press l to reload save, opens file explorer to choose file
            elif event.key == pygame.K_l:
                load_game()

            # Press m to generate a meteor to kill organisms in a 10x10 area
            elif event.key == pygame.K_m:
                meteor()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            view.handle_click()
        elif event.type == pygame.MOUSEMOTION:
            view.handle_mouse_move()
        elif event.type == pygame.MOUSEBUTTONUP:
            view.handle_mouse_up()

    if state == PLAY or state == STEP:
        # Allows simulation to change speed without effecting Delta time
        if time_since_last_update > speed_threshold:
            iterations += 1
            process_cells(world)
            time_since_last_update = 0
        else:
            time_since_last_update += dt
        if iterations == iterations_per_frame:
            view.update()
            iterations = 0
            if state == STEP:
                state = PAUSE

    pygame.display.flip()
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(fps)

pygame.quit()