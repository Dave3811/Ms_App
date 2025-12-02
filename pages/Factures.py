import streamlit as st

from Utils.Database import (
    get_factures,
    delete_estimation,
    init_db
)
from Utils.html_invoice import generate_invoice_html
from Utils.Auth import check_password


# ---------- AUTH ----------
if not check_password():
    st.stop()

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

if st.sidebar.button("🚪 Déconnexion"):
    st.session_state["auth_ok"] = False
    st.session_state["username"] = None
    st.rerun()

init_db()

st.title("🧾 Factures")

factures = get_factures()

if not factures:
    st.info("Aucune facture.")
    st.stop()


def safe(row, key, default=""):
    try:
        val = row[key]
        return default if val is None else val
    except:
        return default


for f in factures:

    estimate_id = safe(f, "id")
    invoice = safe(f, "facture_numero")
    client = safe(f, "client")
    adresse = safe(f, "adresse")
    date = safe(f, "date")
    desc = safe(f, "description")
    service = safe(f, "service")
    montant = safe(f, "montant", 0)
    taxes = safe(f, "taxes", 0)
    total = safe(f, "total", 0)

    header = f"{invoice} — {client} — {date}"

    with st.expander(header):

        st.write(f"Client : {client}")
        st.write(f"Adresse : {adresse}")
        st.write(f"Service : {service}")

        if desc:
            st.write(f"Description : {desc}")

        st.write(f"Montant : {montant} $")

        if taxes:
            st.write(f"Taxes / Extras : {taxes} $")

        st.write(f"Total : {total} $")

        # ---------- TÉLÉCHARGEMENT HTML ----------
        replacements = {
            "facture_numero": invoice,
            "client": client,
            "adresse": adresse,
            "service": service,
            "description": desc,
            "montant": montant,
            "extras": taxes,
            "total": total,
            "date": date,

            # INFOS ENTREPRISE (déjà dans ton template côté HTML)
            "logo_path": "assets/logo.png",
            "entreprise_nom": "M&S Déneigement & Gazon",
        }

        html_file = generate_invoice_html(
            "Utils/templates/factures.html",
            replacements
        )

        col_pdf, col_del = st.columns(2)

        with col_pdf:
            with open(html_file, "rb") as file:
                st.download_button(
                    label="📥 Télécharger la facture",
                    data=file,
                    file_name=f"{invoice}.html",
                    mime="text/html",
                )

        # ---------- SUPPRESSION ----------
        with col_del:
            confirm = st.checkbox(
                "⚠️ Confirmer suppression",
                key=f"conf_del_{estimate_id}"
            )

            if confirm and st.button(
                "🗑️ Supprimer la facture",
                key=f"del_{estimate_id}"
            ):
                delete_estimation(estimate_id)
                st.success("Facture supprimée.")
                st.rerun()
