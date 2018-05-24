"""An implementation of Tetris for OpenAI Gym using Pygame."""
import random, time, pygame, sys
from pygame.locals import (
    QUIT,
    KEYUP,
    KEYDOWN,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_a,
    K_d,
    K_q,
    K_s,
    K_w,
)


# the width of the main game window
SCREEN_WIDTH = 330
# the height of the main game window
SCREEN_HEIGHT = 430
# the number of pixels to use for a box
BOXSIZE = 20
# the number of horizontal boxes on the board (classic Tetris uses 10)
BOARDWIDTH = 10
# the number of vertical boxes on the board (classic Tetris uses 20)
BOARDHEIGHT = 20
# the value denoting a blank pixel in a template
BLANK = '.'


# TODO: document
MOVESIDEWAYSFREQ = 0.15
# TODO: document
MOVEDOWNFREQ = 0.1


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


# the label for the "Next" piece to come
NEXT_LABEL = 'Next'
# the label for the current level status
LEVEL_LABEL = 'Level'
# the label for the current score status
SCORE_LABEL = 'Score'
# the label for the press key
PRESS_KEY_LABEL = 'Press a key to play.'
# the label to indicate that the game is over
GAME_OVER_LABEL = 'Over'
# the label to indicate that the game is paused
GAME_PAUSE_LABEL = 'Pause'
# the label for the title screen and window
GAME_NAME_LABEL = 'Tetris'


# TODO: move color stuff to palette.py
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


# the max width of a Tetromino
TEMPLATEWIDTH = 5
# the max height of a Tetromino
TEMPLATEHEIGHT = 5


# TODO: move to templates.py

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


PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE
}


# an enumeration of actions in the game
ACTIONS = [
    'NOP',
    'LEFT',
    'RIGHT',
    'DOWN',
    'ROT_R',
    'ROT_L',
]


class Tetris():
    """An object oriented design of Tetris."""

    def __init__(self) -> None:
        """Initialize a new Tetris game."""
        # initialize pygame
        pygame.init()
        pygame.display.set_caption(GAME_NAME_LABEL)
        self._display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        # set the board as a blank board
        self.board = get_blank_board()
        # set the score to 0 and get the corresponding level and fall rate
        self.score = 0
        self.level, self.fall_freq = level_and_fall_frequency(self.score)
        # setup the initial pieces
        self.falling_piece = new_piece()
        self.next_piece = new_piece()
        # setup the initial times for movement restriction
        self.last_move_down_time = time.time()
        self.last_move_side_time = time.time()
        self.last_fall_time = time.time()

    def left(self) -> None:
        """Move the falling piece left on the board."""
        if is_valid_position(self.board, self.falling_piece, adj_x=-1):
            if time.time() - self.last_move_side_time < MOVESIDEWAYSFREQ:
                return
            self.falling_piece['x'] -= 1
            self.last_move_side_time = time.time()

    def right(self) -> None:
        """Move the falling piece right on the board."""
        if is_valid_position(self.board, self.falling_piece, adj_x=1):
            if time.time() - self.last_move_side_time < MOVESIDEWAYSFREQ:
                return
            self.falling_piece['x'] += 1
            self.last_move_side_time = time.time()

    def down(self) -> None:
        """Moving the falling piece down on the board."""
        if is_valid_position(self.board, self.falling_piece, adj_y=1):
            if time.time() - self.last_move_down_time < MOVEDOWNFREQ:
                return
            self.falling_piece['y'] += 1
            self.last_move_down_time = time.time()

    def rot_r(self) -> None:
        """Rotate the falling piece right on the board."""
        rots = len(PIECES[self.falling_piece['shape']])
        self.falling_piece['rotation'] = (self.falling_piece['rotation'] + 1) % rots
        # rotate back if the position is invalid
        if not is_valid_position(self.board, self.falling_piece):
            self.falling_piece['rotation'] = (self.falling_piece['rotation'] - 1) % rots

    def rot_l(self) -> None:
        """Rotate the falling piece left on the board."""
        rots = len(PIECES[self.falling_piece['shape']])
        self.falling_piece['rotation'] = (self.falling_piece['rotation'] - 1) % rots
        # rotate back if the position is invalid
        if not is_valid_position(self.board, self.falling_piece):
            self.falling_piece['rotation'] = (self.falling_piece['rotation'] + 1) % rots

    def step(self, action: int):
        """
        """
        if self.falling_piece is None:
            # No falling piece in play, so start a new piece at the top
            self.falling_piece = self.next_piece
            self.next_piece = new_piece()
            # can't fit a new piece on the board, so game over
            if not is_valid_position(self.board, self.falling_piece):
                return

        # TODO: handle action

        # return if it's not time to fall yet
        if time.time() - self.last_fall_time < self.fall_freq:
            return

        # see if the piece has landed
        if not is_valid_position(self.board, self.falling_piece, adj_y=1):
            # falling piece has landed, set it on the board
            add_to_board(self.board, self.falling_piece)
            self.score += remove_complete_lines(self.board)
            self.level, self.fall_freq = level_and_fall_frequency(self.score)
            self.falling_piece = None
        else:
            # piece did not land, just move the piece down
            self.falling_piece['y'] += 1
            self.last_fall_time = time.time()

    def __del__(self) -> None:
        """Close the pygame environment before deleting this object."""
        pygame.quit()


def main():
    a = Tetris()
    del a

    global DISPLAYSURF, BASICFONT
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    # update the name of the game
    pygame.display.set_caption(GAME_NAME_LABEL)
    # run the game loop
    while True:
        run_game()


def run_game():
    # setup variables for the start of the game
    board = get_blank_board()
    last_move_down_time = time.time()
    last_move_side_time = time.time()
    last_fall_time = time.time()
    moving_down = False
    moving_left = False
    moving_right = False
    score = 0
    level, fall_freq = level_and_fall_frequency(score)

    falling_piece = new_piece()
    next_piece = new_piece()

    # game loop
    while True:
        if falling_piece is None:
            # No falling piece in play, so start a new piece at the top
            falling_piece = next_piece
            next_piece = new_piece()
            # reset last_fall_time
            last_fall_time = time.time()

            # can't fit a new piece on the board, so game over
            if not is_valid_position(board, falling_piece):
                return

        # event handling loop
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
                elif event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                elif event.key == K_DOWN or event.key == K_s:
                    moving_down = False
            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and is_valid_position(board, falling_piece, adj_x=-1):
                    falling_piece['x'] -= 1
                    moving_left = True
                    moving_right = False
                    last_move_side_time = time.time()
                elif (event.key == K_RIGHT or event.key == K_d) and is_valid_position(board, falling_piece, adj_x=1):
                    falling_piece['x'] += 1
                    moving_right = True
                    moving_left = False
                    last_move_side_time = time.time()
                elif event.key == K_UP or event.key == K_w:
                    # rotate
                    falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])
                elif event.key == K_q:
                    # rotate opposite direction
                    falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])

                # making the piece fall faster with the down key
                elif event.key == K_DOWN or event.key == K_s:
                    moving_down = True
                    if is_valid_position(board, falling_piece, adj_y=1):
                        falling_piece['y'] += 1
                    last_move_down_time = time.time()

        # handle moving the piece because of user input
        if (moving_left or moving_right) and time.time() - last_move_side_time > MOVESIDEWAYSFREQ:
            if moving_left and is_valid_position(board, falling_piece, adj_x=-1):
                falling_piece['x'] -= 1
            elif moving_right and is_valid_position(board, falling_piece, adj_x=1):
                falling_piece['x'] += 1
            last_move_side_time = time.time()

        if moving_down and time.time() - last_move_down_time > MOVEDOWNFREQ and is_valid_position(board, falling_piece, adj_y=1):
            falling_piece['y'] += 1
            last_move_down_time = time.time()

        # let the piece fall if it is time to fall
        if time.time() - last_fall_time > fall_freq:
            # see if the piece has landed
            if not is_valid_position(board, falling_piece, adj_y=1):
                # falling piece has landed, set it on the board
                add_to_board(board, falling_piece)
                score += remove_complete_lines(board)
                level, fall_freq = level_and_fall_frequency(score)
                falling_piece = None
            else:
                # piece did not land, just move the piece down
                falling_piece['y'] += 1
                last_fall_time = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(board)
        draw_status(score, level)
        draw_next_piece(next_piece)
        if falling_piece is not None:
            draw_piece(falling_piece)

        pygame.display.update()


def make_text(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    """Terminate the game and exit."""
    pygame.quit()
    # TODO: sys.exit not necessary in gym env
    sys.exit()


def level_and_fall_frequency(score: float) -> tuple:
    """
    Return the level the player is on based on score and the fall speed.

    Args:
        score: the score to calculate level and fall freq from

    Returns:
        a tuple of:
        - the level the player is on
        - the fall_frequency for piece (drop speed)

    """
    # get the level that the player is on
    level = int(score / 10) + 1
    # get the frequency with which to move pieces down
    fall_freq = 0.27 - (level * 0.02)

    return level, fall_freq


def new_piece() -> dict:
    """Return a random new piece in a random rotation."""
    shape = random.choice(list(PIECES.keys()))
    # start the new piece above the board (i.e. y < 0)
    return {
        'shape': shape,
        'rotation': random.randint(0, len(PIECES[shape]) - 1),
        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
        'y': -2,
        'color': PALETTE[shape]
    }


def add_to_board(board: list, piece: dict) -> None:
    """
    Fill in the board based on piece's location, shape, and rotation.

    Args:
        board: the board to add the piece to
        piece: the piece to add to the board

    Returns:
        None

    """
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def get_blank_board() -> list:
    """Return a new blank board data structure."""
    board = []
    for _ in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)

    return board


def is_on_board(x: int, y: int) -> bool:
    """
    Return a boolean determining if the box is on the board.

    Args:
        x: the x coordinate of the box
        y: the y coordinate of the box

    Returns:
        True if the coordinates are in range, False otherwise

    """
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def is_valid_position(
    board: list,
    piece: dict,
    adj_x: int=0,
    adj_y: int=0
) -> bool:
    """
    Return True if the piece is within the board and not colliding.

    Args:
        board: the board to look for collisions in
        piece: the piece to check the validity of
        adj_x: TODO
        adj_y: TODO

    Returns:
        True if the piece is within the board and not colliding

    """
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            is_above_board = y + piece['y'] + adj_y < 0
            is_blank = PIECES[piece['shape']][piece['rotation']][y][x] == BLANK
            if is_above_board or is_blank:
                continue
            if not is_on_board(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
                return False
            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
                return False

    return True


def is_complete_line(board: list, y: int) -> bool:
    """
    Return True if the line filled with boxes with no gaps.

    Args:
        board: the board of pieces to look in
        y: the line to check for completion

    Returns:
        True if the line is complete, False otherwise
    """
    for x in range(BOARDWIDTH):
        # if there is a blank box then the line is not complete
        if board[x][y] == BLANK:
            return False

    return True


def remove_complete_lines(board: list) -> int:
    """Remove completed lines on the board.

    Args:
        board: the board of pieces to remove completed lines from

    Returns:
        The number of completed lines removed from the board

    Note:
        - lines are moved down after complete ones are removed

    """
    num_lines_removed = 0
    # start y at the bottom of the board
    y = BOARDHEIGHT - 1
    while y >= 0:
        if is_complete_line(board, y):
            # Remove the line and pull boxes down by one line.
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y - 1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            num_lines_removed += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            # move on to check next row up
            y -= 1

    return num_lines_removed


def to_pixel_coordinate(box_x: int, box_y: int) -> tuple:
    """
    Convert x, y coordinates of the board to pixel coordinates.

    Args:
        box_x: the x coordinate of the box on the board
        box_y: the y coordinate of the box on the board

    Returns:
        a tuple of:
        - the x coordinate as a pixel
        - the y coordinate as a pixel

    """
    return (XMARGIN + (box_x * BOXSIZE)), (TOPMARGIN + (box_y * BOXSIZE))


def draw_box(
    box_x: int,
    box_y: int,
    color: int,
    pixel_x: int = None,
    pixel_y: int = None,
) -> None:
    """
    Draw a single box of a piece at given coordinates.

    Args:
        box_x: the x coordinate in the Tetris grid
        box_y: the y coordinate in the Tetris grid
        color: the color of the box (as an index)
        pixel_x: optional x pixel coordinate to override the box coordinate
        pixel_y: optional y pixel coordinate to override the box coordinate

    Returns:
        None

    """
    # don't draw empty boxes
    if color == BLANK:
        return
    # convert the box coordinates to pixel coordinates if none are specified
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = to_pixel_coordinate(box_x, box_y)
    # draw the main background box
    main_rect = (pixel_x + 1, pixel_y + 1, BOXSIZE - 1, BOXSIZE - 1)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], main_rect)
    # draw the smaller depth perspective effect box
    depth_rect = (pixel_x + 1, pixel_y + 1, BOXSIZE - 4, BOXSIZE - 4)
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], depth_rect)


def draw_board(board: list) -> None:
    """
    Draw the board.

    Args:
        board: the board of boxes to draw

    Returns:
        None

    """
    # draw the border
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, BORDER_DIMS, 3)
    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, BG_DIMS)
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            draw_box(x, y, board[x][y])


def draw_piece(piece: dict, pixel_x: int = None, pixel_y: int = None) -> None:
    """
    draw a piece on the board.

    Args:
        piece: the piece to draw as a dictionary
        pixel_x: the optional x pixel to draw the piece at
        pixel_y: the optional y pixel to draw the piece at

    Returns:
        None

    """
    # get the template of the piece based on shape and rotation
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    # if pixel_x & pixel_y are None, use the pieces internal location
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = to_pixel_coordinate(piece['x'], piece['y'])
    # draw each of the boxes that make up the piece
    for box_x in range(TEMPLATEWIDTH):
        for box_y in range(TEMPLATEHEIGHT):
            if shapeToDraw[box_y][box_x] != BLANK:
                x = pixel_x + (box_x * BOXSIZE)
                y = pixel_y + (box_y * BOXSIZE)
                draw_box(None, None, piece['color'], x, y)


def draw_status(score: int, level: int) -> None:
    """
    Draw the status information for the player

    Args:
        score: the score of the game
        level: the current level the player is on

    Returns:
        None

    """
    # draw the score label
    score_label_surf = BASICFONT.render(SCORE_LABEL, True, TEXTCOLOR)
    score_label_rect = score_label_surf.get_rect()
    score_label_rect.topleft = (STATUS_X, SCORE_LABEL_Y)
    DISPLAYSURF.blit(score_label_surf, score_label_rect)
    # draw the score
    score_surf = BASICFONT.render(str(score), True, TEXTCOLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (STATUS_X, SCORE_Y)
    DISPLAYSURF.blit(score_surf, score_rect)
    # draw the level label
    level_label_surf = BASICFONT.render(LEVEL_LABEL, True, TEXTCOLOR)
    level_label_rect = level_label_surf.get_rect()
    level_label_rect.topleft = (STATUS_X, LEVEL_LABEL_Y)
    DISPLAYSURF.blit(level_label_surf, level_label_rect)
    # draw the level
    level_surf = BASICFONT.render(str(level), True, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (STATUS_X, LEVEL_Y)
    DISPLAYSURF.blit(level_surf, level_rect)


def draw_next_piece(piece: dict) -> None:
    """
    Draw the next piece that is coming to the player.

    Args:
        piece: the piece to draw as a dictionary

    Returns:
        None

    """
    # draw the "next" label
    next_surf = BASICFONT.render(NEXT_LABEL, True, TEXTCOLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (STATUS_X, NEXT_LABEL_Y)
    DISPLAYSURF.blit(next_surf, next_rect)
    # draw the "next" piece preview
    draw_piece(piece, pixel_x=STATUS_X, pixel_y=NEXT_Y)


if __name__ == '__main__':
    main()
