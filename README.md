# gym-<img src='https://github.com/Kautenja/gym-tetris/blob/master/sketch/T.svg' width=40 height=20/>etris

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

An [OpenAI Gym](https://github.com/openai/gym) environment for Tetris. This environemnt 
derives from the Tetromino clone developed by Al Sweigart found [here][Tetromino].

[Tetromino]: http://inventwithpython.com/blog/2010/11/18/code-comments-tutorial-tetromino/

# Installation

The preferred installation of `gym-tetris` is from `pip`:

```shell
pip install gym-tetris
```

# Usage

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
