import streamlit as st
from Utils.Auth import check_password

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

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

st.success("✅ Connexion M&S active")
st.info("Les fichiers seront sauvegardés automatiquement dans le Drive M&S.")
