import pygame

from view.sections.buttonBarUI import ButtonBarUI
from view.constants import *
from view.sections.playbackUI import PlaybackUI
from view.sections.settingsUI import SettingsUI
from view.sections.statsUI import StatsUI
from view.sections.modalUI import ModalUI
from view.text import render_text

GAME, MODAL = 0, 1  # View modes
class View:
    """Handles rendering the UI and the different UI components"""
    def __init__(self, rows: int, cols: int, world, start_fn, pause_fn, reset_fn, step_fn, save_fn, load_fn, slider_fns, meteor_fn):
        self._rows: int = rows
        self._cols: int = cols
        self._world = world
        self._grid_size: float = WORLD_WIDTH / rows
        # _grid_size * _render_scale needs to be an int.
        # _render_scale can be adjusted for this, if ROWS/COLS changes
        self._render_scale = 2
        self._render_surface = pygame.Surface(
            (self._cols * self._grid_size * self._render_scale,
             self._rows * self._grid_size * self._render_scale)
        )
        self._pause_fn = pause_fn
        self._start_fn = start_fn
        self._reset_fn = reset_fn
        self._step_fn = step_fn
        self._viewing_modal = False  # used to stop checking clicks when user is viewing an organism

        # initialize window
        pygame.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self._screen.fill(WINDOW_BG)
        self._render_title()
        self._draw_world_border()

        # initialize/draw components
        # _playback_ui, _file_ui, _stats_ui, _settings_ui
        self._playback_ui = PlaybackUI(self._screen, self._start_fn,
                                       self._pause_fn,
                                       self._reset_fn, self._step_fn)
        width = (BUTTON_WIDTH * 2) + BUTTON_GAP
        file_x = WINDOW_WIDTH - width - 150
        self._file_ui = ButtonBarUI(self._screen, file_x, 15,
                        (SAVE_ICON, SAVE_ICON_HOVER, save_fn),
                                (LOAD_ICON, LOAD_ICON_HOVER, load_fn),
                                (METEOR_ICON, METEOR_ICON_HOVER, meteor_fn))
        self._stats_ui = StatsUI(self._screen, self._change_view_to_modal, world)
        self._settings_ui = SettingsUI(self._screen, slider_fns)

        self._view_modal_ui = ModalUI(self._screen,
                                      self.change_view_to_game, world)

        self._game_components = [self._playback_ui, self._file_ui,
                                 self._stats_ui,
                                 self._settings_ui]
        self._view_modal_components = [self._view_modal_ui]
        self._components = self._game_components


    def _draw_game_view(self):
        self._screen.fill(WINDOW_BG)
        self._render_title()
        self._draw_world_border()

        for component in self._game_components:
            component.draw()

        self._render_grid()


    def _draw_world_border(self):
        """Draws the border around the world"""
        pygame.draw.rect(self._screen, WORLD_BORDER_COLOR,
                         (WORLD_X - BORDER_WIDTH,
                          WORLD_Y - BORDER_WIDTH,
                          self._grid_size * self._cols + BORDER_WIDTH * 2,
                          self._grid_size * self._rows + BORDER_WIDTH * 2),
                         border_radius=5)

    def _render_grid(self):
        """Draws the world grid"""
        # Draw everything to _render_surface instead of screen
        # If the grid locations are floats, Pygame leaves uneven gaps/lines
        # between the rects. _render_surface is a larger area, enabling all
        # calculations to be made with integers. The _render_surface gets
        # scaled down/placed at the same location, but doesn't show gaps/lines.

        # Draw the world background to the scaled up render_surface
        self._render_surface.fill(
            self._world.get_environment().get_environment_color())

        for row in range(self._rows):
            for col in range(self._cols):
                organism = self._world.get_cell(row, col)
                if organism:
                    self._draw_organism(organism, row, col)

        scaled_surface = pygame.transform.scale(
            self._render_surface,
            (WORLD_WIDTH, WORLD_HEIGHT)
        )
        self._screen.blit(scaled_surface, (WORLD_X, WORLD_Y))


    def update(self):
        """
        Draws the components that need to be refreshed at each game iteration,
        the world grid and updated stats
        """
        self._render_grid()
        self._stats_ui.render_statistics()

    def _draw_organism(self, organism, row: int, col: int):
        """Helper method to draw an organism"""
        color = organism.get_color()

        # Draw as a square
        rect = self._convert_cell_to_rect(row, col)
        pygame.draw.rect(self._render_surface, color, rect)


    def _convert_cell_to_rect(self, row: int, col: int):
        """Helper method to convert row/col to a rect using screen coords"""
        # Positions are relative to _render_surface, since they are not
        # being directly drawn to self._screen
        scaled_grid_size = self._grid_size * self._render_scale
        return (col * scaled_grid_size,
                row * scaled_grid_size,
                scaled_grid_size, scaled_grid_size)

    def _render_title(self):
        """Draws the game title to the screen"""
        x_center = WORLD_X / 2 + BUTTON_HEIGHT
        y_center = 60
        font = pygame.font.SysFont(TITLE_FONT_NAME, TITLE_FONT_SIZE)
        render_text(GAME_TITLE, font, TITLE_TEXT,
                    x_center, y_center, self._screen)

    def _handle_grid_click(self) -> bool:
        """
        Checks if a user clicks on an organism in the grid.
        If an organism is clicked, switches to view species view.
        """
        x, y = pygame.mouse.get_pos()
        if (x >= WORLD_X and x <= WORLD_X + WORLD_WIDTH and y >= WORLD_Y and
            y <= WORLD_Y + WORLD_HEIGHT):
            row = int((y - WORLD_Y) / self._grid_size)
            col = int((x - WORLD_X) / self._grid_size)
            organism = self._world.get_cell(row, col)
            if organism and str(organism.get_genome().get_creature_type()) != "CreatureType.OBJECT":
                self._change_view_to_modal(organism_view=True, organism=organism)
                return True
            return False

    def handle_click(self):
        """Handles click events for all the UI components"""
        if not self._viewing_modal and self._handle_grid_click():
            return
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
        # First ensure that the modal closes properly if it is open
        # keyboard commands P,M,L,R should interrupt the modal and close it
        if self._viewing_modal:
            self.change_view_to_game()
        self._playback_ui.update_playback_state(playbackState)

    def _change_view_to_modal(self, organism_view=False, organism=None):
        """Toggles the view state between GAME And MODAL"""
        self._pause_fn() # make sure game is paused BEFORE _viewing_modal True
        self._viewing_modal = True
        self._components = self._view_modal_components
        if not organism_view:
            self._view_modal_ui.draw()
        else:
            self._view_modal_ui.draw_organism_view(organism)

    def change_view_to_game(self):
        """Changes from modal view to game view, redrawing the game view"""
        self._viewing_modal = False
        self._components = self._game_components # happens in init game view
        self._draw_game_view()

    def get_screen(self):
        """Getter method to return screen"""
        return self._screen