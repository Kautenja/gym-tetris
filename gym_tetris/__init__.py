"""Registration code of Gym environments in this package."""
import gym as _gym
from gym import make
from .tetris_env import TetrisEnv


# register the environment
_gym.envs.registration.register(
    id='Tetris-v0',
    entry_point='gym_tetris:TetrisEnv',
    nondeterministic=True,
)


# define the outward facing API of this package
__all__ = [
    make.__name__,
    TetrisEnv.__name__,
]
