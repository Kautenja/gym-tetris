"""An OpenAI Gym environment for Tetris."""
import os
import random
from nes_py import NESEnv


# the directory that houses this module
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


# the path to the Zelda 1 ROM
_ROM_PATH = os.path.join(_MODULE_DIR, '_roms', 'Tetris.nes')


# the table for looking up piece orientations
_PIECE_ORIENTATION_TABLE = [
    'Tu',
    'Tr',
    'Td',
    'Tl',
    'Jl',
    'Ju',
    'Jr',
    'Jd',
    'Zh',
    'Zv',
    'O',
    'Sh',
    'Sv',
    'Lr',
    'Ld',
    'Ll',
    'Lu',
    'Iv',
    'Ih',
]


class TetrisEnv(NESEnv):
    """An environment for playing Tetris with OpenAI Gym."""

    # the legal range of rewards for each step
    reward_range = (-float('inf'), float('inf'))

    def __init__(self,
        b_type: bool=False,
        reward_score: bool=False,
        reward_lines: bool=True,
        penalize_height: bool=True,
    ) -> None:
        """
        Initialize a new Tetris environment.

        Args:
            reward_score:
            reward_lines:
            penalize_height:

        Returns:
            None

        """
        super().__init__(_ROM_PATH)
        self._b_type = b_type
        self._reward_score = reward_score
        self._current_score = 0
        self._reward_lines = reward_lines
        self._current_lines = 0
        self._penalize_height = penalize_height
        self._current_height = 0
        # reset the emulator, skip the start screen, and backup the state
        self.reset()
        self._skip_start_screen()
        self._backup()

    def seed(self, seed):
        """Seed the random number generator."""
        random.seed(seed)
        return [seed]

    def _read_bcd(self, address, length, little_endian=True):
        """
        Read a range of bytes where each nibble is a 10's place figure.

        Args:
            address: the address to read from as a 16 bit integer
            length: the number of sequential bytes to read
            little_endian: whether the bytes are in little endian order

        Returns:
            the integer value of the BCD representation

        """
        if little_endian:
            iterator = range(address, address + length)
        else:
            iterator = reversed(range(address, address + length))
        # iterate over the addresses to accumulate the value
        value = 0
        for idx, address in enumerate(iterator):
            value += 10**(2 * idx + 1) * (self.ram[address] >> 4)
            value += 10**(2 * idx) * (0x0F & self.ram[address])

        return value

    # MARK: Memory access

    @property
    def _current_piece(self):
        """Return the current piece."""
        try:
            return _PIECE_ORIENTATION_TABLE[self.ram[0x0042]]
        except IndexError:
            return None

    @property
    def _number_of_lines(self):
        """Return the number of cleared lines."""
        return self._read_bcd(0x0050, 2)

    @property
    def _lines_being_cleared(self):
        """Return the number of cleared lines."""
        return self.ram[0x0056]

    @property
    def _score(self):
        """Return the current score."""
        return self._read_bcd(0x0053, 3)

    @property
    def _is_game_over(self):
        """Return True if the game is over, False otherwise."""
        return bool(self.ram[0x0058])

    @property
    def _did_win_game(self):
        """Return True if game winning frame for B-type game mode."""
        if self._b_type:
            return self._number_of_lines == 0
        else: # can never win the A-type game
            return False

    @property
    def _next_piece(self):
        """Return the current piece."""
        try:
            return _PIECE_ORIENTATION_TABLE[self.ram[0x00BF]]
        except IndexError:
            return None

    @property
    def _statistics(self):
        """Return the statistics for the Tetrominoes."""
        return {
            'T': self._read_bcd(0x03F0, 2),
            'J': self._read_bcd(0x03F2, 2),
            'Z': self._read_bcd(0x03F4, 2),
            'O': self._read_bcd(0x03F6, 2),
            'S': self._read_bcd(0x03F8, 2),
            'L': self._read_bcd(0x03FA, 2),
            'I': self._read_bcd(0x03FC, 2),
        }

    @property
    def _board(self):
        """Return the Tetris board from NES RAM."""
        return self.ram[0x0400:0x04C8].reshape((20, 10)).copy()

    @property
    def _board_height(self):
        """Return the height of the board."""
        board = self._board
        # set the sentinel value for "empty" to 0
        board[board == 239] = 0
        # look for any piece in any row
        board = board.any(axis=1)
        # take to sum to determine the height of the board
        return board.sum()

    # MARK: RAM Hacks

    def _skip_start_screen(self):
        """Press and release start to skip the start screen."""
        # generate a random number for the Tetris RNG
        seed = random.randint(0, 255), random.randint(0, 255)
        # skip garbage screens
        while self.ram[0x00C0] in {0, 1, 2, 3}:
            # seed the random number generator
            self.ram[0x0017:0x0019] = seed
            self._frame_advance(8)
            if self._b_type:
                self._frame_advance(128)
            self._frame_advance(0)

    # MARK: nes-py API calls

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        # skip frames and seed the random number generator
        seed = random.randint(0, 255), random.randint(0, 255)
        for _ in range(14):
            self.ram[0x0017:0x0019] = seed
            self._frame_advance(0)
        # reset local variables
        self._current_score = 0
        self._current_lines = 0
        self._current_height = 0

    def _get_reward(self):
        """Return the reward after a step occurs."""
        reward = 0
        # reward the change in score
        if self._reward_score:
            reward += self._score - self._current_score
        # reward a line being cleared
        if self._reward_lines:
            reward += self._number_of_lines - self._current_lines
        # penalize a change in height
        if self._penalize_height:
            penalty = self._board_height - self._current_height
            # only apply the penalty for an increase in height (not a decrease)
            if penalty > 0:
                reward -= penalty
        # update the locals
        self._current_score = self._score
        self._current_lines = self._number_of_lines
        self._current_height = self._board_height

        return reward

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        return self._is_game_over or self._did_win_game

    def _get_info(self):
        """Return the info after a step occurs."""
        return dict(
            current_piece=self._current_piece,
            number_of_lines=self._number_of_lines,
            score=self._score,
            next_piece=self._next_piece,
            statistics=self._statistics,
            board_height=self._board_height,
        )


# explicitly define the outward facing API of this module
__all__ = [TetrisEnv.__name__]
