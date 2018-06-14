"""An environment to skip k frames and return a max between the last two."""
import gym
import numpy as np


class FrameskipEnv(gym.Wrapper):
    """An environment to skip k frames."""

    def __init__(self, env: gym.Env, skip: int=4) -> None:
        """
        Initialize a new max frame skip env around an existing environment.

        Args:
            env: the environment to wrap around
            skip: the number of frames to skip (i.e. hold an action for)

        Returns:
            None

        """
        super().__init__(env)
        self._skip = skip

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
        # the total reward from `skip` frames having `action` held on them
        total_reward = 0.0
        done = False
        # perform the action `skip` times
        for _ in range(self._skip):
            state, reward, done, info = self.env.step(action)
            total_reward += reward
            # break the loop if the game terminated
            if done:
                break

        return state, total_reward, done, info

    def reset(self) -> np.ndarray:
        """Reset the emulator and return the initial state."""
        return self.env.reset()


# explicitly define the outward facing API of this module
__all__ = [FrameskipEnv.__name__]
