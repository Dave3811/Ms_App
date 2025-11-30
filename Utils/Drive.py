import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_drive_service():
    creds = None

    # Reuse credentials if already stored
    if "google_credentials" in st.session_state:
        creds = Credentials.from_authorized_user_info(
            st.session_state["google_credentials"], SCOPES
        )

    if not creds:
        # ✅ Secrets already parsed as dict
        oauth_config = st.secrets["OAUTH_CLIENT_SECRET"]

        flow = InstalledAppFlow.from_client_config(
            oauth_config,
            SCOPES
        )

        creds = flow.run_console()

        st.session_state["google_credentials"] = oauth_config = st.session_state["google_credentials"] = oauth_config = json.loads(
            creds.to_json())  # store serialized credentials

    return build("drive", "v3", credentials=creds)
