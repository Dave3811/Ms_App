import streamlit as st

from Utils.Database import get_factures, init_db
from Utils.html_invoice import generate_invoice_html
from Utils.Auth import check_password
from pathlib import Path
st.write("CWD:", Path.cwd())
st.write("Contenu de templates/ :", list(Path("templates").glob("*")))


# ---------- AUTH ----------
if not check_password():
    st.stop()

init_db()

st.title("🧾 Factures")

factures = get_factures()

if not factures:
    st.info("Aucune facture générée.")
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
    adresse = safe(f, "adresse")
    date = safe(f, "date")
    desc = safe(f, "description")
    service = safe(f, "service")
    montant = safe(f, "montant", 0)
    extras = safe(f, "taxes", 0)
    total = safe(f, "total", 0)

    header = f"{invoice} — {client} — {date}"

    with st.expander(header):

        st.write(f"Client : {client}")
        st.write(f"Adresse : {adresse}")
        st.write(f"Service : {service}")

        if desc:
            st.write(f"Description : {desc}")

        st.write(f"Montant : {montant} $")

        if extras:
            st.write(f"Taxes / Extras : {extras} $")

        st.write(f"Total : {total} $")

        # ---------- GÉNÉRATION HTML ----------
        replacements = {
            "facture_numero": invoice,
            "client": client,
            "adresse": adresse,
            "service": service,
            "description": desc,
            "montant": montant,
            "extras": extras,
            "total": total,
            "date": date,

            # ENTREPRISE
            "logo_path": "assets/logo.png",
            "entreprise_nom": "M&S Déneigement & Gazon",
            "entreprise_adresse": "Ton adresse ici",
            "entreprise_tel": "418-xxx-xxxx",
            "entreprise_email": "contact@msgazon.com"
        }

        html_file = generate_invoice_html(
            "templates/factures.html",
            replacements
        )

        with open(html_file, "rb") as file:
            st.download_button(
                label="📥 Télécharger la facture",
                data=file,
                file_name=f"{invoice}.html",
                mime="text/html"
            )
