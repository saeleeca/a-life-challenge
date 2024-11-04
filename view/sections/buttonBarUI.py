from typing import Callable

from view.components.button import Button
from view.constants import *
from view.sections.uiComponent import UiComponent


class ButtonBarUI(UiComponent):
    """Creates a horizontal row of buttons that handles click/hover events"""
    def __init__(self, screen, x: float, y: float,
                 *buttons: (str, str, Callable)):
        # each button in buttons is a tuple with icon, hover_icon, click fn
        # Create a Button for each tuple in *buttons and add to _buttons arr
        super().__init__()
        for icon, hover_icon, callback in buttons:
            button_obj = Button(x, y, icon, hover_icon, screen, callback)
            self._buttons.append(button_obj)
            button_obj.draw()
            x += BUTTON_WIDTH + BUTTON_GAP

    def draw(self):
        for button in self._buttons:
            button.draw()
