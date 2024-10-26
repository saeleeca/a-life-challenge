import pygame

from view.button import Button
from view.constants import *



class ButtonBarUI:
    def __init__(self, screen, x, y, *buttons: (str, str, ButtonEvent)):
        # each button is a tuple with icon, hover_icon, event
        self._buttons = []

        for icon, hover_icon, event in buttons:
            button_obj = Button(x, y, icon, hover_icon, event, screen)
            self._buttons.append(button_obj)
            button_obj.draw()
            x += BUTTON_WIDTH + BUTTON_GAP

    def handle_click_event(self):
        for button in self._buttons:
            if button.detect_mouse_collision(pygame.mouse.get_pos()):
                click_type = button.handle_click()
                # The controller will see the returned click type and choose
                # the correct action
                return click_type
        return None

    def handle_hover_event(self):
        # Note: Don't return/exit the loop if you update a button.
        # If the mouse moves fast it will skip an update
        for button in self._buttons:
            if button.detect_mouse_collision(pygame.mouse.get_pos()):
                button.handle_hover()
                button.draw()
                pygame.display.update()

            # If this button was previously hovered, but isn't anymore,
            # go back to the original color
            elif button.get_hover_state():
                button.handle_end_hover()
                button.draw()
                pygame.display.update()

        return False
