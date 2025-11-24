import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_service_account"], scope)
client = gspread.authorize(credentials)

def registrer_tiltak(data):
    sheet = client.open("Klimatiltak").sheet1
    sheet.append_row(data)
    st.toast("Tiltaket er registrert!", icon="✅", duration="long")