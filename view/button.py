import pygame
from view.constants import *

class Button:
    def __init__(self, x, y, icon_filename, hover_icon_filename, playbackType, screen):
        super().__init__()
        self._image = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
        self._image.fill(BUTTON_BG)
        self._rect = self._image.get_rect(topleft=(x, y))
        self._icon = self._load_icon(icon_filename)
        self._action = playbackType
        self._screen = screen
        self._icon_filename = icon_filename
        self._hover_icon_filename = hover_icon_filename
        self._is_hover = False


    @staticmethod
    def _load_icon(filename):
        try:
            icon = pygame.image.load(filename)
            icon = pygame.transform.scale(
                icon,
            (BUTTON_WIDTH // 1.3, BUTTON_HEIGHT // 1.3))
            return icon
        except pygame.error as e:
            print(f"Error loading icon: {filename}. Error: {e}")
            return None
        except TypeError as e:
            print(f"TypeError loading icon: {filename}. Error: {e}")
            return None
        except FileNotFoundError as e:
            print(f"FileNotFoundError loading icon: {filename}. Error: {e}")
            return None


    def detect_mouse_collision(self, mouse_position):
        return self._rect.collidepoint(mouse_position)

    def handle_click(self):
        return self._action

    def _toggle_hover(self):
        self._is_hover = not self._is_hover

    def handle_hover(self):
        # Already hovering on the button, so skip
        if self._is_hover:
            return
        self._toggle_hover()
        self._image.fill(BUTTON_HOVER_BG)
        self._icon = self._load_icon(self._hover_icon_filename)

    def get_hover_state(self):
        return self._is_hover

    def reset(self):
        if self._is_hover:
            self.handle_end_hover()

    def handle_end_hover(self):
        if not self._is_hover:
            return
        self._toggle_hover()
        self._image.fill(BUTTON_BG)
        self._icon = self._load_icon(self._icon_filename)

    def draw(self):
        self._screen.blit(self._image, self._rect)
        if self._icon:
            border_rect = self._rect.inflate(6,
                                             6)
            pygame.draw.rect(self._screen, BUTTON_BORDER_COLOR, border_rect,
                             width=4, border_radius=4)

            icon_rect = self._icon.get_rect(center=self._rect.center)
            self._screen.blit(self._icon, icon_rect)
