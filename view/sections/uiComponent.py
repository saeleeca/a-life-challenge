import pygame


class UiComponent:
    """Parent UI section class, shared logic that handles the buttons"""
    def __init__(self):
        self._buttons: list = []

    def handle_click_event(self) -> bool:
        """Check each button for click"""
        for button in self._buttons:
            if button.detect_mouse_collision(pygame.mouse.get_pos()):
                button.handle_click()
                return True
        return False

    def handle_hover_event(self) -> bool:
        """Check each button for hover"""
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
    def draw(self):
        """Each child class will implement a draw method"""
        pass