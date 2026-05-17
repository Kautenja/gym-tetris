"""Test cases for the Gymnasium registered environments."""
import warnings
from unittest import TestCase

import gymnasium as gym

from .. import make


REGISTERED_ENVIRONMENTS = {
    'TetrisA-v0': dict(
        b_type=False,
        reward_score=True,
        reward_lines=False,
        penalize_height=False,
    ),
    'TetrisA-v1': dict(
        b_type=False,
        reward_score=False,
        reward_lines=True,
        penalize_height=False,
    ),
    'TetrisA-v2': dict(
        b_type=False,
        reward_score=True,
        reward_lines=False,
        penalize_height=True,
    ),
    'TetrisA-v3': dict(
        b_type=False,
        reward_score=False,
        reward_lines=True,
        penalize_height=True,
    ),
    'TetrisB-v0': dict(
        b_type=True,
        reward_score=True,
        reward_lines=False,
        penalize_height=False,
    ),
    'TetrisB-v1': dict(
        b_type=True,
        reward_score=False,
        reward_lines=True,
        penalize_height=False,
    ),
    'TetrisB-v2': dict(
        b_type=True,
        reward_score=True,
        reward_lines=False,
        penalize_height=True,
    ),
    'TetrisB-v3': dict(
        b_type=True,
        reward_score=False,
        reward_lines=True,
        penalize_height=True,
    ),
}


def unwrap(env):
    """Return the base environment under Gymnasium API wrappers."""
    return env.unwrapped


def make_env(env_id, **kwargs):
    """Create an environment while accepting intentionally versioned IDs."""
    with warnings.catch_warnings():
        warnings.filterwarnings(
            'ignore',
            message='.*The environment .* is out of date.*',
            category=DeprecationWarning,
        )
        return gym.make(env_id, **kwargs)


class ShouldRegisterGymnasiumEnvironments(TestCase):
    def assert_env_configuration(self, env_id, kwargs):
        """Assert a registered environment preserves its constructor options."""
        env = make_env(env_id, render_mode='rgb_array')
        try:
            base = unwrap(env)
            self.assertEqual(kwargs['b_type'], base._b_type)
            self.assertEqual(kwargs['reward_score'], base._reward_score)
            self.assertEqual(kwargs['reward_lines'], base._reward_lines)
            self.assertEqual(kwargs['penalize_height'], base._penalize_height)
            self.assertEqual('rgb_array', base.render_mode)
            self.assertEqual(256, env.action_space.n)
        finally:
            env.close()

    def test_all_registered_ids_are_available_through_gymnasium(self):
        for env_id, kwargs in REGISTERED_ENVIRONMENTS.items():
            with self.subTest(env_id=env_id):
                self.assert_env_configuration(env_id, kwargs)

    def test_make_alias_uses_gymnasium_make(self):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore',
                message='.*The environment .* is out of date.*',
                category=DeprecationWarning,
            )
            env = make('TetrisA-v0', render_mode='rgb_array')
        try:
            self.assertFalse(unwrap(env)._b_type)
            self.assertTrue(unwrap(env)._reward_score)
        finally:
            env.close()


class ShouldUseGymnasiumStepApiForATypeAndBType(TestCase):
    def assert_reset_and_step_api(self, env_id):
        """Assert the public reset and step tuple contracts."""
        env = make_env(env_id, render_mode='rgb_array')
        try:
            reset_result = env.reset(seed=123)
            self.assertIsInstance(reset_result, tuple)
            self.assertEqual(2, len(reset_result))
            observation, info = reset_result
            self.assertEqual((240, 256, 3), observation.shape)
            self.assertIsInstance(info, dict)

            step_result = env.step(env.action_space.sample())
            self.assertIsInstance(step_result, tuple)
            self.assertEqual(5, len(step_result))
            observation, reward, terminated, truncated, info = step_result
            self.assertEqual((240, 256, 3), observation.shape)
            self.assertIsInstance(reward, float)
            self.assertIsInstance(terminated, bool)
            self.assertIsInstance(truncated, bool)
            self.assertIn('score', info)
            self.assertIsNotNone(env.render())
        finally:
            env.close()

    def test_a_type_v0(self):
        self.assert_reset_and_step_api('TetrisA-v0')

    def test_b_type_v0(self):
        self.assert_reset_and_step_api('TetrisB-v0')
