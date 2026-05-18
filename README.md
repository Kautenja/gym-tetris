# gym-tetris

[![BuildStatus][build-status]][ci-server]
[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[build-status]: https://github.com/Kautenja/gym-tetris/actions/workflows/ci.yml/badge.svg?branch=master
[ci-server]: https://github.com/Kautenja/gym-tetris/actions/workflows/ci.yml
[pypi-version]: https://badge.fury.io/py/gym-tetris.svg
[pypi-license]: https://img.shields.io/pypi/l/gym-tetris.svg
[pypi-status]: https://img.shields.io/pypi/status/gym-tetris.svg
[pypi-format]: https://img.shields.io/pypi/format/gym-tetris.svg
[pypi-home]: https://badge.fury.io/py/gym-tetris
[python-version]: https://img.shields.io/pypi/pyversions/gym-tetris.svg
[python-home]: https://python.org

<p align="center">
<img
  src="https://user-images.githubusercontent.com/2184469/58226585-ee152500-7cec-11e9-84a9-1658e4012361.jpg"
  height="300px" />
<img
  src="https://user-images.githubusercontent.com/2184469/58226782-cffbf480-7ced-11e9-8f55-a42baae35fbd.png"
  width="320px" />
</p>

A [Gymnasium](https://gymnasium.farama.org/) environment for Tetris on The
Nintendo Entertainment System (NES) based on the
[nes-py](https://github.com/Kautenja/nes-py) emulator. It currently supports
CPython 3.13 and 3.14 in CI.

## Installation

The preferred installation of `gym-tetris` is from `pip`:

```shell
pip install gym-tetris
```

Python 3.13 or newer is required. The supported CI targets are CPython 3.13
and 3.14.

## Usage

### Python

You must import `gym_tetris` before trying to make an environment.
This is because Gymnasium environments are registered at runtime. By default,
`gym_tetris` environments use the full NES action space of 256
discrete actions. To constrain this, `gym_tetris.actions` provides
an action list called `MOVEMENT` (12 discrete actions) for the
`nes_py.wrappers.JoypadSpace` wrapper. There is also
`SIMPLE_MOVEMENT` with a reduced action space (6 actions). For exact details,
see [gym_tetris/actions.py](gym_tetris/actions.py).

```python
import gymnasium as gym
import gym_tetris
from gym_tetris.actions import MOVEMENT
from nes_py.wrappers import JoypadSpace

env = gym.make('TetrisA-v0', render_mode='rgb_array')
env = JoypadSpace(env, MOVEMENT)

observation, info = env.reset(seed=123)
terminated = False
truncated = False

for step in range(5000):
    if terminated or truncated:
        observation, info = env.reset(seed=123)
        terminated = False
        truncated = False
    observation, reward, terminated, truncated, info = env.step(
        env.action_space.sample(),
    )
    frame = env.render()

env.close()
```

**NOTE:** `gym_tetris.make` is just an alias to `gymnasium.make` for
convenience.

**NOTE:** remove calls to `render` in training code for a nontrivial
speedup.

### Command Line

`gym_tetris` features a command line interface for playing
environments using either the keyboard, or uniform random movement.

```shell
gym_tetris -h
gym_tetris --env TetrisA-v0 --mode human --actionspace simple
gym_tetris --env TetrisA-v0 --mode random --steps 100 --render --seed 123
gym_tetris --env TetrisA-v0 --mode random --steps 100 --no-render --actionspace simple --seed 123
gym_tetris --env TetrisB-v0 --mode random --steps 100 --render --actionspace standard
```

Human mode requires rendering, so `--mode human --no-render` is rejected.
Use `--seed/-S` to seed only the first environment reset in CLI playback.

## Environments

There are two game modes defined in NES Tetris, namely, A-type and B-type.
A-type is the standard endurance Tetris game and B-type is an arcade style mode
where the agent must clear a certain number of lines to win. There are three
potential reward streams: (1) the change in score, (2) the change in number of
lines cleared, and (3) a penalty for an increase in board height. The table
below defines the available environments in terms of the game mode (i.e.,
A-type or B-type) and the rewards applied.

| Environment  | Game Mode | reward score | reward lines | penalize height |
|:-------------|:----------|:-------------|:-------------|:----------------|
| `TetrisA-v0` | A-type    | &#9989;      | &#10005;     | &#10005;        |
| `TetrisA-v1` | A-type    | &#10005;     | &#9989;      | &#10005;        |
| `TetrisA-v2` | A-type    | &#9989;      | &#10005;     | &#9989;         |
| `TetrisA-v3` | A-type    | &#10005;     | &#9989;      | &#9989;         |
| `TetrisB-v0` | B-type    | &#9989;      | &#10005;     | &#10005;        |
| `TetrisB-v1` | B-type    | &#10005;     | &#9989;      | &#10005;        |
| `TetrisB-v2` | B-type    | &#9989;      | &#10005;     | &#9989;         |
| `TetrisB-v3` | B-type    | &#10005;     | &#9989;      | &#9989;         |

## `info` dictionary

The `info` dictionary returned by the `step` method contains the following
keys:

| Key               | Type    | Description
|:------------------|:--------|:---------------------------------------------|
| `current_piece`   | `str`   | the current piece as a string
| `number_of_lines` | `int`   | the number of cleared lines in [0, 999]
| `score`           | `int`   | the current score of the game in [0, 999999]
| `next_piece`      | `str`   | the next piece on deck as a string
| `statistics`      | `dict`  | the number of tetriminos dispatched (by type)
| `board_height`    | `int`   | the height of the board in [0, 20]

## Publishing

PyPI releases are published by the `Publish to PyPI` GitHub Actions workflow
through PyPI trusted publishing, not by local `twine` credentials. Configure
the PyPI project publisher with owner `Kautenja`, repository `gym-tetris`,
workflow filename `publish.yml`, and environment `pypi`.

Releases should follow the current GitHub Actions flow:

1. Create and push a tag that matches `pyproject.toml`'s version, with or
   without a leading `v`.
2. Let CI build the tagged distribution artifacts.
3. Publish a GitHub Release from that tag to trigger the trusted-publishing
   workflow.

Build distributions locally with `python -m build` only for verification, not
for authenticated upload.

## Citation

Please cite `gym-tetris` if you use it in your research.

```tex
@misc{gym-tetris,
  author = {Christian Kauten},
  howpublished = {GitHub},
  title = {{Tetris (NES)} for {Gymnasium}},
  URL = {https://github.com/Kautenja/gym-tetris},
  year = {2019},
}
```

## References

The following references contributed to the construction of this project.

1. [Tetris (NES): RAM Map](https://datacrystal.romhacking.net/wiki/Tetris_(NES)). _Data Crystal ROM Hacking_.
2. [Tetris: Memory Addresses](http://www.thealmightyguru.com/Games/Hacking/Wiki/index.php?title=Tetris#Memory_Addresses). _NES Hacker._
3. [Applying Artificial Intelligence to Nintendo Tetris](https://meatfighter.com/nintendotetrisai/). _MeatFighter._
