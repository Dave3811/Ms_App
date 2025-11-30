import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_drive_service():
    creds = None

    if "google_credentials" in st.session_state:
        creds = Credentials.from_authorized_user_info(
            st.session_state["google_credentials"],
            SCOPES
        )

    if not creds:
        flow = InstalledAppFlow.from_client_config(
            st.secrets[["OAUTH"]["OAUTH_CLIENT_SECRET"]],
            SCOPES
        )
        creds = flow.run_console()

        st.session_state["google_credentials"] = json.loads(creds.to_json())

    return build("drive", "v3", credentials=creds)


def upload_pdf_to_drive(pdf_bytes: bytes, filename: str, folder_id=None):
    service = get_drive_service()

    file_metadata = {"name": filename}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    from googleapiclient.http import MediaIoBaseUpload
    from io import BytesIO

    media = MediaIoBaseUpload(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        resumable=False,
    )

    file = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink"
        )
        .execute()
    )

    return file["webViewLink"]
