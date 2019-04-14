"""Test cases for the tetris_env module."""
from unittest import TestCase
from ..tetris_env import TetrisEnv


class ShouldRaiseTypeErrorOnMissingMaxStepsParam(TestCase):
    def test(self):
        self.assertRaises(TypeError, TetrisEnv)


class ShouldCreateTetrisEnv(TestCase):
    def test(self):
        env = TetrisEnv(max_steps=1000)
