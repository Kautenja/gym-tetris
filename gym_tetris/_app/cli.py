"""Tetris for OpenAI Gym."""
import argparse
import gym
from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
from nes_py.app.play_human import play_human
from nes_py.app.play_random import play_random


def _get_args():
    """Parse command line arguments and return them."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--environment', '-e',
        type=str,
        default='Tetris-v0',
        choices=['Tetris-v0', 'Tetris-v1'],
        help='The environment to play.'
    )
    parser.add_argument('--mode', '-m',
        type=str,
        default='human',
        choices=['human', 'random'],
        help='The execution mode for the environment.'
    )
    parser.add_argument('--steps', '-s',
        type=int,
        default=500,
        help='The number of random steps to take.',
    )

    return parser.parse_args()


def main():
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args()
    # build the environment with the given ID
    env = gym.make('Tetris-v0')
    # play the environment with the given mode
    if args.mode == 'human':
        play_human(env)
    else:
        play_random(env, args.steps)


# explicitly define the outward facing API of this module
__all__ = [main.__name__]
