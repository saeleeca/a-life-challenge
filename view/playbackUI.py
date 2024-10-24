from enum import Enum
from view.constants import *
import pygame.sprite

from view.button import Button


class PlaybackState(Enum):
    PLAY = 1
    PAUSE = 2
    STEP = 3
    RESET = 4


class PlaybackUI:
    def __init__(self, screen):
        self._is_paused = True
        self._buttons = pygame.sprite.Group()

        width = (BUTTON_WIDTH * 3) + (BUTTON_GAP * 2)
        self._start_x = WORLD_X + width / 2

        step_x = self._start_x + BUTTON_WIDTH + BUTTON_GAP
        restart_x = step_x + BUTTON_WIDTH + BUTTON_GAP

        y = WORLD_HEIGHT + WORLD_Y + 20

        self._play_button = Button(self._start_x, y,
                                   PLAY_ICON, PLAY_ICON_HOVER,
                                   PlaybackState.PLAY, screen)
        self._pause_button = Button(self._start_x, y, PAUSE_ICON,
                                    PAUSE_ICON_HOVER,
                                    PlaybackState.PAUSE, screen)

        self._step_button = Button(step_x, y, STEP_ICON, STEP_ICON_HOVER,
                                   PlaybackState.STEP, screen)

        self._restart_button = Button(restart_x, y, RESTART_ICON,
                                      RESTART_ICON_HOVER, PlaybackState.RESET,
                                      screen)

        self._buttons = [self._play_button,
                         self._step_button, self._restart_button]

        for button in self._buttons:
            button.draw()

    def _toggle_play_pause(self):
        # Game is paused, so switch to play
        if self._is_paused:
            # When game is in play mode, the pause icon is displayed
            # First copy hover state (button would be hovered if user clicked
            # it, but if they used keyboard commands, clicked step it shouldn't
            # be hovered)
            if self._buttons[0].get_hover_state():
                self._pause_button.handle_hover()
            else:
                self._pause_button.handle_end_hover()
            self._buttons[0] = self._pause_button
        else:
            # When game is paused, the play icon is displayed
            # First copy hover state
            if self._buttons[0].get_hover_state():
                self._pause_button.handle_hover()
            else:
                self._pause_button.handle_end_hover()
            self._buttons[0] = self._play_button
        self._buttons[0].draw()
        self._is_paused = not self._is_paused

        pygame.display.update()

    def handle_click_event(self):
        for button in self._buttons:
            if button.detect_mouse_collision(pygame.mouse.get_pos()):
                click_type = button.handle_click()
                # Toggle the play and pause icon if they were clicked
                if (click_type == PlaybackState.PLAY or
                    click_type == PlaybackState.PAUSE):
                    self._toggle_play_pause()
                # Clicking on step when the game is playing, switches to pause
                elif click_type == PlaybackState.STEP and not self._is_paused:
                    self._play_button.reset()
                    self._toggle_play_pause()

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

    def update_playback_state(self, playback_state):
        if playback_state == PlaybackState.PLAY and self._is_paused:
            self._toggle_play_pause()
        elif playback_state == PlaybackState.PAUSE and not self._is_paused:
            self._toggle_play_pause()
        elif playback_state == PlaybackState.STEP and not self._is_paused:
            self._play_button.reset()
            self._toggle_play_pause()