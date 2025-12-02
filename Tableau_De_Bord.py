import streamlit as st

from Utils.Database import (
    get_estimations,
    update_status,
    init_db
)
from Utils.Auth import check_password

# ---------- AUTH ----------
if not check_password():
    st.stop()

init_db()

st.title("📊 Tableau de bord")

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

sections = {
    "🕒 En attente": "PENDING",
    "✅ Acceptées": "APPROVED",
    "❌ Refusées": "REJECTED"
}

for name, status in sections.items():

    st.subheader(name)

    data = get_estimations(status)

    if not data:
        st.info("Aucune estimation.")
        continue

    for e in data:

        with st.expander(f"#{e[1]} — {e[3]} — {e[17]} $"):

            st.write(f"Client : {e[3]}")
            st.write(f"Adresse : {e[4]}")
            st.write(f"Service : {e[7]}")
            st.write(f"Description : {e[9]}")
            st.write(f"Montant : {e[10]} $")
            st.write(f"Extras : {e[11] or ''} / {e[12] or ''}")
            st.write(f"Total : {e[17]} $")

            if status == "PENDING":

                col1, col2 = st.columns(2)

                if col1.button("✅ Accepter", key=f"ok_{e[0]}"):
                    update_status(e[0], "APPROVED")
                    st.rerun()

                if col2.button("❌ Refuser", key=f"no_{e[0]}"):
                    update_status(e[0], "REJECTED")
                    st.rerun()
