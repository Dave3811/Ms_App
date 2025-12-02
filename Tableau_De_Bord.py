import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from Utils.Auth import check_password

# =================== CONFIG ===================

st.set_page_config(
    page_title="M&S Déneigement et Gazon",
    page_icon="❄️",
    layout="centered"
)

SCOPES = ["https://www.googleapis.com/auth/drive"]

# =================== OAUTH ===================


def handle_oauth():

    # Déjà connecté ?
    if "google_creds" in st.session_state:
        return True

    params = st.experimental_get_query_params()

    # --------- CALLBACK GOOGLE ---------
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

        # Échange du code contre un token
        flow.fetch_token(code=params["code"][0])

        creds = flow.credentials

        # Sauvegarde du token en session
        st.session_state["google_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

        # Nettoyer l'URL
        st.experimental_set_query_params()

        # Recharge propre
        st.rerun()

    # --------- PREMIÈRE CONNEXION ---------

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
        access_type="offline",
        prompt="consent"
    )

    st.link_button("🔐 Se connecter à Google", auth_url)
    st.stop()

# ================= EXEC OAUTH =================


handle_oauth()

# ========= AUTH INTERNE APP =========

if not check_password():
    st.stop()

# ================= INTERFACE =================

st.title("🏠 Tableau de bord M&S")
st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

st.success("✅ Google Drive connecté")

st.info("Utilise le menu de gauche pour naviguer.")
