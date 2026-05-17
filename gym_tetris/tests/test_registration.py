"""Test cases for the gym registered environments."""
from unittest import TestCase
from .. import make


def unwrap(env):
    """Return the base environment under Gym API compatibility wrappers."""
    return env.unwrapped


class ShouldMakeTetrisAv0(TestCase):
    def test(self):
        env = unwrap(make('TetrisA-v0'))
        self.assertFalse(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisAv1(TestCase):
    def test(self):
        env = unwrap(make('TetrisA-v1'))
        self.assertFalse(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisAv2(TestCase):
    def test(self):
        env = unwrap(make('TetrisA-v2'))
        self.assertFalse(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldMakeTetrisAv3(TestCase):
    def test(self):
        env = unwrap(make('TetrisA-v3'))
        self.assertFalse(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldMakeTetrisBv0(TestCase):
    def test(self):
        env = unwrap(make('TetrisB-v0'))
        self.assertTrue(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisBv1(TestCase):
    def test(self):
        env = unwrap(make('TetrisB-v1'))
        self.assertTrue(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisBv2(TestCase):
    def test(self):
        env = unwrap(make('TetrisB-v2'))
        self.assertTrue(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldMakeTetrisBv3(TestCase):
    def test(self):
        env = unwrap(make('TetrisB-v3'))
        self.assertTrue(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertTrue(env._penalize_height)
