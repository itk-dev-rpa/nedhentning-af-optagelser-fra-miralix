"""This module contains the main process of the robot."""

import os

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")


if __name__ == '__main__':
    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Nedhentning af optagelser fra Miralix", conn_string, crypto_key, '')
    process(oc)
