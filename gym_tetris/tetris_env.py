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

    def __init__(self):
        """Initialize a new Tetris environment."""
        super().__init__(_ROM_PATH)
        self._current_score = 0

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
        return _PIECE_ORIENTATION_TABLE[self.ram[0x0042]]

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
    def _next_piece(self):
        """Return the current piece."""
        return _PIECE_ORIENTATION_TABLE[self.ram[0x00BF]]

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
            self._frame_advance(0)

    # MARK: nes-py API calls

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        # mash the start button if this is a game over reset
        while self._is_game_over:
            self._frame_advance(8)
            self._frame_advance(0)
        self._skip_start_screen()
        self._current_score = 0

    def _get_reward(self):
        """Return the reward after a step occurs."""
        # calculate the reward as the change in the score
        reward = self._score - self._current_score
        self._current_score = self._score

        return reward

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        return self._is_game_over

    def _get_info(self):
        """Return the info after a step occurs."""
        return dict(
            current_piece=self._current_piece,
            number_of_lines=self._number_of_lines,
            score=self._score,
            next_piece=self._next_piece,
            statistics=self._statistics,
        )


# explicitly define the outward facing API of this module
__all__ = [TetrisEnv.__name__]
