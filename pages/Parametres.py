import streamlit as st

from Utils.Auth import check_password

if not check_password():
    st.stop()

# Affichage de la connexion
st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

if st.sidebar.button("🚪 Déconnexion"):
    st.session_state["auth_ok"] = False
    st.session_state["username"] = None
    st.rerun()
st.title("Gestion des paramètres")
st.color_picker("Color")
