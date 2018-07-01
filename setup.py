from setuptools import setup, find_packages


def README() -> str:
    """Return the contents of the README file for this project."""
    with open('README.md') as README_file:
        return README_file.read()


setup(
    name='gym_tetris',
    setup_requires=[
        'very-good-setuptools-git-version'
    ],
    version_format='{tag}',
    description='Tetris for OpenAI Gym',
    long_description=README(),
    long_description_content_type='text/markdown',
    keywords='OpenAI-Gym Tetris Reinforcement-Learning-Environment',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment :: Arcade',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/Kautenja/gym-tetris',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'gym>=0.10.5',
        'matplotlib>=2.0.2',
        'numpy>=1.14.2',
        'opencv-python>=3.4.0.12',
        'pygame>=1.9.3',
        'pyglet>=1.3.2',
        'tqdm>=4.19.5',
    ],
    entry_points={
        'console_scripts': [
            'gym_tetris = gym_tetris._app.cli:main',
        ],
    },
)
