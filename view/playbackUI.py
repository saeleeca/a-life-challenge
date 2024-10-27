import pygame.sprite

from view.button import Button
from view.buttonBarUI import ButtonBarUI
from view.constants import *
from view.text import render_text


class PlaybackUI(ButtonBarUI):
    def __init__(self, screen):
        self._is_paused = True
        center_x = WORLD_X + (WINDOW_WIDTH - WORLD_X) / 2
        width = (BUTTON_WIDTH * 3) + (BUTTON_GAP * 2)
        x = center_x - width / 2
        y = WORLD_HEIGHT + WORLD_Y + 20

        super().__init__(screen, x, y,
                         (PLAY_ICON, PLAY_ICON_HOVER, ButtonEvent.PLAY),
                         (STEP_ICON, STEP_ICON_HOVER, ButtonEvent.STEP),
                         (RESTART_ICON, RESTART_ICON_HOVER, ButtonEvent.RESET))

        self._play_button = self._buttons[0]

        self._pause_button = Button(x, y, PAUSE_ICON, PAUSE_ICON_HOVER,
                                    ButtonEvent.PAUSE, screen)

        self._step_button = self._buttons[1]
        self._restart_button = self._buttons[2]

        self._draw_instructions(screen)

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
                self._play_button.handle_hover()
            else:
                self._play_button.handle_end_hover()
            self._buttons[0] = self._play_button
        self._buttons[0].draw()
        self._is_paused = not self._is_paused

        pygame.display.update()

    def handle_click_event(self):
        for button in self._buttons:
            if button.detect_mouse_collision(pygame.mouse.get_pos()):
                click_type = button.handle_click()
                # Toggle the play and pause icon if they were clicked
                if (click_type == ButtonEvent.PLAY or
                        click_type == ButtonEvent.PAUSE):
                    self._toggle_play_pause()
                # Clicking on step when the game is playing, switches to pause
                elif click_type == ButtonEvent.STEP and not self._is_paused:
                    self._play_button.reset()
                    self._toggle_play_pause()

                # The controller will see the returned click type and choose
                # the correct action
                return click_type
        return None

    def update_playback_state(self, playback_state):
        if playback_state == ButtonEvent.PLAY and self._is_paused:
            self._toggle_play_pause()
        elif playback_state == ButtonEvent.PAUSE and not self._is_paused:
            self._toggle_play_pause()
        elif playback_state == ButtonEvent.STEP and not self._is_paused:
            self._play_button.reset()
            self._toggle_play_pause()

    @staticmethod
    def _draw_instructions(screen):
        font = pygame.font.SysFont(TITLE_FONT_NAME, 20)
        x_center = WORLD_X + (WINDOW_WIDTH - WORLD_WIDTH) / 2
        y_center = WORLD_HEIGHT + WORLD_Y + 60 + BUTTON_HEIGHT
        render_text(INSTRUCTIONS, font, INSTRUCTIONS_TEXT, x_center, y_center,
                    screen)

        pygame.display.update()
