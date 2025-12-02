import streamlit as st

from Utils.Database import (
    get_estimations,
    update_status,
    delete_estimation,
    init_db
)
from Utils.Auth import check_password


if not check_password():
    st.stop()

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

if st.sidebar.button("🚪 Déconnexion"):
    st.session_state["auth_ok"] = False
    st.session_state["username"] = None
    st.rerun()
init_db()

st.title("📊 Tableau de bord")

sections = {
    "🕒 En attente": "PENDING",
    "✅ Acceptées (factures)": "APPROVED",
    "❌ Refusées": "REJECTED"
}


def safe(row, key, default=""):
    try:
        val = row[key]
        return default if val is None else val
    except:
        return default


for title, status in sections.items():

    st.subheader(title)
    rows = get_estimations(status)

    if not rows:
        st.info("Aucune entrée")
        continue

    for e in rows:

        estimate_id = safe(e, "id")
        facture_num = safe(e, "facture_numero")
        numero = safe(e, "numero")
        client = safe(e, "client")
        date = safe(e, "date")
        desc = safe(e, "description")
        service = safe(e, "service")
        montant = safe(e, "montant", 0)
        taxes = safe(e, "taxes", 0)
        total = safe(e, "total", 0)

        header = f"#{numero} — {client} — {date}"

        with st.expander(header):

            st.write(f"Client : {client}")
            st.write(f"Service : {service}")

            if desc:
                st.write(f"Description : {desc}")

            if facture_num:
                st.success(f"Facture #: {facture_num}")

            st.write(f"Montant : {montant} $")

            if taxes:
                st.write(f"Taxes / Extras : {taxes} $")

            st.write(f"Total : {total} $")

            '''TODO Si le client se désiste ou s'il change d'idéé être capable
            de changer l'estimations de refusée à acceptée ou l'inverse'''
            if status == "PENDING":

                col1, col2 = st.columns(2)

                if col1.button("✅ Accepter", key=f"ok_{estimate_id}"):
                    update_status(estimate_id, "APPROVED")
                    st.success("Facture créée")
                    st.rerun()

                if col2.button("❌ Refuser", key=f"no_{estimate_id}"):
                    update_status(estimate_id, "REJECTED")
                    st.rerun()

            elif status == "APPROVED":

                confirm = st.checkbox(
                    "⚠️ Supprimer cette facture",
                    key=f"conf_{estimate_id}"
                )

                if confirm and st.button("🗑️ Supprimer", key=f"del_{estimate_id}"):
                    delete_estimation(estimate_id)
                    st.rerun()

            elif status == "REJECTED":

                confirm = st.checkbox(
                    "Confirmer suppression",
                    key=f"conf_{estimate_id}"
                )

                if confirm and st.button("🗑️ Supprimer", key=f"del_{estimate_id}"):
                    delete_estimation(estimate_id)
                    st.rerun()
