"""Wrappers for altering the functionality of the game."""
import gym
from .clip_reward_env import ClipRewardEnv
from .downsample_env import DownsampleEnv
from .frame_stack_env import FrameStackEnv
from .frameskip_env import FrameskipEnv
from .penalize_death_env import PenalizeDeathEnv
from .penalize_height_env import PenalizeHeightEnv
from .reward_cache_env import RewardCacheEnv


def wrap(env: gym.Env,
    image_size: tuple=(84, 84),
    skip_frames: int=3,
    death_penalty: int=-10,
    penalize_height: bool=True,
    clip_rewards: bool=False,
    agent_history_length: int=4,
) -> gym.Env:
    """
    Wrap an environment with standard wrappers.

    Args:
        game_name: the name of the game to make
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
        env = FrameskipEnv(env, skip=skip_frames)
    # apply a down-sampler for the given game
    env = DownsampleEnv(env, image_size)
    # apply the death penalty feature if enabled
    if death_penalty is not None:
        env = PenalizeDeathEnv(env, penalty=death_penalty)
    # apply the penalty for height increases if enabled
    if penalize_height:
        env = PenalizeHeightEnv(env)
    # clip the rewards in {-1, 0, +1} if the feature is on
    if clip_rewards:
        env = ClipRewardEnv(env)
    # apply the back history of frames if the feature is on
    if agent_history_length is not None:
        env = FrameStackEnv(env, agent_history_length)

    return env


# explicitly define the outward facing API of this package
__all__ = [
    ClipRewardEnv.__name__,
    DownsampleEnv.__name__,
    FrameStackEnv.__name__,
    FrameskipEnv.__name__,
    PenalizeDeathEnv.__name__,
    PenalizeHeightEnv.__name__,
    RewardCacheEnv.__name__,
    wrap.__name__,
]
