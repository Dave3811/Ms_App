import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=creds)


def create_empty_file(filename: str):

    service = get_drive_service()
    folder_id = st.secrets["DRIVE"]["FOLDER_ID"]

    file_metadata = {
        "name": filename,
        "parents": [folder_id],
        "mimeType": "text/plain",
    }

    try:
        file = service.files().create(
            body=file_metadata,
            fields="id, webViewLink"
        ).execute()
    except Exception as e:
        raise Exception(f"❌ ERREUR Drive test : {e}")

    return file["webViewLink"]
