"""A script for registering environments with gym."""
import gym


gym.envs.registration.register(
    id='Tetris-v0',
    entry_point='gym_tetris:TetrisEnv',
    kwargs={
        'reward_score': True,
        'reward_lines': False,
        'penalize_height': False,
    },
    nondeterministic=True,
)


gym.envs.registration.register(
    id='Tetris-v1',
    entry_point='gym_tetris:TetrisEnv',
    kwargs={
        'reward_score': False,
        'reward_lines': True,
        'penalize_height': False,
    },
    nondeterministic=True,
)


gym.envs.registration.register(
    id='Tetris-v2',
    entry_point='gym_tetris:TetrisEnv',
    kwargs={
        'reward_score': True,
        'reward_lines': False,
        'penalize_height': True,
    },
    nondeterministic=True,
)


gym.envs.registration.register(
    id='Tetris-v4',
    entry_point='gym_tetris:TetrisEnv',
    kwargs={
        'reward_score': False,
        'reward_lines': True,
        'penalize_height': True,
    },
    nondeterministic=True,
)


# create an alias to gym.make for ease of access
make = gym.make


# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]
