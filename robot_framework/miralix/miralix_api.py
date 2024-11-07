"""API wrappers for interacting with Miralix"""

import json
import os

import requests
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from robot_framework import config


def recordings_for_process(orchestrator_connection: OrchestratorConnection, from_queue_call_id: int = 0) -> list[str]:
    """Get list of recordings from queues specified in process_arguments,
    with an ID higher than the ID provided.

    Args:
        orchestrator_connection: Connection object to OpenOrchestrator.
        from_queue_call_id: Call ID to start download from. Defaults to 0.

    Return:
        List of recordings.
    """
    headers = {
        "X-Miralix-Shared-Secret": orchestrator_connection.get_credential(config.SSK).password
    }

    queue_names = json.loads(orchestrator_connection.process_arguments)["target_queues"]
    target_queues = get_miralix_data("queues", headers=headers)

    params = {
        "fromQueueCallId": from_queue_call_id
    }

    recordings = []
    for queue in queue_names:
        queue_id = get_queue_id(queue, target_queues)
        if queue_id:
            calls = get_miralix_data(f"queues/{queue_id}/calls/recordings", headers=headers, params=params)
            if calls:
                recordings.extend(calls)
    return recordings


def get_miralix_data(endpoint, headers, params=None, ) -> json:
    """Contact Miralix API endpoint to receive JSON data.

    Args:
        endpoint: URL after our Miralix ID for endpoint, eg. 'queues/'
        params: Parameters for get request
        headers: Header for get request. Requires an SSK from Miralix

    Returns:
        JSON formatted data.
    """
    response = requests.get(f"{config.MIRALIX_BASE_URL}/{endpoint}", params=params, headers=headers, timeout=config.MIRALIX_TIMEOUT)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def download_file(call_id, password):
    """Download a specified file from Miralix.

    Args:
        call_id: ID of the call to download
        password: password for Miralix

    Returns:
        The file content downloaded.
    """
    headers = {
        "X-Miralix-Shared-Secret": password
    }
    return requests.get(f'{config.MIRALIX_BASE_URL}/queues/calls/recordings/{call_id}', headers=headers, timeout=config.MIRALIX_TIMEOUT).content


def get_filename(recording) -> str:
    """Generate a filename from a recording.

    Args:
        recording: Recording object from json.

    Returns:
        An mp3 filename in the format 'queue_time-started_agent_caller_file-id.mp3'.
    """
    queue = recording["QueueName"].replace(' ', '')[8:]
    time_started = recording["ConversationStartedUtc"][:19].replace(":", "-")
    agent = recording["AgentName"].replace(' ', '')
    caller = recording["Caller"][4:]  # Only use last four digits for privacy reasons
    file_id = recording["QueueCallId"]
    return f"{queue}_{time_started}_{agent}_{caller}_{file_id}.mp3"


def get_queue_id(queue_name: str, queues: object) -> str:
    """Find the ID of the queue with 'queue_name' in the 'queue' json object.

    Args:
        queue_name: The name of the queue we are looking for.
        queues: A JSON with a collection of queues.

    Returns:
        Return the ID of the queue.
    """
    queue_name = queue_name.strip()
    for queue in queues:
        if queue["Name"] == queue_name:
            return queue["Id"]
    return None


if __name__ == "__main__":
    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Miralix Nedhentning", conn_string, crypto_key, '{"target_queues":["89403330 Opkrævningen P-Gap","89403330 Opkrævningen P-Gap Boliglån tast 2", "89404130 BS - Kørekort P-GAP", "89402000 Aarhus Kommunes Hovednummer NPS", "89402088 Janni testnummer NPS", "894022config.MIRALIX_TIMEOUT BS - Vielseskontoret NPS"]}')
    recordings_for_process(oc)
