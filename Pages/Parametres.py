import streamlit as st

from Utils.Auth import check_password

if not check_password():
    st.stop()

# Affichage de la connexion
st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")
st.title("Gestion des paramètres")
