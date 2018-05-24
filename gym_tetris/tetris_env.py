"""An environment for playing Tetris."""
import random, time, pygame
import numpy as np
import gym
from gym.envs.classic_control.rendering import SimpleImageViewer
from .template import PIECES, TEMPLATEHEIGHT, TEMPLATEWIDTH
from .palette import (
    BGCOLOR,
    BORDERCOLOR,
    TEXTCOLOR,
    TEXTSHADOWCOLOR,
    COLORS,
    LIGHTCOLORS,
    PALETTE
)


# The width of images rendered by the NES
SCREEN_WIDTH = 330
# The height of images rendered by the NES
SCREEN_HEIGHT = 430
# the number of pixels to use for a box
BOXSIZE = 20
# the number of horizontal boxes on the board (classic Tetris uses 10)
BOARDWIDTH = 10
# the number of vertical boxes on the board (classic Tetris uses 20)
BOARDHEIGHT = 20
# the number of pixels to pad the game from the right border of the screen
XMARGIN = 10
# the number of pixels to pad the game from the top border of the screen
TOPMARGIN = 20
# the dimensions of the border rectangle
BORDER_DIMS = (
    XMARGIN - 5,
    TOPMARGIN - 5,
    BOARDWIDTH * BOXSIZE + 10,
    BOARDHEIGHT * BOXSIZE + 10
)
# the dimensions of the background rectangle
BG_DIMS = (
    XMARGIN,
    TOPMARGIN,
    BOXSIZE * BOARDWIDTH,
    BOXSIZE * BOARDHEIGHT
)


# the x position for status items
STATUS_X = BORDER_DIMS[2] + 15
# the Y position for the "score" static label
SCORE_LABEL_Y = BORDER_DIMS[0] + 15
# the Y position for the score status
SCORE_Y = SCORE_LABEL_Y + 30
# the Y position for the "level" static label
LEVEL_LABEL_Y = SCORE_Y + 30
# the Y position for the level status
LEVEL_Y = LEVEL_LABEL_Y + 30
# the Y position for the "next" label
NEXT_LABEL_Y = LEVEL_Y + 30
# the Y position for the next piece preview
NEXT_Y = NEXT_LABEL_Y + 30


# the label for the "Next" piece to come
NEXT_LABEL = 'Next'
# the label for the current level status
LEVEL_LABEL = 'Level'
# the label for the current score status
SCORE_LABEL = 'Score'
# the label for the press key
PRESS_KEY_LABEL = 'Press a key to play.'
# the label to indicate that the game is over
GAME_OVER_LABEL = 'Over'
# the label to indicate that the game is paused
GAME_PAUSE_LABEL = 'Pause'
# the label for the title screen and window
GAME_NAME_LABEL = 'Tetris'


# the value denoting a blank pixel in a template
BLANK = '.'
# the frequency with which a piece can move sideways
MOVESIDEWAYSFREQ = 0.15
# the frequency with which a piece can move downwards
MOVEDOWNFREQ = 0.1


class TetrisEnv(gym.Env, gym.utils.EzPickle):
    """An environment for playing NES games in OpenAI Gym using FCEUX."""

    # meta-data about the environment for OpenAI Gym utilities (like Monitor)
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 144,
    }

    def __init__(self, max_episode_steps: int, random_seed: int=0) -> None:
        """
        Initialize a new Tetris environment.

        Args:
            max_episode_steps: the maximum number of steps per episode.
            random_seed: the random seed to start the environment with

        Returns:
            None

        """
        gym.utils.EzPickle.__init__(self)
        self.max_episode_steps = max_episode_steps
        self.curr_seed = random_seed
        self.viewer = None
        self.step_number = 0
        # Setup the observation space
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3),
            dtype=np.uint8
        )
        # set the screen to white noise from the observation space
        self.screen = self.observation_space.sample()
        # Setup the action space
        self.actions = ['U', 'D', 'L', 'R', 'UL', 'UR', 'DL', 'DR']
        self.action_space = gym.spaces.Discrete(len(self.actions))

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
            -   a dictionary of additional information

        """
        pass
        # # unwrap the string action value from the list of actions
        # self._joypad(self.actions[action])
        # # increment the frame counter
        # self.step_number += 1
        # # get the screen, reward, and done flag from the emulator
        # self.screen, reward, done = self._get_state()

        # return self.screen, reward, done, {}

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        pass
        # if not self.emulator_started:
        #     self._start_emulator()
        # # write the reset command to the emulator
        # self._write_to_pipe('reset' + SEP)
        # self.step_number = 0
        # # get a state from the emulator. ignore the `reward` and `done` flag
        # self.screen, _, _ = self._get_state()

        # return self.screen

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
        pass
        # if mode == 'human':
        #     if self.viewer is None:
        #         self.viewer = SimpleImageViewer()
        #     self.viewer.imshow(self.screen)
        # elif mode == 'rgb_array':
        #     return self.screen

    def close(self) -> None:
        """Close the emulator and shutdown FCEUX."""
        pass
        # self._write_to_pipe('close')
        # self.pipe_in.close()
        # self.pipe_out.close()
        # self.emulator_started = False

    def seed(self, seed: int=None) -> list:
        """
        Set the seed for this env's random number generator(s).

        Returns:
            A list of seeds used in this env's random number generators.
            there is only one "main" seed in this env
        """
        self.curr_seed = gym.utils.seeding.hash_seed(seed) % 256
        return [self.curr_seed]


# explicitly define the outward facing API of this module
__all__ = [TetrisEnv.__name__]
