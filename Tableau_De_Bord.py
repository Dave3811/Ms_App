import streamlit as st
from google_auth_oauthlib.flow import Flow

from Utils.Auth import check_password
from Utils.OAuth import SCOPES

# ---------------- OAuth Callback Handler ----------------

SCOPES = ["https://www.googleapis.com/auth/drive"]


def handle_oauth_callback():
    params = st.experimental_get_query_params()

    if "code" not in params:
        return False

    code = params["code"][0]

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": st.secrets["OAUTH"]["CLIENT_ID"],
                "client_secret": st.secrets["OAUTH"]["CLIENT_SECRET"],
                "redirect_uris": [st.secrets["OAUTH"]["REDIRECT_URI"]],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        redirect_uri=st.secrets["OAUTH"]["REDIRECT_URI"],
        scopes=SCOPES
    )

    flow.fetch_token(code=code)

    creds = flow.credentials

    st.session_state["google_creds"] = creds

    # Nettoyage de l'URL
    st.experimental_set_query_params()

    return True

# --------------------------------------------------------


handle_oauth_callback()

st.set_page_config(
    page_title="M&S Déneigement et Gazon",
    page_icon="❄️",
    layout="centered"
)

# DEBUG optionnel
st.write("Secrets chargés :", st.secrets.keys())


# Authentification APP interne
if not check_password():
    st.stop()


# Interface principale

st.title("🏠 Tableau de bord M&S")
st.write("Bienvenue dans votre système d’estimations et de facturation.")

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

st.info("Utilise le menu de gauche pour naviguer.")
