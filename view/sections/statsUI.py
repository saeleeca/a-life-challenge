import pygame

from view.components.button import Button
from view.constants import WINDOW_BG, STATS_X, STATS_Y, BUTTON_HEIGHT, \
    STATS_PADDING_Y, FONT_NAME, STATS_FONT_SIZE, STATS_COLOR, GENETICS_ICON, \
    GENETICS_ICON_HOVER
from view.text import render_text_pair
from view.sections.uiComponent import UiComponent


class StatsUI(UiComponent):
    """
    Displays the Statistics text as a vertical list and a view genomes button
    """
    def __init__(self, screen, view_genome_fn):
        super().__init__()
        self._screen = screen
        self._view_genome_button: Button = (
            self._render_view_genomes_btn(view_genome_fn))
        self._buttons.append(self._view_genome_button)
        self._stats_height: int = 0

    def _render_view_genomes_text(self):
        # text portion
        font = pygame.font.SysFont(FONT_NAME, STATS_FONT_SIZE)
        surface = font.render("View Genomes:", True, STATS_COLOR)
        rect = surface.get_rect(topleft=(STATS_X, STATS_Y))
        self._screen.blit(surface, rect)
        return rect

    def _render_view_genomes_btn(self, view_genome_fn):
        """Displays the view genomes list item and button"""
        rect = self._render_view_genomes_text()
        button_x = rect.right + 20
        button = Button(button_x, STATS_Y, GENETICS_ICON, GENETICS_ICON_HOVER,
                        self._screen, view_genome_fn)
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

    def draw(self):
        self.render_statistics()
        self._render_view_genomes_text()
        self._view_genome_button.draw()

    def handle_click_event(self) -> bool:
        # button should not be hovered, next time it is viewed
        self._view_genome_button.reset()
        return super().handle_click_event()
