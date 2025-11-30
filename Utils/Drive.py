from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import streamlit as st

from Utils.OAuth import get_user_credentials


def upload_html_user_drive(html: str, filename: str):

    # Récupérer les credentials OAuth de l'utilisateur connecté
    creds = get_user_credentials()

    # Créer le service Google Drive
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": filename,
        "parents": [st.secrets["DRIVE"]["FOLDER_ID"]],
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
