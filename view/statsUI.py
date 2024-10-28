import pygame

from view.button import Button
from view.constants import WINDOW_BG, STATS_X, STATS_Y, BUTTON_HEIGHT, \
    STATS_PADDING_Y, FONT_NAME, STATS_FONT_SIZE, STATS_COLOR, GENETICS_ICON, \
    GENETICS_ICON_HOVER, ButtonEvent
from view.text import render_text_pair


class StatsUI:
    """Displays the Statistics text as a vertical list"""
    def __init__(self, screen):
        self._screen = screen
        self._view_genome_button: Button = self._render_view_genome()
        self._stats_height: int = 0

        self._render_view_genome()

    def _render_view_genome(self):
        """Displays the view genomes list item and button"""
        # text portion
        font = pygame.font.SysFont(FONT_NAME, STATS_FONT_SIZE)
        surface = font.render("View Genomes:", True, STATS_COLOR)
        rect = surface.get_rect(topleft=(STATS_X, STATS_Y))
        button_x = rect.right + 20
        self._screen.blit(surface, rect)
        button = Button(button_x, STATS_Y, GENETICS_ICON, GENETICS_ICON_HOVER,
                        ButtonEvent.GENETICS, self._screen)
        button.draw()
        return button

    def render_statistics(self):
        """Displays the statistics list"""
        # dummy values (will come from world when completed)
        statistics = {"Days": 100, "Population": 500, "Deaths": 1500,
            "No. of Species": 14, "Number of mutations": 7,
            "Total Offspring": 1497, "Generations (max)": 36, }
        y = STATS_Y + BUTTON_HEIGHT + STATS_PADDING_Y

        # Remove old stats from ui
        pygame.draw.rect(self._screen, WINDOW_BG,
                         (STATS_X, y, 450, self._stats_height - y))
        # Draw new stats
        for title, value in statistics.items():
            y += render_text_pair(title, value, y,
                                  self._screen) + STATS_PADDING_Y

        self._stats_height = STATS_Y + y    # save height for updating later

    def handle_hover_event(self) -> bool:
        """Handles hovering the view genomes button"""
        if self._view_genome_button.detect_mouse_collision(
                pygame.mouse.get_pos()):
            self._view_genome_button.handle_hover()
            self._view_genome_button.draw()
            pygame.display.update()
            return True
        elif self._view_genome_button.get_hover_state():
            self._view_genome_button.handle_end_hover()
            self._view_genome_button.draw()
            pygame.display.update()
            return True
        return False

    def handle_click_event(self) -> ButtonEvent | None:
        """Handles clicking the view genomes button"""
        if self._view_genome_button.detect_mouse_collision(
                pygame.mouse.get_pos()):
            return self._view_genome_button.handle_click()
        return None
