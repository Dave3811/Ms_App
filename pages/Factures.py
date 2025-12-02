import streamlit as st

from Utils.Database import get_factures, init_db
from Utils.Auth import check_password


# ---------- AUTH ----------
if not check_password():
    st.stop()

init_db()

st.title("🧾 Factures")

factures = get_factures()

if not factures:
    st.info("Aucune facture enregistrée.")
    st.stop()


def safe(row, key, default=""):
    try:
        val = row[key]
        return default if val is None else val
    except:
        return default


for f in factures:

    invoice = safe(f, "facture_numero")
    client = safe(f, "client")
    date = safe(f, "date")
    desc = safe(f, "description")
    service = safe(f, "service")
    montant = safe(f, "montant", 0)
    extras = safe(f, "taxes", 0)
    total = safe(f, "total", 0)

    header = f"{invoice} — {client} — {date}"

    with st.expander(header):

        st.write(f"Client : {client}")

        if desc:
            st.write(f"Description : {desc}")

        st.write(f"Service : {service}")
        st.write(f"Montant : {montant} $")

        if extras:
            st.write(f"Taxes/Extras : {extras} $")

        st.write(f"Total : {total} $")
