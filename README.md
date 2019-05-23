# gym-tetris

[![BuildStatus][build-status]][ci-server]
[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[build-status]: https://travis-ci.com/Kautenja/gym-tetris.svg?branch=master
[ci-server]: https://travis-ci.com/Kautenja/gym-tetris
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

An [OpenAI Gym](https://github.com/openai/gym) environment for Tetris on The
Nintendo Entertainment System (NES) based on the
[nes-py](https://github.com/Kautenja/nes-py) emulator.

## Installation

The preferred installation of `gym-tetris` is from `pip`:

```shell
pip install gym-tetris
```

## Usage

### Python

You must import `gym_tetris` before trying to make an environment.
This is because gym environments are registered at runtime. By default,
`gym_tetris` environments use the full NES action space of 256
discrete actions. To constrain this, `gym_tetris.actions` provides
an action list called `MOVEMENT` (20 discrete actions) for the
`nes_py.wrappers.BinarySpaceToDiscreteSpaceEnv` wrapper.

```python
from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
import gym_tetris
from gym_tetris.actions import MOVEMENT

env = gym_tetris.make('Tetris-v0')
env = BinarySpaceToDiscreteSpaceEnv(env, MOVEMENT)

done = True
for step in range(5000):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())
    env.render()

env.close()
```

**NOTE:** `gym_tetris.make` is just an alias to `gym.make` for
convenience.

**NOTE:** remove calls to `render` in training code for a nontrivial
speedup.

### Command Line

`gym_tetris` features a command line interface for playing
environments using either the keyboard, or uniform random movement.

```shell
gym_tetris -m <`human` or `random`>
```

## Step

Info about the rewards and info returned by the `step` method.

### Reward Function

The reward function assumes the objective of the game is to increase the score.
As such, the reward is defined as the instantaneous change in score for a
given action.

### `info` dictionary

The `info` dictionary returned by the `step` method contains the following
keys:

| Key               | Type    | Description
|:------------------|:--------|:------------------------------------------------------|
| `current_piece`   | `str`   | the current piece as a string
| `number_of_lines` | `int`   | the number of cleared lines
| `score`           | `int`   | the current score of the game
| `next_piece`      | `str`   | the next piece on deck
| `statistics`      | `dict`  | statistics for each piece

## Citation

Please cite `gym-tetris` if you use it in your research.

```tex
@misc{gym-tetris,
  author = {Christian Kauten},
  title = {{Tetris (NES)} for {OpenAI Gym}},
  year = {2019},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Kautenja/gym-tetris}},
}
```

## References

The following references contributed to the construction of this project.

1. [Tetris (NES): RAM Map](https://datacrystal.romhacking.net/wiki/Tetris_(NES)). _Data Crystal ROM Hacking_.
2. [Tetris: Memory Addresses](http://www.thealmightyguru.com/Games/Hacking/Wiki/index.php?title=Tetris#Memory_Addresses). _NES Hacker._
3. [Applying Artificial Intelligence to Nintendo Tetris](https://meatfighter.com/nintendotetrisai/). _MeatFighter._
