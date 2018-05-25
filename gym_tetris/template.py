"""Templates for Tetrominos."""


# the max width of a Tetromino
TEMPLATEWIDTH = 5
# the max height of a Tetromino
TEMPLATEHEIGHT = 5
# the sentinel denoting a blank box
BLANK = '.'


S_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '..OO.',
     '.OO..',
     '.....'],
    ['.....',
     '..O..',
     '..OO.',
     '...O.',
     '.....']
]


Z_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '.OO..',
     '..OO.',
     '.....'],
    ['.....',
     '..O..',
     '.OO..',
     '.O...',
     '.....']
]


I_SHAPE_TEMPLATE = [
    ['..O..',
     '..O..',
     '..O..',
     '..O..',
     '.....'],
    ['.....',
     '.....',
     'OOOO.',
     '.....',
     '.....']
]


O_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '.OO..',
     '.OO..',
     '.....']
]


J_SHAPE_TEMPLATE = [
    ['.....',
     '.O...',
     '.OOO.',
     '.....',
     '.....'],
    ['.....',
     '..OO.',
     '..O..',
     '..O..',
     '.....'],
    ['.....',
     '.....',
     '.OOO.',
     '...O.',
     '.....'],
    ['.....',
     '..O..',
     '..O..',
     '.OO..',
     '.....']
]


L_SHAPE_TEMPLATE = [
    ['.....',
     '...O.',
     '.OOO.',
     '.....',
     '.....'],
    ['.....',
     '..O..',
     '..O..',
     '..OO.',
     '.....'],
    ['.....',
     '.....',
     '.OOO.',
     '.O...',
     '.....'],
    ['.....',
     '.OO..',
     '..O..',
     '..O..',
     '.....']
]


T_SHAPE_TEMPLATE = [
    ['.....',
     '..O..',
     '.OOO.',
     '.....',
     '.....'],
    ['.....',
     '..O..',
     '..OO.',
     '..O..',
     '.....'],
    ['.....',
     '.....',
     '.OOO.',
     '..O..',
     '.....'],
    ['.....',
     '..O..',
     '.OO..',
     '..O..',
     '.....']
]


# a dictionary of piece names to templates
PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE
}
