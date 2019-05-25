"""Test cases for the gym registered environments."""
from unittest import TestCase
from .. import make


class ShouldMakeTetrisScore(TestCase):
    def test(self):
        env = make('Tetris-v0')
        self.assertEqual('score', env._reward_stream)


class ShouldMakeTetrisScore(TestCase):
    def test(self):
        env = make('Tetris-v1')
        self.assertEqual('lines', env._reward_stream)
