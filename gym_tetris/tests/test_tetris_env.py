"""Test cases for the Super Mario Bros meta environment."""
from unittest import TestCase
from ..tetris_env import TetrisEnv


class ShouldCreateEnvWithDefaultRewardLines(TestCase):
    def test(self):
        env = TetrisEnv()
        self.assertFalse(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertTrue(env._penalize_height)
        self.assertEqual(0, env._current_score)
        self.assertEqual(0, env._current_lines)
        self.assertEqual(0, env._current_height)


class ShouldCreateEnvWithRewardScore(TestCase):
    def test(self):
        env = TetrisEnv(reward_score=True)
        self.assertFalse(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldCreateEnvWithoutPenalizeHeight(TestCase):
    def test(self):
        env = TetrisEnv(penalize_height=False)
        self.assertFalse(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldCreateEnvWithoutRewardLines(TestCase):
    def test(self):
        env = TetrisEnv(reward_lines=False)
        self.assertFalse(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldCreateEnvWithBType(TestCase):
    def test(self):
        env = TetrisEnv(b_type=True)
        self.assertTrue(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldStep(TestCase):
    def test(self):
        env = TetrisEnv()
        env.seed(1)
        _ = env.reset()
        _, reward, _, info = env.step(0)
        # check all the information
        self.assertEqual(0, reward)
        self.assertEqual('Ld', info['current_piece'])
        self.assertEqual(0, info['number_of_lines'])
        self.assertEqual(0, info['score'])
        self.assertEqual('Sh', info['next_piece'])
        stats = {'T': 0, 'J': 0, 'Z': 0, 'O': 0, 'S': 0, 'L': 1, 'I': 0}
        self.assertEqual(stats, info['statistics'])

        env.close()


class ShouldCompleteEpisode(TestCase):

    def assertIsNotBlackScreen(self, screen):
        """
        Assert that the given screen (as a NumPy vector) is not empty.

        Args:
            screen: the screen to validate

        Returns:
            None

        """
        self.assertNotEqual(0, screen.sum())

    def test(self):
        env = TetrisEnv()
        s = env.reset()
        self.assertIsNotBlackScreen(s)
        done = False
        while not done:
            s, r, done, i = env.step(0)
            self.assertIsNotBlackScreen(s)
        s = env.reset()
        self.assertIsNotBlackScreen(s)
        env.close()
