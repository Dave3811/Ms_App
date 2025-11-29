import streamlit as st


def check_password():

    users = st.secrets["users"]

    # ✅ si déjà connecté → OK direct
    if st.session_state.get("auth_ok"):
        return True

    st.subheader("Connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username in users and users[username] == password:
            st.session_state["auth_ok"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

    return False
