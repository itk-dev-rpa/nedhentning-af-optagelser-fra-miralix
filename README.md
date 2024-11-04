# Download of recordings from Miralix
This project is based on the [ITK Robot Framework](https://github.com/itk-dev-rpa/Robot-Framework), for use with [OpenOrchestrator](https://github.com/itk-dev-rpa/OpenOrchestrator) and Miralix.

Using the Miralix API, we extract recordings from a set of phone queues, and send these recordings to GetOrganized ESDH.

## Quick start

1. Setup a trigger and Miralix Shared Key in OpenOrchestrator.
3. Setup a case in GetOrganized, making sure metadata is setup properly.
2. Set Miralix queues and case number as parameters to the trigger: 
```
{"case_number": "EMN-2024-123456", "target_queues":["89403330 Opkrævningen P-Gap","89403330 Opkrævningen P-Gap Boliglån tast 2")]}
```
4. Run the trigger.

## Requirements
Minimum python version 3.10

## Linting and Github Actions

This template is also setup with flake8 and pylint linting in Github Actions.
This workflow will trigger whenever you push your code to Github.
The workflow is defined under `.github/workflows/Linting.yml`.

