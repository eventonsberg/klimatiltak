import streamlit as st
from google.oauth2.service_account import Credentials
import gspread

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=scope)
client = gspread.authorize(credentials)

def registrer_tiltak(data):
    sheet = client.open("Klimatiltak").sheet1
    sheet.append_row(data)
    st.toast("Tiltaket er registrert!", icon="✅", duration="long")