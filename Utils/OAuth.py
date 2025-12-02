import streamlit as st
from google_auth_oauthlib.flow import Flow

SCOPES = ["https://www.googleapis.com/auth/drive"]


def login_google():

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
        redirect_uri=st.secrets["OAUTH"]["REDIRECT_URI"],
    )

    # Récupération PROPRE des paramètres
    code = st.query_params.get("code")

    # ---------- CALLBACK ----------
    if code:
        flow.fetch_token(code=code)
        st.session_state["google_creds"] = flow.credentials

        # Nettoyage de l'URL
        st.query_params.clear()

        st.rerun()

    # ---------- LOGIN ----------
    auth_url, _ = flow.authorization_url(
        prompt="consent",
        include_granted_scopes=True,
    )

    st.link_button("👉 Se connecter à Google", auth_url)
