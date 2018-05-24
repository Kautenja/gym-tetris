"""The dimensions for various parts of the game."""


# The width of images rendered by the NES
SCREEN_WIDTH = 330
# The height of images rendered by the NES
SCREEN_HEIGHT = 430
# the number of pixels to use for a box
BOXSIZE = 20
# the number of horizontal boxes on the board (classic Tetris uses 10)
BOARDWIDTH = 10
# the number of vertical boxes on the board (classic Tetris uses 20)
BOARDHEIGHT = 20
# the number of pixels to pad the game from the right border of the screen
XMARGIN = 10
# the number of pixels to pad the game from the top border of the screen
TOPMARGIN = 20
# the dimensions of the border rectangle
BORDER_DIMS = (
    XMARGIN - 5,
    TOPMARGIN - 5,
    BOARDWIDTH * BOXSIZE + 10,
    BOARDHEIGHT * BOXSIZE + 10
)
# the dimensions of the background rectangle
BG_DIMS = (
    XMARGIN,
    TOPMARGIN,
    BOXSIZE * BOARDWIDTH,
    BOXSIZE * BOARDHEIGHT
)


# the x position for status items
STATUS_X = BORDER_DIMS[2] + 15
# the Y position for the "score" static label
SCORE_LABEL_Y = BORDER_DIMS[0] + 15
# the Y position for the score status
SCORE_Y = SCORE_LABEL_Y + 30
# the Y position for the "level" static label
LEVEL_LABEL_Y = SCORE_Y + 30
# the Y position for the level status
LEVEL_Y = LEVEL_LABEL_Y + 30
# the Y position for the "next" label
NEXT_LABEL_Y = LEVEL_Y + 30
# the Y position for the next piece preview
NEXT_Y = NEXT_LABEL_Y + 30
