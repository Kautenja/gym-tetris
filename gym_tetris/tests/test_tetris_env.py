"""Test cases for the Super Mario Bros meta environment."""
from unittest import TestCase
from ..tetris_env import TetrisEnv


class ShouldRaiseErrorOnInvalidReward(TestCase):
    def test(self):
        self.assertRaises(ValueError, TetrisEnv, reward=None)
        self.assertRaises(ValueError, TetrisEnv, reward='foo')


class ShouldCreateEnvWithScore(TestCase):
    def test(self):
        env = TetrisEnv()
        self.assertEqual('score', env._reward_stream)


class ShouldCreateEnvWithLine(TestCase):
    def test(self):
        env = TetrisEnv(reward='lines')
        self.assertEqual('lines', env._reward_stream)


class ShouldStep(TestCase):
    def test(self):
        env = TetrisEnv()
        env.seed(1)
        _ = env.reset()
        s, r, d, i = env.step(0)
        # check all the information
        self.assertEqual(0, r)
        self.assertEqual('O', i['current_piece'])
        self.assertEqual(0, i['number_of_lines'])
        self.assertEqual(0, i['score'])
        self.assertEqual('Td', i['next_piece'])
        stats = {'T': 0, 'J': 0, 'Z': 0, 'O': 1, 'S': 0, 'L': 0, 'I': 0}
        self.assertEqual(stats, i['statistics'])

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
