import random
import pygame
import pickle
import os
import tkinter as tk
from tkinter import filedialog

import events
from models import CreatureType, Genome, PassiveOrganism, HerbivoreOrganism, CarnivoreOrganism
from view.constants import ButtonEvent
from view.view import View
from world import World
from events import *

ROWS, COLS = World.ROWS, World.COLS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PLAY, PAUSE, STEP = 0, 1, 2
state = PAUSE
running = True
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
    visited = set()
    for row in range(ROWS):
        for col in range(COLS):
            organism = world.get_cell(row, col)
            if organism and organism not in visited:
                visited.add(organism)
                organism.choose_action()


def start_game():
    global state
    state = PLAY
    view.update_playback_state(ButtonEvent.PLAY)

def pause_game():
    global state
    state = PAUSE
    view.update_playback_state(ButtonEvent.PAUSE)

def reset_game():
    global world
    global view
    global state
    state = PAUSE
    world = World(ROWS, COLS)
    # Reinitializing the view, sets the playback buttons to paused
    view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game)

    setup_life(world)
    view.update()

def step_game():
    global state
    state = PAUSE
    view.update_playback_state(ButtonEvent.PAUSE)
    process_cells(world)
    view.update()

def save_game(data_to_save):
    # Open file dialog (using Tkinter)
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pkl",
        filetypes=[("Pickle Files", "*.pkl")]
    )
    root.destroy()

    if file_path:
        # Save data using pickle
        with open(file_path, "wb") as file:
            pickle.dump(data_to_save, file)
        print("Data saved successfully!")

def open_file_explorer():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path

# currently bugged, game doesn't load properly unless in main game loop
def load_game():
    file_path = open_file_explorer()
    if file_path:
        # Do something with the selected file
        print("Selected file:", file_path)

    with open(file_path, 'rb') as file:
        savedWorld = pickle.load(file)
    world = savedWorld
    view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game)
    view.render_grid()


world = World(ROWS, COLS)
view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game)
clock = pygame.time.Clock()

setup_life(world)
view.update()
pygame.display.flip()

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and state == PLAY:
                pause_game()
            elif event.key == pygame.K_p and state == PAUSE:
                start_game()
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_q:
                pygame.quit()

            elif event.key == pygame.K_r:  # r to restart the simulation
                world = World(ROWS, COLS)
                view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game)
                setup_life(world)
                view.render_grid()

            elif event.key == pygame.K_s:  # s to save
                savegame = world
                save_game(savegame)

            elif event.key == pygame.K_l:  # l to reload save
                # load_game() currently bugged
                file_path = open_file_explorer()
                if file_path:
                    # Do something with the selected file
                    print("Selected file:", file_path)

                with open(file_path, 'rb') as file:
                    savedWorld = pickle.load(file)
                world = savedWorld
                view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game)
                view.render_grid()

            elif event.key == pygame.K_m:  # summons a meteor to kill organisms in a 10x10 area
                events.meteor(world)
                view.update()

            elif event.key == pygame.K_q:  # q to quit
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            view.handle_click()
        elif event.type == pygame.MOUSEMOTION:
            view.handle_mouse_move()
        elif event.type == pygame.MOUSEBUTTONUP:
            view.handle_mouse_up()


    if state == PLAY:
        process_cells(world)
        view.update()

    pygame.display.flip()
    # limits FPS to 1
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(20)

pygame.quit()