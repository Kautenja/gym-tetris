"""A script for registering environments with gym."""
import gym


gym.envs.registration.register(
    id='Tetris-v0',
    entry_point='gym_tetris:TetrisEnv',
    kwargs={'reward': 'score'},
    nondeterministic=True,
)


gym.envs.registration.register(
    id='Tetris-v1',
    entry_point='gym_tetris:TetrisEnv',
    kwargs={'reward': 'lines'},
    nondeterministic=True,
)


# create an alias to gym.make for ease of access
make = gym.make


# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]
