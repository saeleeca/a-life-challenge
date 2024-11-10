import pygame

from view.components.button import Button
from view.constants import WINDOW_BG, WINDOW_HEIGHT, WINDOW_WIDTH, \
    VIEW_GENOMES_X, VIEW_GENOMES_Y, VIEW_GENOMES_HEIGHT, VIEW_GENOMES_WIDTH, \
    LIGHT_GREY_2, BUTTON_WIDTH, EXIT_ICON_HOVER, \
    EXIT_ICON, TITLE_FONT_NAME, BUTTON_HEIGHT, VIEW_SPECIES_TITLE, \
    VIEW_SPECIES_FONT_SIZE, TITLE_TEXT, PREV_ICON, PREV_ICON_HOVER, NEXT_ICON, \
    NEXT_ICON_HOVER, BUTTON_GAP, STATS_COLOR, FONT_NAME, STATS_FONT_SIZE, \
    VIEW_ORGANISM_TITLE
from view.sections.buttonBarUI import ButtonBarUI
from view.sections.uiComponent import UiComponent
from view.text import render_text, render_text_pair


class ModalUI(UiComponent):
    """Displays a modal view for view genomes/species and organisms"""
    def __init__(self, screen, exit_fn, world):
        super().__init__()
        self._screen = screen
        self._exit_fn = exit_fn
        self._world = world
        self._species_idx: int = 0

        exit_button_padding: int= 20
        exit_button_x: int = (VIEW_GENOMES_X + VIEW_GENOMES_WIDTH -
                         BUTTON_WIDTH - exit_button_padding)
        exit_button_y: int = VIEW_GENOMES_Y + exit_button_padding

        self._exit_button: Button = Button(exit_button_x, exit_button_y,
                                           EXIT_ICON, EXIT_ICON_HOVER,
                                           self._screen, exit_fn)

        self._genome_data_height: int = 0

    def draw_organism_view(self, organism):
        """
        Draws the Organism View modal:
        Same as Species View, but with a different title, and only the Exit btn
        """
        self._draw_background()
        self._draw_title(False)
        self._draw_modal_data(False, organism)
        self._exit_button.draw()
        self._buttons = [self._exit_button]


    def draw(self):
        """
        Draws the Species View modal:
        Has a title, Prev, Next and Exit buttons
        """
        self._species_idx = 0
        self._draw_background()
        self._draw_title(True)
        self._draw_modal_data()

        def next_fn():
            # use hardcoded data for now
            self._species_idx = (self._species_idx + 1) % 3
            # self._genome_num = self._genome_num + 1 % len(self._world.get_genome_data())
            self._draw_modal_data()
        def prev_fn():
            # use hardcoded data for now
            self._species_idx = (self._species_idx - 1) % 3
            # self._genome_num = self._genome_num - 1 % len(self._world.get_genome_data())
            self._draw_modal_data()

        arrows = ButtonBarUI(self._screen, (WINDOW_WIDTH / 2) - (BUTTON_WIDTH + BUTTON_GAP / 2),
                    VIEW_GENOMES_Y + 100,
                    (PREV_ICON, PREV_ICON_HOVER, prev_fn),
                    (NEXT_ICON, NEXT_ICON_HOVER, next_fn))
        self._buttons = arrows._buttons + [self._exit_button]
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

    def _draw_title(self, is_species_view=True):
        x_center = WINDOW_WIDTH / 2
        y_center = VIEW_GENOMES_Y + BUTTON_HEIGHT
        font = pygame.font.SysFont(TITLE_FONT_NAME, VIEW_SPECIES_FONT_SIZE)
        if is_species_view:
            render_text(VIEW_SPECIES_TITLE, font, TITLE_TEXT,
                        x_center, y_center, self._screen)
        else:
            render_text(VIEW_ORGANISM_TITLE, font, TITLE_TEXT,
                        x_center, y_center, self._screen)

    def _draw_modal_data(self, is_species_view=True, organism=None):
        y = VIEW_GENOMES_Y + 200
        original_y = y

        # remove old data
        pygame.draw.rect(self._screen, WINDOW_BG,
                     (VIEW_GENOMES_X, y, VIEW_GENOMES_WIDTH,
                      self._genome_data_height))

        data = organism.get_data() if not is_species_view \
            else self._world.get_species_data()[self._species_idx]

        # Drawing Organism/Species data in top part of the modal
        for key, value in data.items():
            if key == "Genome":
                continue
            y += render_text_pair(key, value, y, self._screen,
                                  VIEW_GENOMES_X + 100)

        y += 30 # spacing before genome data

        genome = data.get("Genome", {})
        # Draw Genome data
        for key, value in genome.items():
            if key == "Color":
                continue
            y += render_text_pair(key, value, y, self._screen, VIEW_GENOMES_X + 100)

        self._genome_data_height = y - original_y

        self._draw_genome_organism(genome)

    def _draw_genome_organism(self, data):
        color = data["Color"]
        organism_width = 100
        center_x = VIEW_GENOMES_X + (VIEW_GENOMES_WIDTH * .75)

        # "Appearance text above organism"
        font = pygame.font.SysFont(FONT_NAME, STATS_FONT_SIZE)
        render_text("Appearance:", font, STATS_COLOR, center_x,
                    VIEW_GENOMES_Y + 230, self._screen)


        rect = (center_x - (organism_width / 2),
                VIEW_GENOMES_Y + 260,
                organism_width, organism_width)
        pygame.draw.rect(self._screen, color, rect)

    def handle_click_event(self) -> bool:
        # button should not be hovered, next time it is viewed
        self._exit_button.reset()
        return super().handle_click_event()