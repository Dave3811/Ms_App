import streamlit as st
import datetime

from Utils.Auth import check_password
from Utils.Sheets import get_estimations, add_facture
from Utils.Pdf import generate_facture_pdf
from Utils.Drive import upload_pdf_to_drive

if not check_password():
    st.stop()

st.title("🧾 Factures")

estimations = get_estimations()

menu = {
    f"{e['numero']} — {e['client']} — {e['total']}$": e
    for e in estimations
}

choix = st.selectbox("Sélectionner une estimation :", menu.keys())

estimation = menu[choix]

st.write("### Aperçu estimation")
st.write(estimation)

if st.button("🧾 Convertir en facture"):

    date_facture = datetime.date.today()
    date_echeance = date_facture + datetime.timedelta(days=30)

    facture_numero = f"FAC-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    estimation["facture_numero"] = facture_numero
    estimation["statut"] = "ENVOYÉE"
    estimation["date_facture"] = str(date_facture)
    estimation["date_echeance"] = str(date_echeance)

    pdf = generate_facture_pdf(estimation)

    link = upload_pdf_to_drive(pdf, f"{facture_numero}.pdf")

    add_facture(estimation)

    st.success("✅ Facture générée")
    st.markdown(f"🔗 [Ouvrir la facture]({link})")
