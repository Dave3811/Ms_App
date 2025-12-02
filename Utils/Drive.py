import streamlit as st
from io import BytesIO
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():

    if "user_creds" not in st.session_state:
        raise Exception("Aucune session Google active")

    creds = Credentials.from_authorized_user_info(
        st.session_state["user_creds"], SCOPES
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

    file = service.files().create(
        body=file_metadata,
        fields="id, webViewLink",
    ).execute()

    return file["webViewLink"]
