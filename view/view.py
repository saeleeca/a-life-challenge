import pygame

from view.buttonBarUI import ButtonBarUI
from view.constants import *
from view.playbackUI import PlaybackUI
from view.statsUI import StatsUI
from view.text import render_text, render_stat_text


class View:
    def __init__(self, rows: int, cols: int, world):
        self._rows: int = rows
        self._cols: int = cols
        self._world = world
        self._grid_size: float = WORLD_WIDTH / rows

        pygame.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # initialize window
        self._screen.fill(WINDOW_BG)
        self._render_title()

        self._playback_ui = PlaybackUI(self._screen)

        width = (BUTTON_WIDTH * 2) + BUTTON_GAP
        file_x = WINDOW_WIDTH - width - 50
        self._file_ui = ButtonBarUI(self._screen,
                                    file_x, 15,
                                    (SAVE_ICON, SAVE_ICON_HOVER, ButtonEvent.SAVE),
                                    (LOAD_ICON, LOAD_ICON_HOVER, ButtonEvent.LOAD))

        self._draw_world_border()
        self._stats_ui = StatsUI(self._screen)

    def _draw_world_border(self):
        # Create world border
        pygame.draw.rect(self._screen, WORLD_BORDER_COLOR,
                         (WORLD_X - BORDER_WIDTH,
                          WORLD_Y - BORDER_WIDTH,
                          self._grid_size * self._cols + BORDER_WIDTH * 2,
                          self._grid_size * self._rows + BORDER_WIDTH * 2),
                         border_radius=5)

    def render_grid(self):
        # Draw the world background
        pygame.draw.rect(self._screen, WORLD_BG,
                         (WORLD_X, WORLD_Y,
                          WORLD_HEIGHT, WORLD_WIDTH))


        for row in range(self._rows):
            for col in range(self._cols):
                organism = self._world.get_cell(row, col)
                if organism:
                    self._draw_organism(organism, row, col)

        self._stats_ui.render_statistics()

    def _draw_organism(self, organism, row, col):
        color = organism.get_color()

        # Draw as a square
        rect = self._convert_cell_to_rect(row, col)
        pygame.draw.rect(self._screen, color, rect)


    def _convert_cell_to_rect(self, row, col):
        return (col * self._grid_size + WORLD_X,
                row * self._grid_size + WORLD_Y,
                self._grid_size, self._grid_size)

    def _render_title(self):
        x_center = WORLD_X / 2 + BUTTON_HEIGHT
        y_center = 60
        font = pygame.font.SysFont(TITLE_FONT_NAME, TITLE_FONT_SIZE)
        render_text(GAME_TITLE, font, TITLE_TEXT,
                    x_center, y_center, self._screen)

    def handle_click(self):
        playback_action = (self._playback_ui.handle_click_event() or
                           self._file_ui.handle_click_event() or
                           self._stats_ui.handle_click_event())
        if playback_action:
            return playback_action
        return None

    def handle_mouse_move(self):
        if (self._playback_ui.handle_hover_event() or
                self._file_ui.handle_hover_event() or
                self._stats_ui.handle_hover_event()):
            return

    def update_playback_state(self, playbackState):
        self._playback_ui.update_playback_state(playbackState)


