# Changelog

All notable changes to `gym-tetris` are documented in this file.

This changelog was reconstructed from local git tags, version metadata, and
repository history.

## 4.0.0 (upcoming)

Current package metadata in `pyproject.toml` is set to `4.0.0`, but no local
`4.0.0` tag exists yet.

### Highlights

- Migrated the package from the legacy Gym API to Gymnasium, including updated
  environment reset and step behavior, CLI support, and refreshed tests.
- Modernized packaging by replacing `setup.py` with `pyproject.toml`.
- Aligned CI and supported Python versions with `nes-py`.
- Added GitHub Actions workflows for CI and trusted PyPI publishing.
- Replaced the old makefile-oriented maintenance flow with `main.sh`.
- Clarified wrapper bootstrap metadata policy in `requirements.txt`.

### Release notes

- Expect this release to be the first Gymnasium-native major version.
- Downstream users should plan for API updates consistent with Gymnasium's
  `reset()` and `step()` signatures.
- Release automation now assumes GitHub Actions plus PyPI trusted publishing.

## 3.0.4 - 2022-09-09

- Removed an extra reset call during deterministic environment setup.

## 3.0.3 - 2022-09-09

- Added CLI random seed support.
- Fixed random number seeding in the Tetris environment for more reliable
  reproducibility.

## 3.0.2 - 2019-06-02

- Avoided replaying the start-screen flow on every reset.
- Improved game completion handling for win conditions.

## 3.0.1 - 2019-06-02

- Added `board_height` to the environment `info` dictionary.

## 3.0.0 - 2019-06-02

- Introduced separate A-type and B-type Tetris environments.
- Updated registration and documentation for the split game modes.

## 2.3.0 - 2019-06-02

- Added reward variants that combine line-based rewards with board-height
  penalties.
- Added board-height tracking used by the new reward modes.

## 2.2.3 - 2019-06-02

- Updated CLI behavior and package metadata around the `2.2.x` release line.

## 2.2.2 - 2019-05-29

- Fixed the line-count reward stream so it triggers only once per clear.
- Fixed command-line environment selection.

## 2.2.1 - 2019-05-24

- Refreshed project metadata and maintenance scripts.

## 2.2.0 - 2019-05-24

- Added a new alternate reward stream.
- Added a CLI environment flag.
- Documented the new environment and reward behavior.

## 2.1.0 - 2019-05-24

- Updated action definitions and package configuration ahead of the `2.2.x`
  reward-stream work.

## 2.0.2 - 2019-05-23

- Fixed a post-`2.0.1` packaging/runtime error.

## 2.0.1 - 2019-05-23

- Shipped a quick follow-up release after the `2.0.0` backend transition.

## 2.0.0 - 2019-05-23

- Merged the `nes-backend` work that re-based the project on the newer
  emulator/backend stack.

## 0.1.0 - 1.2.10

- Early releases established the initial NES Tetris environment, human/random
  play support, packaging refinements, wheel/source distribution fixes, scoring
  updates, frame-limit and server-rendering fixes, and CLI/application
  refactors.
- The `1.2.x` line also introduced the height-related work that later informed
  the `board_height` info field and reward variants.
