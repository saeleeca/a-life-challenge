import pygame

from view.constants import STATS_FONT_SIZE, FONT_NAME, STATS_COLOR, STATS_X


def render_text(text: str, font, color: (int, int, int), x: float, y: float,
                screen, isCenter=True) -> int:
    """Helper function to draw text to the screen"""
    surface = font.render(text, True, color)
    if isCenter:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)
    return rect.width

def render_text_pair(title: str, value: int, y: float, screen) -> int:
    """Helper function to draw a title value pair to the screen"""
    font = pygame.font.SysFont(FONT_NAME, STATS_FONT_SIZE)
    x = STATS_X
    surface = font.render(f"{title}: {value}", True, STATS_COLOR)
    rect = surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)
    return rect.height