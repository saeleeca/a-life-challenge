import pygame

from view.components.button import Button
from view.constants import WINDOW_BG, WINDOW_HEIGHT, WINDOW_WIDTH, \
    VIEW_GENOMES_X, VIEW_GENOMES_Y, VIEW_GENOMES_HEIGHT, VIEW_GENOMES_WIDTH, \
    LIGHT_GREY_2, BUTTON_WIDTH, EXIT_ICON_HOVER, \
    EXIT_ICON, TITLE_FONT_NAME, BUTTON_HEIGHT, VIEW_GENOMES_TITLE, \
    VIEW_GENOMES_FONT_SIZE, TITLE_TEXT
from view.sections.uiComponent import UiComponent
from view.text import render_text


class ViewGenomeUI(UiComponent):
    """Displays a new view in the Pygame window for view genomes"""
    def __init__(self, screen, exit_fn):
        super().__init__()
        self._screen = screen
        self._exit_fn = exit_fn

        exit_button_padding = 20
        exit_button_x = (VIEW_GENOMES_X + VIEW_GENOMES_WIDTH -
                         BUTTON_WIDTH - exit_button_padding)
        exit_button_y = VIEW_GENOMES_Y + exit_button_padding

        self._exit_button: Button = Button(exit_button_x, exit_button_y,
                                           EXIT_ICON, EXIT_ICON_HOVER,
                                           self._screen, exit_fn)
        self._buttons.append(self._exit_button)


    def draw(self):
        self._draw_background()
        self._draw_title()
        for button in self._buttons:
            button.draw()

    def _draw_background(self):
        # Cover the entire background
        background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT),
                                            pygame.SRCALPHA)
        alpha_value = 200
        background_surface.fill((*LIGHT_GREY_2, alpha_value))
        self._screen.blit(background_surface, (0, 0))

        # Draw "modal" window
        modal_rect = (VIEW_GENOMES_X, VIEW_GENOMES_Y,
                      VIEW_GENOMES_WIDTH, VIEW_GENOMES_HEIGHT)
        pygame.draw.rect(self._screen, WINDOW_BG, modal_rect)

    def _draw_title(self):
        x_center = WINDOW_WIDTH / 2
        y_center = VIEW_GENOMES_Y + BUTTON_HEIGHT
        font = pygame.font.SysFont(TITLE_FONT_NAME, VIEW_GENOMES_FONT_SIZE)
        render_text(VIEW_GENOMES_TITLE, font, TITLE_TEXT,
                    x_center, y_center, self._screen)

    def handle_click_event(self) -> bool:
        # button should not be hovered, next time it is viewed
        self._exit_button.reset()
        return super().handle_click_event()