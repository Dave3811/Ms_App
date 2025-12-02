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
    """
    Gère tout le cycle OAuth :
    - Première connexion : affiche le bouton Google
    - Retour de Google (?code=...) : échange le code contre un token
    - Si déjà connecté : retourne directement les credentials
    """

    # Déjà connecté
    if "google_creds" in st.session_state:
        return Credentials.from_authorized_user_info(
            st.session_state["google_creds"],
            SCOPES
        )

    params = st.query_params

    # --------- RETOUR DE GOOGLE ---------
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
            st.error("❌ Erreur pendant la validation OAuth (fetch_token).")
            st.write("Message technique :", str(e))
            st.stop()

        creds = flow.credentials

        # Sauvegarde du token en session
        st.session_state["google_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": list(creds.scopes) if creds.scopes else [],
        }

        # Nettoyage de l'URL
        st.query_params.clear()

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

    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true"
    )

    st.session_state["oauth_state"] = state

    st.link_button("🔐 Se connecter à Google", auth_url)
    st.stop()

# ================= EXEC OAUTH =================


creds = handle_oauth()

# ========= AUTH INTERNE APP =========

if not check_password():
    st.stop()

# ================= INTERFACE =================

st.title("🏠 Tableau de bord M&S")
st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

if creds:
    st.success("✅ Google Drive connecté")
else:
    st.warning("⚠️ Problème de connexion Google Drive")

st.info("Utilise le menu de gauche pour naviguer.")
