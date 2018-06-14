"""A gym wrapper for penalizing height increases."""
import gym
import numpy as np


class PenalizeHeightEnv(gym.Wrapper):
    """a wrapper that penalizes height increases."""

    def __init__(self, env: gym.Env) -> None:
        """
        Initialize a new height-increase penalizing environment wrapper.

        Args:
            env: the environment to wrap

        Returns:
            None

        """
        super().__init__(env)
        self.height = 0

    def step(self, action: int) -> tuple:
        """
        Take a step using the given action.

        Args:
            action: the discrete action to perform.

        Returns:
            a tuple of:
            -   the start as a result of the action
            -   the reward achieved by taking the action
            -   a flag denoting whether the episode has ended
            -   a dictionary of extra information

        """
        obs, reward, done, info = self.env.step(action)
        # augment the reward based on the change in height
        reward -= info['height'] - self.height
        # update the local reference to the height of the board
        self.height = info['height']

        return obs, reward, done, info

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        # reset the height to 0
        self.height = 0

        return self.env.reset()


# explicitly specify the external API of this module
__all__ = [PenalizeHeightEnv.__name__]
