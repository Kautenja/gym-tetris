"""Test cases for the command line playback helpers."""
import contextlib
import io
from unittest import TestCase
from unittest.mock import Mock, patch

import gymnasium as gym
import numpy as np

from ..actions import MOVEMENT, SIMPLE_MOVEMENT
from .._app import cli


class SeedProbeEnv(gym.Env):
    """Minimal Gymnasium env that records reset seeds."""

    metadata = {}
    action_space = gym.spaces.Discrete(2)
    observation_space = gym.spaces.Box(
        low=0,
        high=255,
        shape=(1,),
        dtype=np.uint8,
    )

    def __init__(self):
        """Initialize the probe."""
        self.reset_calls = []

    def reset(self, *, seed=None, options=None):
        """Record reset inputs and return a valid Gymnasium reset tuple."""
        self.reset_calls.append((seed, options))
        return np.zeros((1,), dtype=np.uint8), {}

    def step(self, action):
        """Return a valid Gymnasium step tuple."""
        return np.zeros((1,), dtype=np.uint8), 0.0, True, False, {}


class ShouldParseCliPlaybackOptions(TestCase):
    def test_random_mode_accepts_headless_seeded_playback_options(self):
        args = cli._get_args([
            '--env', 'TetrisB-v3',
            '--mode', 'random',
            '--steps', '7',
            '--no-render',
            '--seed', '123',
            '--actionspace', 'simple',
        ])

        self.assertEqual('TetrisB-v3', args.env)
        self.assertEqual('random', args.mode)
        self.assertEqual(7, args.steps)
        self.assertFalse(args.render)
        self.assertEqual(123, args.seed)
        self.assertEqual('simple', args.actionspace)

    def test_human_mode_rejects_no_render(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as context:
                cli._get_args(['--mode', 'human', '--no-render'])

        self.assertEqual(2, context.exception.code)
        self.assertIn(
            'human mode requires graphical rendering',
            stderr.getvalue(),
        )


class ShouldSeedFirstReset(TestCase):
    def test_cli_seed_is_applied_once_to_the_first_reset(self):
        base_env = SeedProbeEnv()
        env = cli.FirstResetSeed(base_env, 123)

        env.reset()
        env.reset()

        self.assertEqual([(123, None), (None, None)], base_env.reset_calls)

    def test_explicit_first_reset_seed_consumes_cli_seed(self):
        base_env = SeedProbeEnv()
        env = cli.FirstResetSeed(base_env, 123)

        env.reset(seed=456)
        env.reset()

        self.assertEqual([(456, None), (None, None)], base_env.reset_calls)


class ShouldRunCliPlayback(TestCase):
    def test_random_no_render_does_not_request_human_render_mode(self):
        base_env = SeedProbeEnv()

        with patch.object(cli.gym, 'make', return_value=base_env) as make:
            with patch.object(cli, 'play_random') as play_random:
                cli.main([
                    '--mode', 'random',
                    '--steps', '5',
                    '--no-render',
                    '--seed', '123',
                ])

        make.assert_called_once_with('TetrisA-v0', render_mode=None)
        env = play_random.call_args.args[0]
        self.assertIsInstance(env, cli.FirstResetSeed)
        play_random.assert_called_once_with(env, 5, render=False)

        env.reset()
        self.assertEqual([(123, None)], base_env.reset_calls)

    def test_random_render_requests_human_render_mode(self):
        base_env = Mock()

        with patch.object(cli.gym, 'make', return_value=base_env) as make:
            with patch.object(cli, 'play_random') as play_random:
                cli.main(['--mode', 'random', '--steps', '3'])

        make.assert_called_once_with('TetrisA-v0', render_mode='human')
        play_random.assert_called_once_with(base_env, 3, render=True)

    def test_human_mode_uses_human_playback(self):
        base_env = Mock()

        with patch.object(cli.gym, 'make', return_value=base_env) as make:
            with patch.object(cli, 'play_human') as play_human:
                cli.main(['--mode', 'human'])

        make.assert_called_once_with('TetrisA-v0', render_mode=None)
        play_human.assert_called_once_with(base_env)


class ShouldConfigureActionSpaces(TestCase):
    def test_public_action_presets_are_available_to_the_cli(self):
        self.assertIs(MOVEMENT, cli._ACTION_SPACES['standard'])
        self.assertIs(SIMPLE_MOVEMENT, cli._ACTION_SPACES['simple'])

    def test_selected_action_space_wraps_environment_before_playback(self):
        base_env = Mock()
        wrapped_env = Mock()

        with patch.object(cli.gym, 'make', return_value=base_env):
            with patch.object(
                cli,
                'JoypadSpace',
                return_value=wrapped_env,
            ) as joypad_space:
                with patch.object(cli, 'play_random') as play_random:
                    cli.main([
                        '--mode', 'random',
                        '--no-render',
                        '--actionspace', 'standard',
                    ])

        joypad_space.assert_called_once_with(base_env, MOVEMENT)
        play_random.assert_called_once_with(wrapped_env, 500, render=False)
