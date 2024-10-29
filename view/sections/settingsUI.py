from view.constants import WINDOW_HEIGHT, STATS_X, ButtonEvent
from view.components.slider import Slider


class SettingsUI:
    """Handles drawing and updating the settings in the UI"""
    def __init__(self, screen):
        self._screen = screen
        y = WINDOW_HEIGHT - 100
        self._speed_slider = Slider(STATS_X, y, screen,
                                    1, 30, 5,
                                    "Game Speed")
        self._skip_slider = Slider(STATS_X, y + 40, screen,
                                    1, 100, 1,
                                    "Iterations per frame")

    def handle_click_event(self) -> bool:
        """Checks each slider for click, stops if triggered"""
        return (self._speed_slider.handle_click_event() or
                self._skip_slider.handle_click_event())

    def handle_hover_event(self) -> bool:
        """Checks each slider for mouse move update, stops if triggered"""
        return (self._speed_slider.handle_mouse_move() or
         self._skip_slider.handle_mouse_move())


    def handle_mouse_up(self):
        """Checks each slider for mouse up if updating, stops if triggered"""
        (self._speed_slider.handle_mouse_up() or
                self._skip_slider.handle_mouse_up())