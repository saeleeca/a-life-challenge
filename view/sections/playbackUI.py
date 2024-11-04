import pygame.sprite

from view.components.button import Button
from view.sections.buttonBarUI import ButtonBarUI
from view.constants import *
from view.text import render_text


class PlaybackUI(ButtonBarUI):
    """
    Creates a horizontal row of playback buttons (start/pause, step, restart)
    with click/hover events and instructions
    """
    def __init__(self, screen, start_fn, pause_fn, reset_fn, step_fn):
        self._screen = screen
        self._is_paused: bool = True
        center_x = WORLD_X + WORLD_WIDTH / 2
        width = (BUTTON_WIDTH * 3) + (BUTTON_GAP * 2)
        x = center_x - width / 2
        y = WORLD_HEIGHT + WORLD_Y + 20

        super().__init__(screen, x, y,
                         (PLAY_ICON, PLAY_ICON_HOVER, start_fn),
                         (STEP_ICON, STEP_ICON_HOVER, step_fn),
                         (RESTART_ICON, RESTART_ICON_HOVER, reset_fn))

        self._play_button: Button = self._buttons[0]
        self._pause_button: Button = Button(x, y, PAUSE_ICON, PAUSE_ICON_HOVER,
                                    screen, pause_fn)
        self._step_button: Button = self._buttons[1]
        self._restart_button: Button = self._buttons[2]

        self._draw_instructions(screen)

    def _toggle_play_pause(self):
        """Switches from play to pause or pause to play"""
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


    def update_playback_state(self, playback_state: ButtonEvent):
        """
        Updates the ui to play/pause depending on playback_state event.
        Triggered from outside the class, like if keyboard commands are used
        """
        if playback_state == ButtonEvent.PLAY and self._is_paused:
            self._toggle_play_pause()
        elif playback_state == ButtonEvent.PAUSE and not self._is_paused:
            self._toggle_play_pause()
        elif playback_state == ButtonEvent.STEP and not self._is_paused:
            self._play_button.reset()
            self._toggle_play_pause()

    @staticmethod
    def _draw_instructions(screen):
        """Draws the playback instructions"""
        font = pygame.font.SysFont(TITLE_FONT_NAME, 20)
        x_center = WORLD_X + WORLD_WIDTH / 2
        y_center = WORLD_HEIGHT + WORLD_Y + 60 + BUTTON_HEIGHT
        render_text(INSTRUCTIONS, font, INSTRUCTIONS_TEXT, x_center, y_center,
                    screen)

        pygame.display.update()

    def draw(self):
        self._draw_instructions(self._screen)
        for button in self._buttons:
            button.draw()
