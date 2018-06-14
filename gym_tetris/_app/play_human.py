"""A method to play gym environments using human IO inputs."""
import gym
import pygame
from .visualize.realtime_plot import RealtimePlot


def play(env: gym.Env, fps: int=30) -> None:
    """
    Play the game using the keyboard as a human.

    Args:
        env: gym.Env
            Environment to use for playing.
        fps: int
            Maximum number of steps of the environment to execute every second.
            Defaults to 30.

    Returns:
        None

    """
    # get the mapping of keyboard keys to actions in the environment
    if hasattr(env, 'get_keys_to_action'):
        keys_to_action = env.get_keys_to_action()
    elif hasattr(env.unwrapped, 'get_keys_to_action'):
        keys_to_action = env.unwrapped.get_keys_to_action()
    else:
        raise ValueError('env has no get_keys_to_action method')
    # create a set of the relevant keys used in the environment
    relevant_keys = set(sum(map(list, keys_to_action.keys()),[]))

    pressed_keys = []
    running = True
    done = True
    clock = pygame.time.Clock()
    plot = RealtimePlot()

    # start the main game loop
    while running:
        if done:
            done = False
            _ = env.reset()
        else:
            action = keys_to_action.get(tuple(sorted(pressed_keys)), 0)
            _, reward, done, _ = env.step(action)
            plot(reward)
        # process pygame events
        for event in pygame.event.get():
            # test events, set key states
            if event.type == pygame.KEYDOWN:
                if event.key in relevant_keys:
                    pressed_keys.append(event.key)
                elif event.key == 27:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in relevant_keys:
                    pressed_keys.remove(event.key)
            elif event.type == pygame.QUIT:
                running = False
        # limit the frame-rate
        clock.tick(fps)


# explicitly define the outward facing API of the module
__all__ = [play.__name__]
