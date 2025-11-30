import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=creds)


def upload_html_to_drive(html: str, filename: str, folder_id: str):
    service = get_drive_service()

    file_metadata = {
        "name": filename,
        "parents": [folder_id],
        "mimeType": "text/html"
    }

    media = MediaIoBaseUpload(
        BytesIO(html.encode("utf-8")),
        mimetype="text/html",
        resumable=False
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()

    return file["webViewLink"]
