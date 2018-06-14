"""An environment for playing Tetris."""
import random
import numpy as np
import gym
from ._constants.dimensions import SCREEN_HEIGHT, SCREEN_WIDTH
from .tetris import Tetris


class TetrisEnv(gym.Env, gym.utils.EzPickle):
    """An environment for playing Tetris in OpenAI Gym."""

    # meta-data about the environment for OpenAI Gym utilities (like Monitor)
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 30,
    }

    def __init__(self, max_steps: int, random_state: int=None) -> None:
        """
        Initialize a new Tetris environment.

        Args:
            max_steps: the max number of steps per episode.
            random_state: the random seed to start the environment with

        Returns:
            None

        """
        gym.utils.EzPickle.__init__(self)
        self.max_steps = max_steps
        self.viewer = None
        self.step_number = 0
        # Setup the observation space as RGB game frames
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3),
            dtype=np.uint8
        )
        # Setup the action space, the game defines 12 legal actions
        self.action_space = gym.spaces.Discrete(12)
        # setup the game
        self.game = Tetris()
        self.seed(random_state)

    @property
    def screen(self) -> np.ndarray:
        """Return the screen of the game"""
        return self.game.screen

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        self.game.reset()
        # reset the step count
        self.step_number = 0
        # return the initial screen from the game
        return self.game.screen

    def step(self, action: int) -> tuple:
        """
        Take a step using the given action.

        Args:
            action: the discrete action to perform. will use the action in
                    `self.actions` indexed by this value

        Returns:
            a tuple of:
            -   the start as a result of the action
            -   the reward achieved by taking the action
            -   a flag denoting whether the episode has ended
            -   a dictionary of extra information

        """
        state, reward, done, info = self.game.step(action)
        self.step_number += 1
        # if this step has passed the max number, set the episode to done
        if self.step_number >= self.max_steps:
            done = True
        return state, reward, done, info

    def render(self, mode: str='human'):
        """
        Render the current screen using the given mode.

        Args:
            mode: the mode to render the screen using
                - 'human': render in a window using GTK
                - 'rgb_array': render in the back-end and return a matrix

        Returns:
            None if mode is 'human' or a matrix if mode is 'rgb_array'

        """
        # if the mode is RGB, return the screen as a NumPy array
        if mode == 'rgb_array':
            return self.game.screen
        # if the mode is human, create a viewer and display the screen
        elif mode == 'human':
            from pyglet.window import Window
            from gym.envs.classic_control.rendering import SimpleImageViewer
            if self.viewer is None:
                self.viewer = SimpleImageViewer()
                self.viewer.window = Window(
                    width=SCREEN_WIDTH,
                    height=SCREEN_HEIGHT,
                    caption=self.spec.id,
                )
            self.viewer.imshow(self.game.screen)
            return self.viewer.isopen
        # otherwise the render mode is not supported, raise an error
        else:
            raise ValueError('unsupported render mode: {}'.format(repr(mode)))

    def close(self) -> None:
        """Close the emulator."""
        # delete the existing game if there is one
        if isinstance(self.game, Tetris):
            del self.game
        if self.viewer is not None:
            self.viewer.close()
            del self.viewer

    def seed(self, random_state: int=None) -> list:
        """
        Set the seed for this env's random number generator(s).

        Args:
            random_state: the seed to set the random generator to

        Returns:
            A list of seeds used in this env's random number generators

        """
        random.seed(random_state)
        self.curr_seed = random_state

        return [self.curr_seed]

    def get_keys_to_action(self) -> dict:
        """Return the dictionary of keyboard keys to actions."""
        # Map of in game directives to their associated keyboard value
        down = ord('s')
        left = ord('a')
        right = ord('d')
        rot_l = ord('q')
        rot_r = ord('e')
        # A mapping of pressed key combinations to discrete actions
        keys_to_action = {
            (): 0,
            (left, ): 1,
            (right, ): 2,
            (down, ): 3,
            (rot_l, ): 4,
            (rot_r, ): 5,
            tuple(sorted((left, down, ))): 6,
            tuple(sorted((right, down, ))): 7,
            tuple(sorted((left, rot_l, ))): 8,
            tuple(sorted((right, rot_l, ))): 9,
            tuple(sorted((left, rot_r, ))): 10,
            tuple(sorted((right, rot_r, ))): 11,
        }

        return keys_to_action


# explicitly define the outward facing API of this module
__all__ = [TetrisEnv.__name__]
