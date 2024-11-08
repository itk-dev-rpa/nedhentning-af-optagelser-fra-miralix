"""Functions for accessing the Miralix API."""

import json

from requests import Session
from requests_ntlm import HttpNtlmAuth
from robot_framework import config


def create_session(apiurl: str, username: str, password: str) -> Session:
    """Create a session for accessing GetOrganized API.

    Args:
        apiurl: URL for the API.
        username: Username for login.
        password: Password for login.

    Returns:
        Return the session object
    """
    session = Session()
    session.headers.setdefault("Content-Type", "application/json")
    session.auth = HttpNtlmAuth(username, password)
    session.post(apiurl, timeout=config.GO_TIMEOUT)
    return session


def upload_document(*, apiurl: str, session: Session, file: bytearray, case: str, filename: str, agent_name: str | None = None, date_string: str | None = None) -> tuple[str, Session]:
    """Upload a document to Get Organized.

    Args:
        apiurl: Base url for API.
        session: Session token for request.
        file: Bytearray of file to upload.
        case: Case name already present in GO.
        filename: Name of file when saved in GO.
        agent_name: Agent name, used for creating a folder in GO. Defaults to None.
        date_string: A date to add as metadata to GetOrganized. Defaults to None.

    Returns:
        Return response text and session token.
    """
    url = apiurl + "/_goapi/Documents/AddToCase"
    payload = {
        "Bytes": file,
        "CaseId": case,
        "SiteUrl": f"{apiurl}/cases/EMN/{case}",
        "ListName": "Dokumenter",
        "FolderPath": agent_name,
        "FileName": filename,
        "Metadata": f"<z:row xmlns:z='#RowsetSchema' ows_Dato='{date_string}'/>",
        "Overwrite": True
    }
    response = session.post(url, data=json.dumps(payload), timeout=config.GO_TIMEOUT)
    return response.text, session


def delete_document(apiurl, session, document_id) -> tuple[str, Session]:
    """Delete a document from GetOrganized.

    Args:
        apiurl: Url of the GetOrganized API.
        session: Session object used for logging in.
        document_id: ID of the document to delete.

    Returns:
        Return the response and session objects
    """
    url = apiurl + "/_goapi/Documents/ByDocumentId"
    payload = {
        "DocId": document_id
    }
    response = session.delete(url, data=json.dumps(payload), timeout=config.GO_TIMEOUT)
    return response.text, session


def create_case(apiurl: str, session: str, title: str) -> tuple[str, Session]:
    """Create a case in GetOrganized.

    Args:
        apiurl: Url for the GetOrganized API.
        session: Session object to access API.
        title: Title of the case being created.

    Returns:
        Return the response and session objects.
    """
    url = apiurl + "/_goapi/Cases/"
    payload = {
        'CaseTypePrefix': 'EMN',
        'MetadataXml': f'<z:row xmlns:z="#RowsetSchema" ows_Title="{title}" ows_CaseStatus="Åben"/>',
        'ReturnWhenCaseFullyCreated': False
        }
    # Send the POST request
    response = session.post(url, data=json.dumps(payload), timeout=config.GO_TIMEOUT)
    # Return the response
    return response.text, session


def close_case(apiurl, session, case_number) -> tuple[str, Session]:
    """Close a case in GetOrganized.

    Args:
        apiurl: Url for the GetOrganized API.
        session: Session object to access API.
        case_number: Case number of case to be closed.

    Returns:
        Return the response and session objects.
    """
    url = apiurl + "/_goapi/Cases/CloseCase"
    payload = {"CaseId": case_number}
    response = session.post(url, data=payload, timeout=config.GO_TIMEOUT)
    return response.text, session


def journalize_document(apiurl, doc_id, session) -> tuple[str, Session]:
    """Journalize a document in GetOrganized.

    Args:
        apiurl: URL for GetOrganized API.
        doc_id: ID of document to journalize.
        session: Session token for connection.

    Returns:
        Response text and updated session token.
    """
    url = apiurl + "/_goapi/Documents/Finalize/ByDocumentId"
    payload = {"DocID": doc_id}
    response = session.post(url, data=payload, timeout=config.GO_TIMEOUT)
    return response.text, session


def unjournalize_documents(apiurl, doc_ids, session) -> tuple[str, Session]:
    """Unjournalize a document in GetOrganized.

    Args:
        apiurl: URL for GetOrganized API.
        doc_id: ID of document to journalize.
        session: Session token for connection.

    Returns:
        Response text and updated session token.
    """
    url = apiurl + "/_goapi/Documents/UnmarkFinalizedByDocumentId"
    payload = {
        "DocIDs": doc_ids,
        "OnlyUnfinalize": True
    }
    response = session.post(url, data=payload)
    return response.text, session


def log_to_getorganized(apiurl: str, session: Session, message: str) -> tuple[str, Session]:
    """Log a message to GetOrganized.

    Args:
        apiurl: URL of API to GetOrganized.
        session: Session token for connection.
        message: Message to log.

    Returns:
        Response text and updated session token.
    """
    url = apiurl + "/_goapi/administration/Log"
    data = {
        "FullClassName": "GO API CLASS NAME FULL",
        "FunctionName": "LogFromGoApi",
        "OperationName": "OperationNameFromGoApi",
        "Message": message,
        "LogLevel": "1"
    }
    response = session.post(url, json.dumps(data))
    return response, session


if __name__ == "__main__":
    print("main")
