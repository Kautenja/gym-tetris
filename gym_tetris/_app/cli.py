"""Tetris for Gymnasium."""
import argparse
import gymnasium as gym
from nes_py.wrappers import JoypadSpace
from nes_py.play import play_human
from nes_py.play import play_random
from ..actions import MOVEMENT, SIMPLE_MOVEMENT


# a key mapping of action spaces to wrap with
_ACTION_SPACES = {
    'simple': SIMPLE_MOVEMENT,
    'standard': MOVEMENT,
}


class FirstResetSeed(gym.Wrapper):
    """Inject a CLI seed into the first Gymnasium reset call."""

    def __init__(self, env, seed):
        """Initialize the wrapper with a one-shot seed."""
        super().__init__(env)
        self._first_reset_seed = seed

    def reset(self, *, seed=None, options=None):
        """Reset the environment, applying the CLI seed once."""
        if self._first_reset_seed is not None:
            if seed is None:
                seed = self._first_reset_seed
            self._first_reset_seed = None
        return self.env.reset(seed=seed, options=options)


def _get_args(argv=None):
    """Parse command line arguments and return them."""
    parser = argparse.ArgumentParser(description=__doc__)
    envs = []
    for mode in {'A', 'B'}:
        for version in range(4):
            envs.append('Tetris{}-v{}'.format(mode, version))
    parser.add_argument('--env', '-e',
        type=str,
        default='TetrisA-v0',
        choices=envs,
        help='The environment to play.'
    )
    parser.add_argument('--mode', '-m',
        type=str,
        default='human',
        choices=['human', 'random'],
        help='The execution mode for the environment.'
    )
    parser.add_argument('--actionspace', '-a',
        type=str,
        default='nes',
        choices=['nes', 'standard', 'simple'],
        help='the action space wrapper to use'
    )
    parser.add_argument('--seed', '-S',
        type=int,
        help='the random number seed to use'
    )
    parser.add_argument('--steps', '-s',
        type=int,
        default=500,
        help='The number of random steps to take.',
    )
    parser.add_argument('--render',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='render random-mode frames to a graphical window',
    )
    args = parser.parse_args(argv)
    if args.mode == 'human' and not args.render:
        parser.error('human mode requires graphical rendering')
    return args


def main(argv=None):
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args(argv)
    # build the environment with the given ID
    render_mode = 'human' if args.mode == 'random' and args.render else None
    env = gym.make(args.env, render_mode=render_mode)
    if args.seed is not None:
        env = FirstResetSeed(env, args.seed)
    # wrap the environment with an action space if specified
    if args.actionspace != 'nes':
        # unwrap the actions list by key
        actions = _ACTION_SPACES[args.actionspace]
        # wrap the environment with the new action space
        env = JoypadSpace(env, actions)
    # play the environment with the given mode
    if args.mode == 'human':
        play_human(env)
    else:
        play_random(env, args.steps, render=args.render)


if __name__ == '__main__':
    main()


# explicitly define the outward facing API of this module
__all__ = [main.__name__]
