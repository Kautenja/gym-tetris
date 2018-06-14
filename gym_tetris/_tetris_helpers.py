"""Helper methods for a Tetris game state"""
import random
from ._constants.template import PIECES, TEMPLATEHEIGHT, TEMPLATEWIDTH, BLANK
from ._constants.palette import PALETTE
from ._constants.dimensions import (
    BOARDWIDTH,
    BOARDHEIGHT,
    BOXSIZE,
    XMARGIN,
    TOPMARGIN,
)


def level_and_fall_freq(
    complete_lines: float,
    base_speed: float=8.0,
    speed_limit: float=0.1,
) -> tuple:
    """
    Return the level the player is on based on number of complete lines.

    Args:
        complete_lines: the number of lines cleared in the game
        base_speed: the initial frequency at level 1 to scale down from

    Returns:
        a tuple of:
        - the level the player is on
        - the fall_frequency for piece (drop speed)

    """
    # get the level that the player is on
    level = int(complete_lines / 10) + 1
    # get the frequency with which to move pieces down
    fall_freq = base_speed / level
    # reset the fall_frequency if it's below the speed limit
    if fall_freq < speed_limit:
        fall_freq = speed_limit

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
                board[y + piece['y']][x + piece['x']] = piece['color']


def new_board() -> list:
    """Return a new blank board data structure."""
    board = []
    for _ in range(BOARDHEIGHT):
        board.append([BLANK] * BOARDWIDTH)

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
        adj_x: the direction in the x blocks to check
        adj_y: the direction in the y blocks to check

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
            if board[y + piece['y'] + adj_y][x + piece['x'] + adj_x] != BLANK:
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
        if board[y][x] == BLANK:
            return False

    return True


def remove_complete_lines(board: list) -> int:
    """Remove completed lines on the board.

    Args:
        board: the board of pieces to remove completed lines from

    Returns:
        The number of completed lines removed from the board

    Note:
        - lines move down after removing completed ones

    """
    num_lines_removed = 0
    # start y at the top of the board
    y = BOARDHEIGHT - 1
    while y >= 0:
        if is_complete_line(board, y):
            # Remove the line and pull boxes down by one line.
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[pull_down_y][x] = board[pull_down_y - 1][x]
            # Set top line to blank.
            for x in range(BOARDWIDTH):
                board[0][x] = BLANK
            num_lines_removed += 1
            # y is the same on the next iteration of the loop in case the line
            # following the removed line is also complete and needs removed
        else:
            # move on to check next row up
            y -= 1

    return num_lines_removed


def get_height(board: list) -> int:
    """
    Return the height of the board.

    Args:
        board: the board to return the height of

    Returns:
        the y coordinate of the first row (from top) with a non-blank box in it

    """
    # iterate over the board starting at the end of the matrix (the bottom)
    for y in reversed(range(0, BOARDHEIGHT)):
        # if reached a row with entirely blanks, return the row index
        if set(board[y]) == {BLANK}:
            return BOARDHEIGHT - y - 1

    return BOARDHEIGHT


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


# explicitly define the outward facing API of this module
__all__ = [
    level_and_fall_freq.__name__,
    new_piece.__name__,
    add_to_board.__name__,
    new_board.__name__,
    is_on_board.__name__,
    is_valid_position.__name__,
    is_complete_line.__name__,
    remove_complete_lines.__name__,
    get_height.__name__,
    to_pixel_coordinate.__name__,
]
