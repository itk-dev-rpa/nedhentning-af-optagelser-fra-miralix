"""API wrappers for interacting with Miralix"""

import requests
import json
import os

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from robot_framework import config


def download_from_queues(orchestrator_connection: OrchestratorConnection):
    """Download files from the queues specified in the process arguments.

    Args:
        orchestrator_connection: Connection object to OpenOrchestrator
    """
    headers = {
        "X-Miralix-Shared-Secret": orchestrator_connection.get_credential(config.SSK).password
    }

    queue_names = json.loads(orchestrator_connection.process_arguments)["target_queues"]
    target_queues = get_miralix_data("queues", headers=headers)

    params = {
        "fromQueueCallId": get_last_download_id()
    }

    for queue in queue_names:
        queue_id = get_queue_id(queue, target_queues)
        if queue_id:
            recordings = get_miralix_data(f"queues/{queue_id}/calls/recordings", headers=headers, params=params)
            return download_files(recordings, config.DOWNLOAD_LOCATION, headers=headers)


def get_miralix_data(endpoint, headers, params=None, ) -> json:
    """Contact Miralix API endpoint to receive JSON data.

    Args:
        endpoint: URL after our Miralix ID for endpoint, eg. 'queues/'
        params: Parameters for get request
        headers: Header for get request. Requires an SSK from Miralix

    Returns:
        JSON formatted data.
    """
    response = requests.get(f"{config.MIRALIX_BASE_URL}/{endpoint}", params=params, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def download_files(recordings, destination, headers) -> list[str]:
    """Download files for list of recordings.

    Args:
        recordings: List of json objects representing recordings in the API.
        destination: The local folder to store the files in.
        headers: Headers for the HTTP request.

    Returns:
        List of path of files that have been downloaded.
    """
    files = []
    for recording in recordings:
        file_data = requests.get(f"{config.MIRALIX_BASE_URL}/queues/calls/recordings/{recording["QueueCallId"]}", headers=headers).content
        file_name = f"{destination}/{get_filename(recording)}"
        with open(file_name, mode="wb") as file:
            file.write(file_data)
        files.append(file_name)
    return files


def get_filename(recording) -> str:
    """Generate a filename from a recording.

    Args:
        recording: Recording object from json.

    Returns:
        An mp3 filename in the format 'queue_time-started_agent_file-id.mp3'.
    """
    queue = recording["QueueName"].replace(' ', '')[8:]
    time_started = recording["ConversationStartedUtc"][:19].replace(":", "-")
    agent = recording["AgentName"].replace(' ', '')
    file_id = recording["QueueCallId"]
    return f"{queue}_{time_started}_{agent}_{file_id}.mp3"


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


def get_last_download_id() -> int:
    """Get the ID of the latest call recording downloaded.

    Returns:
        A call ID as an int.
    """
    folder_path = config.DOWNLOAD_LOCATION
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    highest_id = 0
    for file in files:
        file_id = int(get_fileid_from_filename(file))
        if highest_id < file_id:
            highest_id = file_id
    return highest_id


def get_fileid_from_filename(filename: str) -> str:
    """Extract fileid from a filename.

    Args:
        filename: A string filename in the format 'queue_time-started_agent_file-id.mp3'

    Returns:
        A fileid.
    """
    return filename.split("_")[-1].split(".")[0]


if __name__ == "__main__":
    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Miralix Nedhentning", conn_string, crypto_key, '{"target_queues":["89403330 Opkrævningen P-Gap","89403330 Opkrævningen P-Gap Boliglån tast 2", "89404130 BS - Kørekort P-GAP", "89402000 Aarhus Kommunes Hovednummer NPS", "89402088 Janni testnummer NPS", "89402260 BS - Vielseskontoret NPS"]}')
    download_from_queues(oc)
