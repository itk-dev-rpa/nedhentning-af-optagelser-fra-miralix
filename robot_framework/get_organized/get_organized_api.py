"""Functions for accessing the Miralix API."""

from requests import Session
import json
import os
from requests_ntlm import HttpNtlmAuth


def create_session(APIURL: str, username: str, password: str) -> Session:
    """Create a session for accessing API.

    Args:
        APIURL: URL for the API.
        username: Username for login.
        password: Password for login.

    Returns:
        Return the session object
    """
    session = Session()
    session.headers.setdefault("Content-Type", "application/json")
    session.auth = HttpNtlmAuth(username, password)
    session.post(APIURL, timeout=60)
    return session


def create_case(APIURL: str, session: str, title: str) -> tuple[str, Session]:
    """Create a case in GetOrganized.

    Args:
        APIURL: Url for the GetOrganized API.
        session: Session object to access API.
        title: Title of the case being created.

    Returns:
        Return the response and session objects.
    """
    url = APIURL + "/_goapi/Cases/"
    payload = {
        'CaseTypePrefix': 'EMN',
        'MetadataXml': f'<z:row xmlns:z="#RowsetSchema" ows_Title="{title}" ows_CaseStatus="Åben"/>',
        'ReturnWhenCaseFullyCreated': False
        }
    # Send the POST request
    response = session.post(url, data=json.dumps(payload), timeout=600)
    # Return the response
    return response.text, session


def close_case(APIURL, session, case_number) -> tuple[str, Session]:
    """Close the case in GetOrganized.

    Args:
        APIURL: Url for the GetOrganized API.
        session: Session object to access API.
        case_number: Case number of case to be closed.

    Returns:
        Return the response and session objects.
    """
    url = APIURL + "/_goapi/Cases/CloseCase"
    payload = {"CaseId": case_number}
    response = session.post(url, data=payload, timeout=600)
    return response.text, session


def upload_document(APIURL: str, session: Session, filepath: str, case: str) -> tuple[str, Session]:
    """Upload a document to GetOrganized.

    Args:
        APIURL: Url of the GetOrganized API.
        session: Session object for login.
        filepath: Filepath of the file to upload.
        case: WWhich case to add the file to.

    Returns:
        Return the response and session objects
    """
    url = APIURL + "/_goapi/Documents/AddToCase"
    payload = {
        "Bytes": file_to_bytes(filepath),
        "CaseId": case,
        "SiteUrl": f"{APIURL}/cases/EMN/{case}",
        "ListName": "Dokumenter",
        "FolderPath": None,
        "FileName": os.path.basename(filepath),
        "Metadata": "<z:row xmlns:z='#RowsetSchema' ows_CustomProperty='Another prop value' />",
        "Overwrite": False
        }
    response = session.post(url, data=json.dumps(payload), timeout=600)
    return response.text, session


def delete_document(APIURL, session, document_id) -> tuple[str, Session]:
    """Delete a document from GetOrganized.

    Args:
        APIURL: Url of the GetOrganized API.
        session: Session object used for logging in.
        document_id: ID of the document to delete.  

    Returns:
        Return the response and session objects
    """
    url = APIURL + "/_goapi/Documents/ByDocumentId"
    payload = {
        "DocId": document_id
        }
    response = session.delete(url, data=json.dumps(payload), timeout=600)
    return response.text, session


def journalize_documents(APIURL, DocID, session) -> tuple[str, Session]:
    url = APIURL + "/_goapi/Documents/Finalize/ByDocumentId"
    payload = {"DocID": DocID}
    response = session.post(url, data=payload, timeout=600)
    return response.text, session


def unjournalize_documents(APIURL, DocIDS, session) -> tuple[str, Session]:
    url = APIURL + "/_goapi/Documents/UnmarkFinalizedByDocumentId"
    payload = {"DocIDs": DocIDS,
               "OnlyUnfinalize": True
               }
    response = session.post(url, data=payload)
    return response.text, session


def log_to_getorganized(APIURL: str, session: Session, message: str) -> tuple[str, Session]:
    url = APIURL + "/_goapi/administration/Log"
    data = {
        "FullClassName": "GO API CLASS NAME FULL",
        "FunctionName": "LogFromGoApi",
        "OperationName": "OperationNameFromGoApi",
        "Message": message,
        "LogLevel": "1"
            }
    response = session.post(url, json.dumps(data))
    return response.text, session


def file_to_bytes(file_path) -> list[int]:
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    return list(file_bytes)
