import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_user_credentials():

    if "user_creds" in st.session_state:
        return Credentials.from_authorized_user_info(
            st.session_state["user_creds"], SCOPES
        )

    params = st.query_params

    # CALLBACK GOOGLE
    if "code" in params:

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

        flow.fetch_token(code=params["code"])

        creds = flow.credentials

        st.session_state["user_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": list(creds.scopes),
        }

        st.query_params.clear()
        st.rerun()

    # PREMIÈRE CONNEXION
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

    auth_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline"
    )

    st.link_button("🔐 Se connecter à Google", auth_url)
    st.stop()
