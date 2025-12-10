import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
import datetime
import pandas as pd
from ulid import ULID

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=scope)
client = gspread.authorize(credentials)

def registrer_tiltak(data):
    unik_id = str(ULID())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet = client.open("Klimatiltak").sheet1
    sheet.append_row([unik_id, timestamp] + data)
    st.session_state['unik_id'] = unik_id
    st.cache_data.clear()

@st.cache_data
def hent_registrerte_tiltak():
    sheet = client.open("Klimatiltak").sheet1
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    df.insert(0, 'Tiltaksnummer', range(1, len(df) + 1))
    return df