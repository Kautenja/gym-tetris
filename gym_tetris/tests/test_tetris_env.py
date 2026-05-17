"""Test cases for the Tetris Gymnasium environment."""
from unittest import TestCase

import numpy as np

from ..tetris_env import TetrisEnv


EXPECTED_INFO_KEYS = {
    'current_piece',
    'number_of_lines',
    'score',
    'next_piece',
    'statistics',
    'board_height',
}


class RewardProbeTetrisEnv(TetrisEnv):
    """Tetris environment with controllable reward inputs."""

    def __init__(self, **kwargs):
        """Initialize the probe with stable synthetic metrics."""
        self._fake_score = 0
        self._fake_lines = 0
        self._fake_height = 0
        kwargs.setdefault('deterministic', True)
        super().__init__(**kwargs)

    @property
    def _score(self):
        """Return the synthetic score."""
        return self._fake_score

    @property
    def _number_of_lines(self):
        """Return the synthetic number of cleared lines."""
        return self._fake_lines

    @property
    def _board_height(self):
        """Return the synthetic board height."""
        return self._fake_height

    def set_metrics(self, score, lines, height):
        """Set the synthetic reward inputs."""
        self._fake_score = score
        self._fake_lines = lines
        self._fake_height = height


class TetrisEnvAssertions(TestCase):
    """Shared assertions for the public Gymnasium API."""

    def assert_valid_observation(self, observation):
        """Assert that an observation matches the NES RGB frame contract."""
        self.assertIsInstance(observation, np.ndarray)
        self.assertEqual((240, 256, 3), observation.shape)
        self.assertEqual(np.uint8, observation.dtype)

    def assert_is_not_black_screen(self, screen):
        """Assert that the given screen is not empty."""
        self.assertNotEqual(0, screen.sum())

    def assert_info_keys(self, info):
        """Assert that the public Tetris info keys are stable."""
        self.assertEqual(EXPECTED_INFO_KEYS, set(info.keys()))

    def reset_env(self, env, seed=None):
        """Reset an environment and assert the Gymnasium reset tuple."""
        output = env.reset(seed=seed)
        self.assertIsInstance(output, tuple)
        self.assertEqual(2, len(output))
        observation, info = output
        self.assert_valid_observation(observation)
        self.assertIsInstance(info, dict)
        self.assert_info_keys(info)
        return observation, info

    def step_env(self, env, action):
        """Step an environment and assert the Gymnasium step tuple."""
        output = env.step(action)
        self.assertIsInstance(output, tuple)
        self.assertEqual(5, len(output))
        observation, reward, terminated, truncated, info = output
        self.assert_valid_observation(observation)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(terminated, bool)
        self.assertIsInstance(truncated, bool)
        self.assertFalse(truncated)
        self.assertIsInstance(info, dict)
        self.assert_info_keys(info)
        return observation, reward, terminated, truncated, info


class ShouldCreateEnvWithDefaultRewardLines(TestCase):
    def test(self):
        env = TetrisEnv()
        try:
            self.assertFalse(env._b_type)
            self.assertFalse(env._reward_score)
            self.assertTrue(env._reward_lines)
            self.assertTrue(env._penalize_height)
            self.assertIsNone(env.render_mode)
            self.assertEqual(0, env._current_score)
            self.assertEqual(0, env._current_lines)
            self.assertEqual(0, env._current_height)
        finally:
            env.close()


class ShouldCreateEnvWithRewardScore(TestCase):
    def test(self):
        env = TetrisEnv(reward_score=True)
        try:
            self.assertFalse(env._b_type)
            self.assertTrue(env._reward_score)
            self.assertTrue(env._reward_lines)
            self.assertTrue(env._penalize_height)
        finally:
            env.close()


class ShouldCreateEnvWithoutPenalizeHeight(TestCase):
    def test(self):
        env = TetrisEnv(penalize_height=False)
        try:
            self.assertFalse(env._b_type)
            self.assertFalse(env._reward_score)
            self.assertTrue(env._reward_lines)
            self.assertFalse(env._penalize_height)
        finally:
            env.close()


class ShouldCreateEnvWithoutRewardLines(TestCase):
    def test(self):
        env = TetrisEnv(reward_lines=False)
        try:
            self.assertFalse(env._b_type)
            self.assertFalse(env._reward_score)
            self.assertFalse(env._reward_lines)
            self.assertTrue(env._penalize_height)
        finally:
            env.close()


class ShouldCreateEnvWithBType(TestCase):
    def test(self):
        env = TetrisEnv(b_type=True)
        try:
            self.assertTrue(env._b_type)
            self.assertFalse(env._reward_score)
            self.assertTrue(env._reward_lines)
            self.assertTrue(env._penalize_height)
        finally:
            env.close()


class ShouldSupportRenderMode(TetrisEnvAssertions):
    def test(self):
        env = TetrisEnv(render_mode='rgb_array')
        try:
            observation, _ = self.reset_env(env, seed=1)
            self.assertIs(env.render(), env.screen)
            self.assert_valid_observation(env.render())
            self.assertTrue(np.array_equal(observation, env.render()))
        finally:
            env.close()


class ShouldStep(TetrisEnvAssertions):
    def test(self):
        env = TetrisEnv(deterministic=True)
        try:
            _ = self.reset_env(env, seed=1)
            _, reward, terminated, truncated, info = self.step_env(env, 0)
            self.assertEqual(0, reward)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertEqual('Jd', info['current_piece'])
            self.assertEqual(0, info['number_of_lines'])
            self.assertEqual(0, info['score'])
            self.assertEqual('Zh', info['next_piece'])
            stats = {'T': 0, 'J': 1, 'Z': 0, 'O': 0, 'S': 0, 'L': 0, 'I': 0}
            self.assertEqual(stats, info['statistics'])
        finally:
            env.close()


class ShouldUseGymnasiumResetSeeding(TetrisEnvAssertions):
    def snapshot(self, env, seed):
        """Return a copied reset snapshot for deterministic comparisons."""
        observation, info = self.reset_env(env, seed=seed)
        return observation.copy(), info.copy()

    def test_seeded_non_deterministic_mode_is_reproducible(self):
        env = TetrisEnv()
        try:
            first_state, first_info = self.snapshot(env, seed=123)
            self.step_env(env, 0)
            second_state, second_info = self.snapshot(env, seed=123)
            self.assertTrue(np.array_equal(first_state, second_state))
            self.assertEqual(first_info, second_info)
        finally:
            env.close()

    def test_deterministic_mode_ignores_seeded_rng_variation(self):
        env = TetrisEnv(deterministic=True)
        try:
            first_state, first_info = self.snapshot(env, seed=123)
            self.step_env(env, 0)
            second_state, second_info = self.snapshot(env, seed=456)
            self.assertTrue(np.array_equal(first_state, second_state))
            self.assertEqual(first_info, second_info)
        finally:
            env.close()


class ShouldCalculateRewardModes(TestCase):
    def test(self):
        cases = [
            (
                'score',
                dict(
                    reward_score=True,
                    reward_lines=False,
                    penalize_height=False,
                ),
                100,
            ),
            (
                'lines',
                dict(
                    reward_score=False,
                    reward_lines=True,
                    penalize_height=False,
                ),
                2,
            ),
            (
                'score_height',
                dict(
                    reward_score=True,
                    reward_lines=False,
                    penalize_height=True,
                ),
                97,
            ),
            (
                'lines_height',
                dict(
                    reward_score=False,
                    reward_lines=True,
                    penalize_height=True,
                ),
                -1,
            ),
        ]
        for name, kwargs, expected_reward in cases:
            with self.subTest(name=name):
                env = RewardProbeTetrisEnv(**kwargs)
                try:
                    env.set_metrics(score=100, lines=2, height=3)
                    self.assertEqual(expected_reward, env._get_reward())
                    self.assertEqual(100, env._current_score)
                    self.assertEqual(2, env._current_lines)
                    self.assertEqual(3, env._current_height)
                finally:
                    env.close()


class ShouldTerminate(TetrisEnvAssertions):
    def test_game_over_uses_gymnasium_terminated_hook(self):
        env = TetrisEnv()
        try:
            self.reset_env(env, seed=1)
            env.ram[0x0058] = 1
            self.assertTrue(env._get_terminated())
        finally:
            env.close()


class ShouldCompleteEpisode(TetrisEnvAssertions):
    def test(self):
        env = TetrisEnv()
        try:
            state, _ = self.reset_env(env, seed=1)
            self.assert_is_not_black_screen(state)
            done = False
            for _ in range(10000):
                state, _, terminated, truncated, _ = self.step_env(env, 0)
                self.assert_is_not_black_screen(state)
                done = terminated or truncated
                if done:
                    break
            self.assertTrue(done)
            state, _ = self.reset_env(env, seed=1)
            self.assert_is_not_black_screen(state)
        finally:
            env.close()
