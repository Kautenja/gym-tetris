"""A list of discrete actions that are legal in the game."""


MOVEMENT = [
    ['NOOP'],
    ['A'],
    ['B'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['left'],
    ['left', 'A'],
    ['left', 'B'],
    ['down'],
    ['down', 'A'],
    ['down', 'B'],
]


SIMPLE_MOVEMENT = [
    ['NOOP'],
    ['A'],
    ['B'],
    ['right'],
    ['left'],
    ['down'],
]
