"""The setup script for installing the package."""
from setuptools import setup, find_packages


# read the contents of the README
with open('README.md') as README_md:
    README = README_md.read()


setup(
    name='gym_tetris',
    version='2.0.1',
    description='Tetris (NES) for OpenAI Gym',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=' '.join([
        'OpenAI-Gym',
        'NES',
        'Tetris',
        'Reinforcement-Learning-Environment',
    ]),
    classifiers=[
        'License :: Free For Educational Use',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    url='https://github.com/Kautenja/gym-tetris',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='Proprietary',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    package_data={ 'gym_tetris': ['_roms/*.nes'] },
    install_requires=['nes-py>=6.2.1'],
    entry_points={
        'console_scripts': [
            'gym_tetris = gym_tetris._app.cli:main',
        ],
    },
)
