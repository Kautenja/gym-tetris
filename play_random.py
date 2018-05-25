"""A simple script for debugging the Super Mario Bros. Lua code."""
from tqdm import tqdm
import gym
import gym_tetris


env = gym_tetris.make('Tetris-v0')
env = gym_tetris.wrap(env)
# env = gym.wrappers.Monitor(env, './monitor', force=True)


try:
    done = True
    progress = tqdm(range(5000))
    for step in progress:
        if done:
            state = env.reset()
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        env.render('human')
        progress.set_postfix(reward=reward)
except KeyboardInterrupt:
    pass


env.reset()
env.close()
