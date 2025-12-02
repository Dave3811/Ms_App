import streamlit as st
from Utils.Auth import check_password
from Utils.Drive import create_empty_file

# =================== CONFIG ===================

st.set_page_config(
    page_title="M&S Déneigement et Gazon",
    page_icon="❄️",
    layout="centered"
)

# ========= AUTH INTERNE APP =========

if not check_password():
    st.stop()

# ================= INTERFACE =================

st.title("🏠 Tableau de bord M&S")

if st.button("🧪 TEST Drive"):
    link = create_empty_file("TEST_M_S.txt")
    st.success("✅ Fichier créé avec succès")
    st.write("Lien :", link)

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

st.success("✅ Connexion M&S active")
st.info("Les fichiers seront sauvegardés automatiquement dans le Drive M&S.")
