"""Color palette information for the Tetris game."""


WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
CYAN = (4, 216, 219)
LIGHT_CYAN = (3, 252, 255)
BLUE = (20, 27, 194)
LIGHT_BLUE = (25, 34, 251)
ORANGE = (202, 131, 24)
LIGHT_ORANGE = (250, 146, 0)
YELLOW = (218, 217, 42)
LIGHT_YELLOW = (255, 255, 0)
GREEN = (9, 220, 43)
LIGHT_GREEN = (61, 255, 0)
PURPLE = (133, 29, 200)
LIGHT_PURPLE = (146, 0, 255)
RED = (202, 34, 5)
LIGHT_RED = (246, 0, 0)


# the color of the game border
BORDERCOLOR = WHITE
# the background color for the game board
BGCOLOR = BLACK
# the color to use for text labels
TEXTCOLOR = WHITE
# the shadow color for text to give perspective
TEXTSHADOWCOLOR = GRAY
# the background color for Tetrominos
COLORS = (
    CYAN,
    BLUE,
    ORANGE,
    YELLOW,
    GREEN,
    PURPLE,
    RED
)
# the foreground color for Tetrominos
LIGHTCOLORS = (
    LIGHT_CYAN,
    LIGHT_BLUE,
    LIGHT_ORANGE,
    LIGHT_YELLOW,
    LIGHT_GREEN,
    LIGHT_PURPLE,
    LIGHT_RED
)
# The color palette for game pieces
PALETTE = {shape: index for index, shape in enumerate(list('IJLOSTZ'))}
