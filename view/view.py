import pygame

from view.sections.buttonBarUI import ButtonBarUI
from view.constants import *
from view.sections.playbackUI import PlaybackUI
from view.sections.settingsUI import SettingsUI
from view.sections.statsUI import StatsUI
from view.text import render_text


class View:
    """Handles rendering the UI and the different UI components"""
    def __init__(self, rows: int, cols: int, world, start_fn, pause_fn, reset_fn, step_fn, save_fn, load_fn):
        self._rows: int = rows
        self._cols: int = cols
        self._world = world
        self._grid_size: float = WORLD_WIDTH / rows

        # initialize window
        pygame.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self._screen.fill(WINDOW_BG)
        self._render_title()
        self._draw_world_border()

        # initialize/draw components
        # _playback_ui, _file_ui, _stats_ui, _settings_ui
        self._playback_ui = PlaybackUI(self._screen, start_fn, pause_fn, reset_fn, step_fn)
        width = (BUTTON_WIDTH * 2) + BUTTON_GAP
        file_x = WINDOW_WIDTH - width - 150
        self._file_ui = ButtonBarUI(self._screen, file_x, 15,
                        (SAVE_ICON, SAVE_ICON_HOVER, save_fn),
                                (LOAD_ICON, LOAD_ICON_HOVER, load_fn),
                                (METEOR_ICON, METEOR_ICON_HOVER, None))
        self._stats_ui = StatsUI(self._screen)
        self._settings_ui = SettingsUI(self._screen)
        self._components = [ self._playback_ui, self._file_ui, self._stats_ui,
                             self._settings_ui]

    def _draw_world_border(self):
        """Draws the border around the world"""
        pygame.draw.rect(self._screen, WORLD_BORDER_COLOR,
                         (WORLD_X - BORDER_WIDTH,
                          WORLD_Y - BORDER_WIDTH,
                          self._grid_size * self._cols + BORDER_WIDTH * 2,
                          self._grid_size * self._rows + BORDER_WIDTH * 2),
                         border_radius=5)

    def render_grid(self):
        """Draws the world grid"""
        # Draw the world background
        pygame.draw.rect(self._screen, 
                         self._world.get_background_environment_color(),
                         (WORLD_X, WORLD_Y,
                          WORLD_HEIGHT, WORLD_WIDTH))


        for row in range(self._rows):
            for col in range(self._cols):
                organism = self._world.get_cell(row, col)
                if organism:
                    self._draw_organism(organism, row, col)

    def update(self):
        """
        Draws the components that need to be refreshed at each game iteration,
        the world grid and updated stats
        """
        self.render_grid()
        self._stats_ui.render_statistics()

    def _draw_organism(self, organism, row: int, col: int):
        """Helper method to draw an organism"""
        color = organism.get_color()

        # Draw as a square
        rect = self._convert_cell_to_rect(row, col)
        pygame.draw.rect(self._screen, color, rect)


    def _convert_cell_to_rect(self, row: int, col: int):
        """Helper method to convert row/col to a rect using screen coords"""
        return (col * self._grid_size + WORLD_X,
                row * self._grid_size + WORLD_Y,
                self._grid_size, self._grid_size)

    def _render_title(self):
        """Draws the game title to the screen"""
        x_center = WORLD_X / 2 + BUTTON_HEIGHT
        y_center = 60
        font = pygame.font.SysFont(TITLE_FONT_NAME, TITLE_FONT_SIZE)
        render_text(GAME_TITLE, font, TITLE_TEXT,
                    x_center, y_center, self._screen)

    def handle_click(self):
        """Handles click events for all the UI components"""
        for component in self._components:
            if component.handle_click_event():
                return

    def handle_mouse_move(self) -> (ButtonEvent | None, int):
        """Handles mouse move/hover events for all the UI components"""
        for component in self._components:
            if component.handle_hover_event():
                return

    def handle_mouse_up(self):
        """Handles mouse up event for slider button components"""
        self._settings_ui.handle_mouse_up() # Slider buttons end slide

    def update_playback_state(self, playbackState: ButtonEvent):
        """
        Updates the playback ui, when changed from outside the UI, like when
        the user switches to pause using the keyboard
        """
        self._playback_ui.update_playback_state(playbackState)


