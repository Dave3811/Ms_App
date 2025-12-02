import streamlit as st
from google_auth_oauthlib.flow import Flow
import traceback

SCOPES = ["https://www.googleapis.com/auth/drive"]

def login_google():

    st.write("🔍 DÉBUT login_google")

    try:
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

        st.write("✅ Flow créé")

        # Générer l'URL OAuth
        auth_url, _ = flow.authorization_url(
            prompt="consent",
            include_granted_scopes="true",
        )

        st.write("🔗 URL AUTH :", auth_url)

        # Lire les paramètres
        qp = st.query_params
        st.write("📨 QUERY PARAMS :", qp)

        code = qp.get("code")

        st.write("🔑 CODE :", code)

        # Traitement du callback
        if code:
            st.write("🚀 fetch_token lancé...")

            flow.fetch_token(code=code)

            st.session_state["google_creds"] = flow.credentials

            st.write("✅ TOKEN OBTENU !")
            st.write("TOKEN INFO :", st.session_state["google_creds"].to_json())

            st.query_params.clear()
            st.rerun()

        st.link_button("👉 Se connecter à Google", auth_url)

    except Exception as e:
        st.error("🔥 ERREUR OAUTH")
        st.error(str(e))
        st.code(traceback.format_exc())