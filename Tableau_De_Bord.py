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


def safe(row, key, default=""):
    """
    Retourne une valeur sécurisée :
    - '' si None ou champ manquant
    - default si inexistant
    """
    try:
        value = row[key]
        if value is None:
            return default
        return value
    except Exception:
        return default


for name, status in sections.items():

    st.subheader(name)
    data = get_estimations(status)

    if not data:
        st.info("Aucune estimation.")
        continue

    for e in data:

        # ---------- RÉCUP CHAMPS ----------
        estimate_id = safe(e, "id")
        numero = safe(e, "numero")
        client = safe(e, "client")
        adresse = safe(e, "adresse")
        service = safe(e, "service")
        description = safe(e, "description")
        montant = safe(e, "montant", 0)
        extras = safe(e, "extras", 0)
        total = safe(e, "total", 0)
        date_estimation = safe(e, "date")

        # ---------- HEADER ----------
        # On affiche MAINTENANT la date au lieu du total
        header = f"#{numero} — {client} — {date_estimation}"

        with st.expander(header):

            # ---------- INFOS ----------
            if client:
                st.write(f"Client : {client}")

            if adresse:
                st.write(f"Adresse : {adresse}")

            if service:
                st.write(f"Service : {service}")

            if description:
                st.write(f"Description : {description}")

            if date_estimation:
                st.write(f"Date : {date_estimation}")

            st.write(f"Montant : {montant} $")

            if extras:
                st.write(f"Extras : {extras} $")

            st.write(f"Total : {total} $")

            # ---------- ACTIONS ----------
            if status == "PENDING":

                col1, col2 = st.columns(2)

                if col1.button(
                    "✅ Accepter",
                    key=f"ok_{estimate_id}"
                ):
                    update_status(estimate_id, "APPROVED")
                    st.rerun()

                if col2.button(
                    "❌ Refuser",
                    key=f"no_{estimate_id}"
                ):
                    update_status(estimate_id, "REJECTED")
                    st.rerun()
