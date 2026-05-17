"""Test cases for the gym registered environments."""
from unittest import TestCase
from .. import make


class ShouldMakeTetrisAv0(TestCase):
    def test(self):
        env = make('TetrisA-v0')
        self.assertFalse(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisAv1(TestCase):
    def test(self):
        env = make('TetrisA-v1')
        self.assertFalse(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisAv2(TestCase):
    def test(self):
        env = make('TetrisA-v2')
        self.assertFalse(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldMakeTetrisAv3(TestCase):
    def test(self):
        env = make('TetrisA-v3')
        self.assertFalse(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldMakeTetrisBv0(TestCase):
    def test(self):
        env = make('TetrisB-v0')
        self.assertTrue(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisBv1(TestCase):
    def test(self):
        env = make('TetrisB-v1')
        self.assertTrue(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertFalse(env._penalize_height)


class ShouldMakeTetrisBv2(TestCase):
    def test(self):
        env = make('TetrisB-v2')
        self.assertTrue(env._b_type)
        self.assertTrue(env._reward_score)
        self.assertFalse(env._reward_lines)
        self.assertTrue(env._penalize_height)


class ShouldMakeTetrisBv3(TestCase):
    def test(self):
        env = make('TetrisB-v3')
        self.assertTrue(env._b_type)
        self.assertFalse(env._reward_score)
        self.assertTrue(env._reward_lines)
        self.assertTrue(env._penalize_height)
