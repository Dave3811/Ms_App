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

# ========= AUTH GOOGLE =========

if "google_creds" not in st.session_state:
    login_google()
    st.stop()

# ================= INTERFACE =================

st.title("🏠 Tableau de bord M&S")
st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

st.success("✅ Connexion Google établie")

# ================= TEST DRIVE =================

st.title("🧪 Test création fichier")

if st.button("Créer fichier vide"):
    link = create_empty_file("TEST_M_S.txt")

    st.success("✅ Fichier vide créé dans le dossier MS")
    st.markdown(f"🔗 [Ouvrir le fichier]({link})")

st.info("Les fichiers seront sauvegardés automatiquement dans le Drive M&S.")
