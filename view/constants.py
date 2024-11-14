from enum import Enum

# SIZES
# CHANGING SIZES CAN BREAK THE UI (MIGHT NEED TO CHANGE OTHER SIZES/POSITIONS)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WORLD_WIDTH = WORLD_HEIGHT = 600
BUTTON_WIDTH = 75
BUTTON_HEIGHT = 35
BUTTON_GAP = 40
BORDER_WIDTH = 6

VIEW_GENOMES_WIDTH = 800
VIEW_GENOMES_HEIGHT = 600

SLIDER_HEIGHT = 10
SLIDER_WIDTH = 200
SLIDER_RADIUS = 10

#LOCATIONS
WORLD_X = 560
WORLD_Y = 80

STATS_X = 75
STATS_Y = 150
STATS_PADDING_Y = 20

VIEW_GENOMES_X = 200
VIEW_GENOMES_Y = 100

# COLORS
# COLOR SCHEME
RED_ACCENT = (230, 57, 70)
OFF_WHITE = (241, 250, 238)
DARK_BLUE = (29, 53, 87)
MID_BLUE = (69,123, 157)
LIGHT_BLUE = (168, 218, 220)
DARK_GREY = (44, 47, 51)
LIGHT_GREY = "grey"
LIGHT_GREY_2 = (144, 147, 151)

WORLD_BG = LIGHT_GREY
WINDOW_BG = DARK_GREY
BUTTON_BG = OFF_WHITE
BUTTON_HOVER_BG = MID_BLUE
TITLE_TEXT = OFF_WHITE
INSTRUCTIONS_TEXT = OFF_WHITE
BUTTON_BORDER_COLOR = OFF_WHITE
WORLD_BORDER_COLOR = OFF_WHITE
STATS_COLOR = LIGHT_BLUE

SLIDER_TRACK = LIGHT_BLUE
SLIDER_CIRCLE = MID_BLUE


# TEXT
GAME_TITLE = "A-LIFE OSU"
INSTRUCTIONS = "P to Pause/Play - Q to Quit - R to Restart - S to Save - L to Load - M to Meteor"
VIEW_SPECIES_TITLE = "VIEW SPECIES"
VIEW_ORGANISM_TITLE = "VIEW ORGANISM"

TITLE_FONT_SIZE = 60
TITLE_FONT_NAME = "Verdana"
FONT_NAME = "Verdana"
STATS_FONT_SIZE = 22
VIEW_SPECIES_FONT_SIZE = 40

# ICONS
PLAY_ICON = "./view/icons/play_arrow_blue.png"
PLAY_ICON_HOVER = "./view/icons/play_arrow_off_white.png"
PAUSE_ICON = "./view/icons/pause_blue.png"
PAUSE_ICON_HOVER = "./view/icons/pause_off_white.png"
STEP_ICON = "./view/icons/skip_next_blue.png"
STEP_ICON_HOVER = "./view/icons/skip_next_off_white.png"
RESTART_ICON = "./view/icons/restart_blue.png"
RESTART_ICON_HOVER = "./view/icons/restart_off_white.png"

SAVE_ICON = "./view/icons/save_blue.png"
SAVE_ICON_HOVER = "./view/icons/save_off_white.png"
LOAD_ICON = "./view/icons/open_blue.png"
LOAD_ICON_HOVER = "./view/icons/open_off_white.png"

GENETICS_ICON = "./view/icons/genetics_blue.png"
GENETICS_ICON_HOVER = "./view/icons/genetics_off_white.png"

EXIT_ICON = "./view/icons/close_blue.png"
EXIT_ICON_HOVER = "./view/icons/close_off_white.png"
PREV_ICON = "./view/icons/arrow_back_blue.png"
PREV_ICON_HOVER = "./view/icons/arrow_back_off_white.png"
NEXT_ICON = "./view/icons/arrow_forward_blue.png"
NEXT_ICON_HOVER = "./view/icons/arrow_forward_off_white.png"

CHECK_ICON = "./view/icons/check_circle_blue.png"
CHECK_ICON_HOVER = "./view/icons/check_circle_off_white.png"


METEOR_ICON = "./view/icons/star_blue.png"
METEOR_ICON_HOVER = "./view/icons/star.png"


class ButtonEvent(Enum):
    PLAY = 1
    PAUSE = 2
    STEP = 3
    RESET = 4
    SAVE = 5
    LOAD = 6
    GENETICS = 7
    SPEED = 8
    SKIP = 9