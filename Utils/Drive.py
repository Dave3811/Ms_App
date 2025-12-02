import streamlit as st
from io import BytesIO

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


# Scope Drive complet (lecture + écriture)
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    """
    Crée un service Google Drive avec le SERVICE ACCOUNT (bot M&S)
    """

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    return build("drive", "v3", credentials=creds)


def upload_html_to_drive(html: str, filename: str):
    """
    Enregistre un fichier HTML dans le dossier M&S Déneigement
    Retourne le lien de visualisation Google Drive
    """

    service = get_drive_service()

    folder_id = st.secrets["DRIVE"]["FOLDER_ID"]

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
