import streamlit as st
import datetime

from Utils.Auth import check_password
from Utils.Sheets import add_estimation
from Utils.Pdf import generate_estimation_html
# ---------- AUTH ----------
if not check_password():
    st.stop()

st.sidebar.write(f"👤 Connecté : {st.session_state['username']}")

if st.sidebar.button("🚪 Déconnexion"):
    st.session_state["auth_ok"] = False
    st.session_state["username"] = None
    st.rerun()


# ---------- CONFIG ----------
TPS = 0.05
TVQ = 0.09975
TAUX_TOTAL = TPS + TVQ

FRAIS_DEPLACEMENT = 50.00


# ---------- UI ----------
st.title("📋 Création d'Estimation")
st.write("Remplis les informations pour créer l'estimation.")

with st.form("estimation_form"):

    nom_client = st.text_input("Nom du client")
    adresse_client = st.text_input("Adresse du client")
    numero_client = st.text_input("Téléphone")
    couriel_client = st.text_input("Courriel")

    service = st.selectbox("Type de service", [
        "Tonte de pelouse",
        "Déneigement",
        "Autre"
    ])

    superficie = st.number_input("Superficie totale", min_value=0, step=10)
    description = st.text_area("Description du travail")

    montant = st.number_input(
        "Montant principal ($)",
        min_value=superficie * 1.50,
        step=1.00
    )

    # Extras
    st.subheader("Extras")
    extra1 = st.checkbox("Taille de haie")
    extra2 = st.checkbox("Découpage")

    exdescription = st.text_area("Description des extras")

    extra_val = st.number_input(
        "Montant des extras ($)",
        min_value=0.00,
        step=1.00
    )

    # ---------- CALCULS ----------
    sous_total = montant + extra_val + FRAIS_DEPLACEMENT
    taxes_calc = sous_total * TAUX_TOTAL
    total = sous_total + taxes_calc

    st.info(f"🚗 Frais de déplacement : {FRAIS_DEPLACEMENT:.2f}$")
    st.write(f"**Sous-total :** {sous_total:.2f}$")
    st.write(f"**Taxes :** {taxes_calc:.2f}$")
    st.write(f"**TOTAL :** {total:.2f}$")
    st.write(f"**Dépôt 25% :** {total * 0.25:.2f}$")

    date_estimation = st.date_input("Date", value=datetime.date.today())

    submitted = st.form_submit_button("Créer l'estimation")


# ---------- SUBMIT ----------
if submitted:

    if not nom_client or not adresse_client:
        st.error("Nom et adresse obligatoires.")
        st.stop()

    numero = f"EST-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    utilisateur = st.session_state["username"]

    data = {
        "numero": numero,
        "utilisateur": utilisateur,
        "client": nom_client,
        "adresse": adresse_client,
        "telephone": numero_client,
        "couriel": couriel_client,
        "service": service,
        "superficie": superficie,
        "description": description,

        "montant": f"{montant:.2f}",

        "extra1": extra1,
        "extra2": extra2,
        "exdescription": exdescription,
        "extraprix": f"{extra_val:.2f}",

        "deplacement": f"{FRAIS_DEPLACEMENT:.2f}",
        "sous_total": f"{sous_total:.2f}",

        "taxes": f"{taxes_calc:.2f}",
        "total": f"{total:.2f}",

        "date_estimation": str(date_estimation)
    }

    # ---------- SAUVEGARDE ----------
    add_estimation(data)
    st.success("✅ Estimation enregistrée dans Google Sheets")

    # ---------- HTML ----------
    html = generate_estimation_html(data)

    # 🡇 Téléchargement local
    st.download_button(
        "📄 Télécharger l'estimation (HTML)",
        html,
        file_name=f"{numero}.html",
        mime="text/html"
    )
