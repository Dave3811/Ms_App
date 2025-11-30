import json
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_drive_service():
    creds = None

    # Reuse session credentials if already logged in
    if "google_credentials" in st.session_state:
        creds = Credentials.from_authorized_user_info(
            st.session_state["google_credentials"],
            SCOPES
        )

    # First login
    if not creds:
        # ✅ Convert secrets TEXT -> DICT
        oauth_config = json.loads(st.secrets["OAUTH_CLIENT_SECRET"])

        flow = InstalledAppFlow.from_client_config(
            oauth_config,
            SCOPES
        )

        # For Streamlit Cloud, interactive login in console works
        creds = flow.run_console()

        # Store creds for later reuse
        st.session_state["google_credentials"] = json.loads(creds.to_json())

    return build("drive", "v3", credentials=creds)


def upload_pdf_to_drive(pdf_bytes: bytes, filename: str, folder_id=None):
    service = get_drive_service()

    metadata = {"name": filename}
    if folder_id:
        metadata["parents"] = [folder_id]

    media = MediaIoBaseUpload(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        resumable=False
    )

    file = service.files().create(
        body=metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()

    return file["webViewLink"]
