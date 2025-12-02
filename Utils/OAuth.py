import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_user_credentials():
    """
    Gère TOUT le cycle OAuth Google pour Streamlit Cloud :
      - Restaure la session existante
      - Intercepte la callback (?code=...)
      - Échange le code contre un token
      - Démarre l'auth si nécessaire

    Retourne un objet Credentials valide ou bloque l'app.
    """

    # --------------------------------------------------
    # 1) SI SESSION EXISTANTE
    # --------------------------------------------------
    if "user_creds" in st.session_state:
        return Credentials.from_authorized_user_info(
            st.session_state["user_creds"],
            SCOPES
        )

    # --------------------------------------------------
    # 2) CALLBACK GOOGLE
    # --------------------------------------------------
    params = st.query_params

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
            redirect_uri=st.secrets["OAUTH"]["REDIRECT_URI"],
            state=st.session_state.get("oauth_state")
        )

        try:
            flow.fetch_token(code=params["code"])

        except Exception as e:
            st.error("❌ Erreur OAuth : impossible d'obtenir le token")
            st.exception(e)
            st.stop()

        creds = flow.credentials

        # --------------------------------------------------
        # SAUVEGARDE SESSION
        # --------------------------------------------------
        st.session_state["user_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": list(creds.scopes) if creds.scopes else [],
        }

        # Nettoyage de l’URL
        st.query_params.clear()
        st.rerun()

    # --------------------------------------------------
    # 3) PREMIÈRE CONNEXION
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
        access_type="offline",
        include_granted_scopes="true"
    )

    st.session_state["oauth_state"] = state

    st.link_button("🔐 Se connecter à Google", auth_url)
    st.stop()