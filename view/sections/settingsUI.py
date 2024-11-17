from view.constants import WINDOW_HEIGHT, STATS_X, ButtonEvent
from view.components.slider import Slider


class SettingsUI:
    """Handles drawing and updating the settings in the UI"""

    def __init__(self, screen, slider_fns):
        self._screen = screen
        y = WINDOW_HEIGHT - 140
        self._speed_slider = Slider(STATS_X, y, screen,
                                    1, 100, 50,
                                    "Game Speed",
                                    slider_fns.get("speed"))
        self._mutation_slider = Slider(STATS_X, y + 40, screen,
                                       1, 100, 1,
                                       "Mutation Rate")
        self._skip_slider = Slider(STATS_X, y + 80, screen, 1,
                                   30, 1,
                                   "Iterations per frame",
                                   slider_fns.get("iterations"))

    def handle_click_event(self) -> bool:
        """Checks each slider for click, stops if triggered"""
        return (self._speed_slider.handle_click_event() or
                self._skip_slider.handle_click_event() or
                self._mutation_slider.handle_click_event())

    def handle_hover_event(self) -> bool:
        """Checks each slider for mouse move update, stops if triggered"""
        return (self._speed_slider.handle_mouse_move() or
                self._skip_slider.handle_mouse_move() or
                self._mutation_slider.handle_mouse_move())

    def handle_mouse_up(self):
        """Checks each slider for mouse up if updating, stops if triggered"""
        (self._speed_slider.handle_mouse_up() or
         self._skip_slider.handle_mouse_up() or
         self._mutation_slider.handle_mouse_up())

    def draw(self):
        self._speed_slider.draw()
        self._skip_slider.draw()
        self._mutation_slider.draw()
