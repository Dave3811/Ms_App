import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ---------- CLIENT ----------


def get_client():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )
    return gspread.authorize(creds)

# ---------- FEUILLES ----------


def get_sheet():
    client = get_client()
    return client.open_by_key(
        st.secrets["SHEETS"]["SHEET_ID"]
    ).sheet1


def get_factures_sheet():
    client = get_client()
    return client.open_by_key(
        st.secrets["SHEETS"]["SHEET_ID"]
    ).worksheet("Factures")


# ---------- INSERT ----------
def add_estimation(data: dict):
    sheet = get_sheet()

    data["extra1"] = "Oui" if data.get("extra1") else "Non"
    data["extra2"] = "Oui" if data.get("extra2") else "Non"

    row = [
        data["numero"],
        data["utilisateur"],
        data["client"],
        data["adresse"],
        data["telephone"],
        data["couriel"],
        data["service"],
        data["superficie"],
        data["description"],
        data["montant"],
        data["extra1"],
        data["extra2"],
        data["exdescription"],
        data["extraprix"],
        data["taxes"],
        data["total"],
        data["date_estimation"]
    ]

    sheet.append_row(row)


def add_facture(data: dict):
    sheet = get_factures_sheet()
    sheet.append_row(list(data.values()))
