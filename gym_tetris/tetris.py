"""Methods for spawning and interacting with a Tetris game."""
import os
import pygame
import numpy as np
# TODO: move all these global constants to a class in their module to reduce
# all this obnoxious import stuff.
from ._constants.template import PIECES, TEMPLATEHEIGHT, TEMPLATEWIDTH, BLANK
from ._constants.palette import (
    COLORS,
    LIGHTCOLORS,
    BORDERCOLOR,
    BGCOLOR,
    TEXTCOLOR,
)
from ._constants.strings import (
    GAME_NAME_LABEL, SCORE_LABEL, LEVEL_LABEL, NEXT_LABEL
)
from ._constants.dimensions import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BOXSIZE,
    BORDER_DIMS,
    BG_DIMS,
    BOARDWIDTH,
    BOARDHEIGHT,
    STATUS_X,
    SCORE_LABEL_Y,
    SCORE_Y,
    LEVEL_LABEL_Y,
    LEVEL_Y,
    NEXT_LABEL_Y,
    NEXT_Y,
)
from ._tetris_helpers import (
    level_and_fall_freq,
    new_piece,
    add_to_board,
    new_board,
    is_valid_position,
    remove_complete_lines,
    get_height,
    to_pixel_coordinate,
)


# the frequency to accept moves of a certain kind
MOVE_FREQ = 3
# the direction indicating a side move to the left
MOVE_RIGHT = 1
# the direction indicating a side move to the right
MOVE_LEFT = -1


class Tetris(object):
    """An object oriented design of Tetris."""

    def __init__(self) -> None:
        """Initialize a new Tetris game."""
        # setup the environment to disable the pygame window
        if os.environ.get('HUMAN_PLAY', None) is None:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        # initialize pygame
        pygame.init()
        pygame.display.set_caption(GAME_NAME_LABEL)
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._font = pygame.font.Font('freesansbold.ttf', 18)
        # a list of callable actions for the game
        self.actions = [
            # NOP
            lambda: None,
            # left
            lambda: self._move_sideways(MOVE_LEFT),
            # right
            lambda: self._move_sideways(MOVE_RIGHT),
            # down
            self._move_down,
            # rotate left
            lambda: self._rotate(MOVE_LEFT),
            # rotate right
            lambda: self._rotate(MOVE_RIGHT),
            # left + down
            lambda: (self._move_sideways(MOVE_LEFT), self._move_down()),
            # right + down
            lambda: (self._move_sideways(MOVE_RIGHT), self._move_down()),
            # left + rotate left
            lambda: (self._move_sideways(MOVE_LEFT), self._rotate(MOVE_LEFT)),
            # right + rotate left
            lambda: (self._move_sideways(MOVE_RIGHT), self._rotate(MOVE_LEFT)),
            # left + rotate right
            lambda: (self._move_sideways(MOVE_LEFT), self._rotate(MOVE_RIGHT)),
            # right + rotate right
            lambda: (self._move_sideways(MOVE_RIGHT), self._rotate(MOVE_RIGHT)),
        ]

    def __del__(self) -> None:
        """Close the pygame environment before deleting this object."""
        pygame.quit()

    # MARK: private graphics methods

    def _draw_box(self,
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
        # convert the box coordinates to pixel coordinates if none are given
        if pixel_x is None and pixel_y is None:
            pixel_x, pixel_y = to_pixel_coordinate(box_x, box_y)
        # draw the main background box
        main_rect = (pixel_x + 1, pixel_y + 1, BOXSIZE - 1, BOXSIZE - 1)
        pygame.draw.rect(self._screen, COLORS[color], main_rect)
        # draw the smaller depth perspective effect box
        depth_rect = (pixel_x + 1, pixel_y + 1, BOXSIZE - 4, BOXSIZE - 4)
        pygame.draw.rect(self._screen, LIGHTCOLORS[color], depth_rect)

    def _draw_board(self, board: list) -> None:
        """
        Draw the board.

        Args:
            board: the board of boxes to draw

        Returns:
            None

        """
        # draw the border
        pygame.draw.rect(self._screen, BORDERCOLOR, BORDER_DIMS, 3)
        # fill the background of the board
        pygame.draw.rect(self._screen, BGCOLOR, BG_DIMS)
        # draw the individual boxes on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                self._draw_box(x, y, board[y][x])

    def _draw_status(self, score: int, level: int) -> None:
        """
        Draw the status information for the player

        Args:
            score: the score of the game
            level: the current level the player is on

        Returns:
            None

        """
        # draw the score label
        score_label_surf = self._font.render(SCORE_LABEL, True, TEXTCOLOR)
        score_label_rect = score_label_surf.get_rect()
        score_label_rect.topleft = (STATUS_X, SCORE_LABEL_Y)
        self._screen.blit(score_label_surf, score_label_rect)
        # draw the score
        score_surf = self._font.render(str(score), True, TEXTCOLOR)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (STATUS_X, SCORE_Y)
        self._screen.blit(score_surf, score_rect)
        # draw the level label
        level_label_surf = self._font.render(LEVEL_LABEL, True, TEXTCOLOR)
        level_label_rect = level_label_surf.get_rect()
        level_label_rect.topleft = (STATUS_X, LEVEL_LABEL_Y)
        self._screen.blit(level_label_surf, level_label_rect)
        # draw the level
        level_surf = self._font.render(str(level), True, TEXTCOLOR)
        level_rect = level_surf.get_rect()
        level_rect.topleft = (STATUS_X, LEVEL_Y)
        self._screen.blit(level_surf, level_rect)

    def _draw_piece(self,
        piece: dict,
        pixel_x: int = None,
        pixel_y: int = None,
    ) -> None:
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
        shape_to_draw = PIECES[piece['shape']][piece['rotation']]
        # if pixel_x & pixel_y are None, use the pieces internal location
        if pixel_x is None and pixel_y is None:
            pixel_x, pixel_y = to_pixel_coordinate(piece['x'], piece['y'])
        # draw each of the boxes that make up the piece
        for box_x in range(TEMPLATEWIDTH):
            for box_y in range(TEMPLATEHEIGHT):
                if shape_to_draw[box_y][box_x] != BLANK:
                    x = pixel_x + (box_x * BOXSIZE)
                    y = pixel_y + (box_y * BOXSIZE)
                    self._draw_box(None, None, piece['color'], x, y)

    def _draw_next_piece(self, piece: dict) -> None:
        """
        Draw the next piece that is coming to the player.

        Args:
            piece: the piece to draw as a dictionary

        Returns:
            None

        """
        # draw the "next" label
        next_surf = self._font.render(NEXT_LABEL, True, TEXTCOLOR)
        next_rect = next_surf.get_rect()
        next_rect.topleft = (STATUS_X, NEXT_LABEL_Y)
        self._screen.blit(next_surf, next_rect)
        # draw the "next" piece preview
        self._draw_piece(piece, pixel_x=STATUS_X, pixel_y=NEXT_Y)

    # MARK: private movement methods

    def _fall(self) -> None:
        """
        Make the piece fall naturally.

        Returns:
            the number of lines removed by this fall

        """
        # the score from the fall
        complete_lines = 0
        # see if the piece has landed
        if not is_valid_position(self.board, self.falling_piece, adj_y=1):
            # falling piece has landed, set it on the board
            add_to_board(self.board, self.falling_piece)
            complete_lines = remove_complete_lines(self.board)
            self.falling_piece = None
        else:
            # piece did not land, just move the piece down
            self.falling_piece['y'] += 1
            self.last_fall_time = self.frame

        # calculate the score of using the standard exponential scoring scheme
        score = 0 if complete_lines == 0 else 2 ** (complete_lines - 1)
        self.score += score
        # update the level based on the number of cleared lines
        self.complete_lines += complete_lines
        self.level, self.fall_freq = level_and_fall_freq(self.complete_lines)

        return score

    def _rotate(self, direction: int) -> None:
        """
        Rotate the falling piece based on the given direction.

        Args:
            direction: the direction to move the piece in

        Returns:
            None
        """
        if self.frame - self.last_rotate_time < MOVE_FREQ:
            return
        # backup the piece in case the rotation is illegal
        backup = self.falling_piece['rotation']
        rots = len(PIECES[self.falling_piece['shape']])
        rotation = (self.falling_piece['rotation'] + direction) % rots
        self.falling_piece['rotation'] = rotation
        # rotate back to the backup if the position is invalid
        if not is_valid_position(self.board, self.falling_piece):
            self.falling_piece['rotation'] = backup
        self.last_rotate_time = self.frame

    def _move_sideways(self, direction: int) -> None:
        """
        Move the falling piece left or right on the board.

        Args:
            direction: the direction to move the piece in

        Returns:
            None

        """
        if is_valid_position(self.board, self.falling_piece, adj_x=direction):
            if self.frame - self.last_move_side_time < MOVE_FREQ:
                return
            self.falling_piece['x'] += direction
            self.last_move_side_time = self.frame

    def _move_down(self) -> None:
        """Moving the falling piece down on the board."""
        if is_valid_position(self.board, self.falling_piece, adj_y=1):
            if self.frame - self.last_move_down_time < MOVE_FREQ:
                return
            self.falling_piece['y'] += 1
        self.last_move_down_time = self.frame

    # MARK: public facing API

    @property
    def screen(self) -> np.ndarray:
        """Return the screen as a NumPy array."""
        return pygame.surfarray.array3d(self._screen).swapaxes(0, 1)

    def reset(self) -> None:
        """Reset the board and game variables."""
        # set the board as a blank board
        self.board = new_board()
        # set the score to 0 and get the corresponding level and fall rate
        self.score = 0
        self.complete_lines = 0
        self.level, self.fall_freq = level_and_fall_freq(self.complete_lines)
        # setup the initial pieces
        self.falling_piece = new_piece()
        self.next_piece = new_piece()
        # setup the initial times for movement restriction
        self.frame = 0
        self.last_move_down_time = self.frame
        self.last_move_side_time = self.frame
        self.last_rotate_time = self.frame
        self.last_fall_time = self.frame
        self.is_game_over = False

    def step(self, action: int) -> None:
        """
        Perform a step with the given action.

        Args:
            action: the action to perform as an index of `self.actions`

        Returns:
            None

        """
        if self.is_game_over:
            raise ValueError('cant call step() when is_game_over is True')

        if self.falling_piece is None:
            # No falling piece in play, so start a new piece at the top
            self.falling_piece = self.next_piece
            self.next_piece = new_piece()
            # can't fit a new piece on the board, so game over
            if not is_valid_position(self.board, self.falling_piece):
                self.is_game_over = True
                info = {'score': self.score, 'height': BOARDHEIGHT}
                return self.screen, 0, True, info

        # unwrap the action and call it
        self.actions[action]()
        height = get_height(self.board)

        # fall if it's time to do so
        reward = 0
        if self.frame - self.last_fall_time > self.fall_freq:
            reward = self._fall()

        # draw everything on the screen
        self._screen.fill(BGCOLOR)
        self._draw_board(self.board)
        self._draw_status(self.score, self.level)
        self._draw_next_piece(self.next_piece)
        if self.falling_piece is not None:
            self._draw_piece(self.falling_piece)
        # update the pygame display
        pygame.display.update()
        self.frame += 1

        info = {'score': self.score, 'height': height}
        return self.screen, reward, False, info


# explicitly define the outward facing API of this module
__all__ = [Tetris.__name__]
