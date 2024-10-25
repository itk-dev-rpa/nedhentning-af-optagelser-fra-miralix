"""This module contains the main process of the robot."""

import os

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from robot_framework.miralix import miralix_api
from robot_framework.get_organized import get_organized_api
import config


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")
    files = miralix_api.download_from_queues(orchestrator_connection)

    get_organized_login = oc.get_credential(config.GO_CREDENTIALS)
    session = get_organized_api.create_session(APIURL, get_organized_login.username, get_organized_login.password)
    for file in files:
        get_organized_api.upload_document(config.GO_API, session, file, config.GO_CASE_ID)


if __name__ == '__main__':
    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Miralix Nedhentning", conn_string, crypto_key, '{"target_queues":["89403330 Opkrævningen P-Gap","89403330 Opkrævningen P-Gap Boliglån tast 2", "89404130 BS - Kørekort P-GAP", "89402000 Aarhus Kommunes Hovednummer NPS", "89402088 Janni testnummer NPS", "89402260 BS - Vielseskontoret NPS"]}')
    
    process(oc)
