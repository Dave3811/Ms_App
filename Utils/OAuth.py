import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_user_credentials():

    if st.session_state.get("user_creds"):
        return Credentials.from_authorized_user_info(
            st.session_state["user_creds"],
            SCOPES
        )

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": st.secrets["OAUTH"]["CLIENT_ID"],
                "client_secret": st.secrets["OAUTH"]["CLIENT_SECRET"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [st.secrets["OAUTH"]["REDIRECT_URI"]],
            }
        },
        scopes=SCOPES,
        redirect_uri=st.secrets["OAUTH"]["REDIRECT_URI"]
    )

    auth_url, state = flow.authorization_url(
        prompt="consent",
        access_type="offline"
    )

    st.session_state["oauth_state"] = state

    st.markdown(
        f"### 🔐 Connexion Google\n\n👉 [Se connecter à Google]({auth_url})")
    st.stop()
