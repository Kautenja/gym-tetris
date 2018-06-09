# gym-![T][]etris

[T]: https://user-images.githubusercontent.com/2184469/41186381-ebd61f8c-6b5a-11e8-98ce-874e29801308.png

[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[pypi-version]: https://badge.fury.io/py/gym-tetris.svg
[pypi-license]: https://img.shields.io/pypi/l/gym-tetris.svg
[pypi-status]: https://img.shields.io/pypi/status/gym-tetris.svg
[pypi-format]: https://img.shields.io/pypi/format/gym-tetris.svg
[pypi-home]: https://badge.fury.io/py/gym-tetris
[python-version]: https://img.shields.io/pypi/pyversions/gym-tetris.svg
[python-home]: https://python.org

An [OpenAI Gym](https://github.com/openai/gym) environment for Tetris. This
environemnt derives from the [Tetromino clone][Tetromino] developed by Al
Sweigart.

![Tetris](https://user-images.githubusercontent.com/2184469/41186404-826ebba2-6b5b-11e8-8215-eb21d765b0b9.png)

[Tetromino]: http://inventwithpython.com/blog/2010/11/18/code-comments-tutorial-tetromino/


# Installation

The preferred installation of `gym-tetris` is from `pip`:

```shell
pip install gym-tetris
```

# Usage

## Python

You must import `gym_tetris` before trying to make an environment. This is
because gym environments are registered at runtime.

```python
import gym_tetris
env = gym_tetris.make('Tetris-v0')

done = True
for step in range(5000):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())

env.close()
```

**NOTE:** `gym_tetris.make` is just an alias to `gym.make` for
convenience.

## Command Line

`gym_tetris` feature a command line interface for playing environments using
either the keyboard, or uniform random movement.

```shell
gym_tetris -e <the environment ID to play> -m <`human` or `random`>
```

**NOTE:** by default, `-e` is set to `Tetris-v0` and `-m` is set to
`human`.

# Citation

Please cite `gym-tetris` if you use it in your research.

```tex
@misc{gym-tetris,
  author = {Albert Sweigart and Christian Kauten},
  title = {{Tetris} for {OpenAI Gym}},
  year = {2018},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Kautenja/gym-tetris}},
}
```
