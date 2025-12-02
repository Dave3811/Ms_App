from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/drive"]


def upload_html_to_drive(html: str, filename: str):

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": filename,
        "parents": [st.secrets["DRIVE"]["FOLDER_ID"]],
        "mimeType": "text/html",
    }

    media = MediaIoBaseUpload(
        BytesIO(html.encode("utf-8")),
        mimetype="text/html",
        resumable=False,
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,webViewLink"
    ).execute()

    return file["webViewLink"]
