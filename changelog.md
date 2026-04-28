# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-28

### Changed

- Bumped OpenOrchestrator to 3.*
- Switched main.py bootstrap to uv

## [1.0.2]

### Fixes

- Will only look at queue elements from the last 20 days to avoid missing reference due to GDPR cleanup.

## [1.0.1]

### Fixed

- If running without existing queue elements, the robot will not fail.

## [1.0.0]

### Added

- Recordings are downloaded from Miralix and uploaded to GetOrganized

[1.0.2]: https://github.com/itk-dev-rpa/nedhentning-af-optagelser-fra-miralix/releases/tag/1.0.2
[1.0.1]: https://github.com/itk-dev-rpa/nedhentning-af-optagelser-fra-miralix/releases/tag/1.0.1
[1.0.0]: https://github.com/itk-dev-rpa/nedhentning-af-optagelser-fra-miralix/releases/tag/1.0.0
