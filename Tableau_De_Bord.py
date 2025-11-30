import streamlit as st
from google_auth_oauthlib.flow import Flow

from Utils.Auth import check_password
from Utils.OAuth import SCOPES

# ---------------- OAuth Callback Handler ----------------

if "code" in st.query_params:

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
        state=st.session_state.get("oauth_state"),
        redirect_uri=st.secrets["OAUTH"]["REDIRECT_URI"],
    )

    flow.fetch_token(code=st.query_params["code"])

    st.session_state["user_creds"] = flow.credentials.to_authorized_user_info()

    st.experimental_set_query_params()
    st.rerun()

# --------------------------------------------------------


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
