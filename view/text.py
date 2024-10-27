import pygame

from view.constants import STATS_FONT_SIZE, FONT_NAME, STATS_COLOR, STATS_X


def render_text(text, font, color, x_center, y_center, screen):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x_center, y_center))
    screen.blit(surface, rect)

def render_stat_text(title, value, y, screen):
    font = pygame.font.SysFont(FONT_NAME, STATS_FONT_SIZE)
    x = STATS_X
    surface = font.render(f"{title}: {value}", True, STATS_COLOR)
    rect = surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)
    return rect.height