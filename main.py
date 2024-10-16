import random

import pygame

# pygame setup screen, clock, and relevant values.
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
setup = True
dt = 0

# screen width and height values to be used in organism arrays
screen_width_1div10 = int(screen.get_width() / 10)
screen_height_1div10 = int(screen.get_height() / 10)

# mutable array that holds 0 for no passive organism and 1 for passive organism. Used in determining if an
# organism dies/lives/reproduces.
passive_og_array= [[0 for i in range(screen_width_1div10)] for j in range(screen_height_1div10)]

def setup_life():
    """Function to set up the Game of Life simulation. Currently, adds passive organisms to a screen"""
    #initialize starting array for passive organism. This will be filled with the coordinates of the passive organism
    passive_coord_array = []

    # Get width and height for current screen size
    x_pos = screen.get_width()
    y_pos = screen.get_height()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # initialize the starting squares. Set up a random number of organisms to be populated. Organisms are currently
    # 10x10 squares, so step the coordinates by 10 so there are no organism overlaps. Add organisms to both the
    # coordinate array and array that indicates if square is filled.
    count = 0
    random_number = random.randrange(1000, 4000)
    while count < random_number:
        new_x = random.randrange(0, x_pos, 10)
        new_y = random.randrange(0, y_pos, 10)
        if [new_x, new_y] not in passive_coord_array:
            passive_coord_array.append([new_x, new_y])
            passive_og_array[int(new_x / 10)][int(new_y / 10)] = 1
            pygame.draw.rect(screen, "red", (new_x, new_y, 10, 10))
            count += 1

    # flip() the display to put your work on screen
    pygame.display.flip()
    return screen, passive_coord_array


def check_neighbors(i,j):
    """Function to check if a cell i and j is occupied. The returned count is used in determining if an organism
    lives/dies/reproduces."""
    count = 0
    if i < screen_width_1div10 - 1 and passive_og_array[i + 1][j] == 1:
        count += 1
    if i > 0 and passive_og_array[i - 1][j] == 1:
        count += 1
    if j < screen_height_1div10 - 1 and passive_og_array[i][j + 1] == 1:
        count += 1
    if j > 0 and passive_og_array[i][j - 1] == 1:
        count += 1
    return count

def cell_death_life():
    """Function to check if a cell i and j should live/die/reproduce."""
    temp_passive_og_array = [[0 for i in range(screen_width_1div10)] for j in range(screen_height_1div10)]
    for i in range(screen_width_1div10):
        for j in range(screen_height_1div10):
            # check current living cell for death
            if passive_og_array[i][j] == 1:
                count_live = check_neighbors(i,j)
                # Any live cell with fewer than two live neighbours dies, as if by underpopulation
                if count_live < 2:
                    temp_passive_og_array[i][j] = 0
                # Any live cell with more than three live neighbours dies, as if by overpopulation
                elif count_live > 3:
                    temp_passive_og_array[i][j] = 0
                # Any live cell with two or three live neighbours lives on to the next generation
                else:
                    temp_passive_og_array[i][j] = 1
            # check empty cell for reproduction
            else:
                count_live = check_neighbors(i, j)
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
                if count_live == 3:
                    temp_passive_og_array[i][j] = 1
                # Or remains empty
                else:
                    temp_passive_og_array[i][j] = 0

    return temp_passive_og_array

def cell_draw():
    """Function to draw a cell on the screen."""
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    for i in range(screen_width_1div10):
        for j in range(screen_height_1div10):
            if passive_og_array[i][j] == 1:
                pygame.draw.rect(screen, "red", (i*10, j*10, 10, 10))
    # flip() the display to put your work on screen
    pygame.display.flip()
    return screen



while running:

    # run setup first before executing the game of life rules
    if setup:
        screen, organism_array = setup_life()
        setup = False

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the functions for the passive organism and draw the new organisms on the screen
    passive_og_array = cell_death_life()
    cell_draw()

    # limits FPS to 1
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(1)

pygame.quit()