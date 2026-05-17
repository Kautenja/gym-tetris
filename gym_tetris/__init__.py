"""Registration code of Gym environments in this package."""
from ._registration import make
from .tetris_env import TetrisEnv


# define the outward facing API of this package
__all__ = [
    make.__name__,
    TetrisEnv.__name__,
]
