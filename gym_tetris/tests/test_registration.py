"""Test cases for the gym registered environments."""
from unittest import TestCase
from .. import make


class ShouldMakeEnv:
    """A test case for making an arbitrary environment."""
    # the number of coins at the start
    coins = 0
    # whether flag get is thrown
    flag_get = False
    # the number of lives left
    life = 2
    # the current world
    world = 1
    # the current score
    score = 0
    # the current stage
    stage = 1
    # the amount of time left
    time = 400
    # the x position of Mario
    x_pos = 40
    # the environments ID
    env_id = None
    # the random seed to apply
    seed = None

    def _test_env(self, env_id):
        env = make(env_id)
        if self.seed is not None:
            env.seed(self.seed)
        env.reset()
        s, r, d, i = env.step(0)
        # self.assertEqual(self.coins, i['coins'])
        # self.assertEqual(self.flag_get, i['flag_get'])
        # self.assertEqual(self.life, i['life'])
        # self.assertEqual(self.world, i['world'])
        # self.assertEqual(self.score, i['score'])
        # self.assertEqual(self.stage, i['stage'])
        # self.assertEqual(self.time, i['time'])
        # self.assertEqual(self.x_pos, i['x_pos'])
        env.close()

    def test(self):
        if isinstance(self.env_id, str):
            self._test_env(self.env_id)
        elif isinstance(self.env_id, list):
            for env_id in self.env_id:
                self._test_env(env_id)


class ShouldMakeTetris(ShouldMakeEnv, TestCase):
    # the environments ID for all versions of Super Mario Bros
    env_id = 'Tetris-v0'
