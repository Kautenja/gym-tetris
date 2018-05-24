"""An environment for playing Tetris."""
import numpy as np
import gym
from gym.envs.classic_control.rendering import SimpleImageViewer


# The width of images rendered by the NES
SCREEN_WIDTH = 256
# The height of images rendered by the NES
SCREEN_HEIGHT = 224


class TetrisEnv(gym.Env, gym.utils.EzPickle):
    """An environment for playing NES games in OpenAI Gym using FCEUX."""

    # meta-data about the environment for OpenAI Gym utilities (like Monitor)
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 60,
    }

    def __init__(self, max_episode_steps: int, random_seed: int=0) -> None:
        """
        Initialize a new Tetris environment.

        Args:
            max_episode_steps: the math number of steps per episode.
                - pass math.inf to use no max_episode_steps limit
            frame_skip: the number of frames to skip between between inputs
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
