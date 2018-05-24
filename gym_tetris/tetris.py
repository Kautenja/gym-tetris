"""Methods for spawning and interacting with a Tetris game."""
from .template import PIECES, TEMPLATEHEIGHT, TEMPLATEWIDTH
from .palette import (
    BGCOLOR,
    BORDERCOLOR,
    TEXTCOLOR,
    TEXTSHADOWCOLOR,
    COLORS,
    LIGHTCOLORS,
    PALETTE
)


# the value denoting a blank pixel in a template
BLANK = '.'
# the frequency with which a piece can move sideways
MOVESIDEWAYSFREQ = 0.15
# the frequency with which a piece can move downwards
MOVEDOWNFREQ = 0.1
