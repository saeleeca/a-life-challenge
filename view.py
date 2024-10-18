import pygame.draw


class View:
    def __init__(self, width: int, height: int, rows: int, cols: int, world, screen, grid_size: int):
        self._width: int = width
        self._height: int = height
        self._rows: int = rows
        self._cols: int = cols
        self._world = world
        self._screen = screen
        self._grid_size: int = grid_size

    def render_grid(self):
        self._screen.fill("grey")

        for row in range(self._rows):
            for col in range(self._cols):
                organism = self._world.get_cell(row, col)
                if organism:
                    self._draw_organism(organism, row, col)

        pygame.display.flip()

    def _draw_organism(self, organism, row, col):
        color = organism.get_color()

        # Draw as a square
        rect = self._convert_cell_to_rect(row, col)
        pygame.draw.rect(self._screen, color, rect)

        # # Draw as a circle
        # center_row = row * self._grid_size + self._grid_size//2
        # center_col = col * self._grid_size + self._grid_size//2
        # center = (center_col, center_row)
        # radius = self._grid_size // 2
        # pygame.draw.circle(self._screen, color, center, radius)


    def _convert_cell_to_rect(self, row, col):
        return (col * self._grid_size, row * self._grid_size,
                self._grid_size, self._grid_size)