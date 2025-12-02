import streamlit as st
from Utils.Auth import check_password
from Utils.OAuth import login_google
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
st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")
