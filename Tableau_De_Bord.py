import streamlit as st
from Utils.Auth import check_password


st.set_page_config(
    page_title="M&S Déneigement et Gazon",
    page_icon="❄️",
    layout="centered"
)

st.write("Secret loaded : ", st.secrets.keys())
# Authentification
if not check_password():
    st.stop()


# Interface

st.set_page_config(page_title="Tableau de bord")
st.title("🏠 Tableau de bord M&S")
st.write("Bienvenue dans votre système d’estimations et factures.")


# Affichage de la connexion
st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

st.info("Utilise le menu de gauche pour naviguer.")
