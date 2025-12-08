import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=scope)
client = gspread.authorize(credentials)

def registrer_tiltak(data):
    tiltak_id = st.session_state.get('forrige_tiltak_id', 0) + 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet = client.open("Klimatiltak").sheet1
    sheet.append_row([tiltak_id, timestamp] + data)
    st.session_state['tiltak_id'] = tiltak_id
    st.cache_data.clear()

@st.cache_data
def hent_registrerte_tiltak():
    sheet = client.open("Klimatiltak").sheet1
    records = sheet.get_all_records()
    st.session_state['forrige_tiltak_id'] = records[-1]['ID-nummer'] if records else 0
    return records