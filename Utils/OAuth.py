import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_user_credentials():

    # --------------------------------------------------
    # 1) Si déjà connecté → retourner les credentials
    # --------------------------------------------------
    if st.session_state.get("user_creds"):
        return Credentials.from_authorized_user_info(
            st.session_state["user_creds"],
            SCOPES
        )

    # --------------------------------------------------
    # 2) Est-ce un retour OAuth ?
    # --------------------------------------------------
    params = st.experimental_get_query_params()

    if "code" in params and "state" in params:

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

        try:
            flow.fetch_token(code=params["code"][0])

        except Exception as e:
            st.error("Erreur OAuth : impossible d'obtenir le token.")
            st.exception(e)
            st.stop()

        creds = flow.credentials

        # Sauvegarde en session
        st.session_state["user_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

        # Nettoyage de l'URL
        st.experimental_set_query_params()

        return Credentials.from_authorized_user_info(
            st.session_state["user_creds"],
            SCOPES
        )

    # --------------------------------------------------
    # 3) Démarrer l'auth Google
    # --------------------------------------------------
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
        f"### 🔐 Connexion Google\n\n👉 [Se connecter à Google]({auth_url})"
    )

    st.stop()
