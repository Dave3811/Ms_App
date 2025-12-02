import streamlit as st
from google_auth_oauthlib.flow import Flow

from Utils.Auth import check_password

# ---------------- OAUTH ----------------

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
        scopes=SCOPES,
        redirect_uri=st.secrets["OAUTH"]["REDIRECT_URI"]
    )

    flow.fetch_token(code=code)

    st.session_state["google_creds"] = flow.credentials

    st.experimental_set_query_params()
    return True


# ---------- EXEC CALLBACK ----------

handle_oauth_callback()

# ------- FORCE LOGIN GOOGLE --------

if "google_creds" not in st.session_state:

    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={st.secrets['OAUTH']['CLIENT_ID']}"
        f"&redirect_uri={st.secrets['OAUTH']['REDIRECT_URI']}"
        f"&response_type=code"
        f"&scope=https://www.googleapis.com/auth/drive"
        f"&access_type=offline"
        f"&prompt=consent"
    )

    st.link_button("🔐 Se connecter à Google", auth_url)
    st.stop()

# ----------------------------------------------------------------


# ---------- PAGE CONFIG ----------

st.set_page_config(
    page_title="M&S Déneigement et Gazon",
    page_icon="❄️",
    layout="centered"
)

# ---------- AUTH APP INTERNE ----------

if not check_password():
    st.stop()

# ---------- INTERFACE ----------

st.title("🏠 Tableau de bord M&S")
st.write("Bienvenue dans votre système d’estimations et de facturation.")

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

st.success("✅ Google Drive connecté")

st.info("Utilise le menu de gauche pour naviguer.")
