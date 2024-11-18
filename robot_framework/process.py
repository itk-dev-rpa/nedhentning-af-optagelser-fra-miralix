"""This module contains the main process of the robot."""

import os
import json

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection, QueueStatus

from robot_framework.miralix import miralix_api
from robot_framework.get_organized import get_organized_api
from robot_framework import config


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")

    get_organized_login = orchestrator_connection.get_credential(config.GO_CREDENTIALS)
    session = get_organized_api.create_session(config.GO_API, get_organized_login.username, get_organized_login.password)
    miralix_password = orchestrator_connection.get_credential(config.MIRALIX_SHARED_KEY).password
    case_number = json.loads(orchestrator_connection.process_arguments)["case_number"]

    #  Check queue elements for highest call ID previously downloaded
    queue_elements = orchestrator_connection.get_queue_elements(config.QUEUE_NAME, status=QueueStatus.DONE)
    last_download = max(int(queue_element.reference) for queue_element in queue_elements)

    #  Get list of recordings that have a higher ID than the previous highest, and sort them
    recordings = miralix_api.recordings_for_process(orchestrator_connection, last_download)
    recordings.sort(key=lambda recording: recording["QueueCallId"])

    #  Run through each recording, download file data and send to GetOrganized
    for i, recording in enumerate(recordings):
        call_id = recording["QueueCallId"]
        filename = miralix_api.get_filename(recording)
        print(f"{i+1}/{len(recordings)} - Call ID {call_id} being saved as {filename}")

        #  Set queue status
        queue_element = orchestrator_connection.create_queue_element(config.QUEUE_NAME, call_id, data=filename)
        orchestrator_connection.set_queue_element_status(queue_element.id, QueueStatus.IN_PROGRESS)

        #  Get file data and upload to GetOrganized as a list of bytes
        file_data = list(miralix_api.download_file(call_id, miralix_password))
        get_organized_api.upload_document(apiurl=config.GO_API,
                                          session=session,
                                          file=file_data,
                                          case=case_number,
                                          filename=filename,
                                          agent_name=recording["AgentName"],
                                          date_string=recording["ConversationStartedUtc"])

        orchestrator_connection.set_queue_element_status(queue_element.id, QueueStatus.DONE)


if __name__ == '__main__':
    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Miralix Nedhentning", conn_string, crypto_key, '{"case_number": "EMN-2024-033020", "target_queues":["89403330 Opkrævningen P-Gap","89403330 Opkrævningen P-Gap Boliglån tast 2", "89404130 BS - Kørekort P-GAP", "89402000 Aarhus Kommunes Hovednummer NPS", "89402088 Janni testnummer NPS", "89402260 BS - Vielseskontoret NPS"]}')
    process(oc)
