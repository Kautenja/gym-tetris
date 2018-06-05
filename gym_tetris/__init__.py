"""Registration code of Gym environments in this package."""
import math
import gym
from .tetris_env import TetrisEnv
from .wrappers import (
    ClipRewardEnv,
    DownsampleEnv,
    FrameStackEnv,
    MaxFrameskipEnv,
    PenalizeDeathEnv,
    RewardCacheEnv,
)


gym.envs.registration.register(
    id='Tetris-v0',
    entry_point='gym_tetris:TetrisEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={'max_steps': math.inf},
    nondeterministic=True,
)


def make(environment: str) -> gym.Env:
    """Make the environment and return it. same as `gym.make`."""
    return gym.make(environment)


def wrap(env: gym.Env,
    image_size: tuple=(84, 84),
    skip_frames: int=4,
    death_penalty: int=-1,
    clip_rewards: bool=True,
    agent_history_length: int=4
) -> gym.Env:
    """
    Wrap an environment with standard wrappers.

    Args:
        env: the environment to wrap
        image_size: the size to down-sample images to
        skip_frames: the number of frames to hold each action for
        death_penatly: the penalty for losing a life in a game
        clip_rewards: whether to clip rewards in {-1, 0, +1}
        agent_history_length: the size of the frame buffer for the agent

    Returns:
        a gym environment configured for this experiment

    """
    # wrap the environment with a reward cacher
    env = RewardCacheEnv(env)
    # apply the frame skip feature if enabled
    if skip_frames is not None:
        env = MaxFrameskipEnv(env, skip=skip_frames)
    # apply a down-sampler for the given game
    env = DownsampleEnv(env, image_size)
    # apply the death penalty feature if enabled
    if death_penalty is not None:
        env = PenalizeDeathEnv(env, penalty=death_penalty)
    # clip the rewards in {-1, 0, +1} if the feature is enabled
    if clip_rewards:
        env = ClipRewardEnv(env)
    # apply the back history of frames if the feature is enabled
    if agent_history_length is not None:
        env = FrameStackEnv(env, agent_history_length)

    return env


# define the outward facing API of this module (none, gym provides the API)
__all__ = [
    TetrisEnv.__name__,
    make.__name__,
    wrap.__name__,
]
