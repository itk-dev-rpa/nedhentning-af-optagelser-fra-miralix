# Download of recordings from Miralix
This project is based on the [ITK Robot Framework](https://github.com/itk-dev-rpa/Robot-Framework), for use with [OpenOrchestrator](https://github.com/itk-dev-rpa/OpenOrchestrator) and Miralix.
Using the Miralix API, we extract recordings from a set of phone queues, and download the files to a folder.

## Quick start

1. Setup a trigger in OpenOrchestrator with this repository
2. Add queues as parameters to the trigger
3. Define the target folder for downloads as a parameter as well
4. Define weather to download all recordings from queues, or only new recordings

## Requirements
Minimum python version 3.10

## Linting and Github Actions

This template is also setup with flake8 and pylint linting in Github Actions.
This workflow will trigger whenever you push your code to Github.
The workflow is defined under `.github/workflows/Linting.yml`.

