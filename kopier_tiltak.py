import streamlit as st

FIELD_MAP = {
    "DIF": "inp_dif",
    "Avdeling": "inp_avdeling",
    "Enhet": "inp_enhet",
    "Tiltaksbeskrivelse": "inp_beskrivelse",
    "Kilde til direkte utslipp": "inp_utslippskilde",
    "Materiell tilknyttet utslipp": "inp_materiell",
    "Antall materiell tiltaket målrettes": "inp_antall_materiell",
    "Kommentar antall materiell": "inp_antall_materiell_kommentar",
    "Materiellets nåværende forbruk": "inp_forbruk",
    "Kommentar nåværende forbruk": "inp_forbruk_kommentar",
    "Årlig reduksjon etter tiltaket (absolutt)": "inp_reduksjon_absolutt",
    "Årlig reduksjon etter tiltaket (prosent)": "inp_reduksjon_prosent",
    "Kommentar årlig reduksjon": "inp_reduksjon_kommentar",
    "Forventet engangsinvestering [NOK]": "inp_engangsinvestering",
    "Kommentar engangsinvestering": "inp_engangsinvestering_kommentar",
    "Forventet merkostnad (MK) [NOK/år]": "inp_merkostnad",
    "Kommentar merkostnad": "inp_merkostnad_kommentar",
    "Tiltakets levetid [år]": "inp_levetid",
    "Kommentar levetid": "inp_levetid_kommentar",
    "Ikke-kvantifiserte effekter": "inp_ikke_kvantifiserte_effekter"
}

def kopier_tiltak(tiltaksnummer, registrerte_tiltak):
    tiltak_data = registrerte_tiltak[registrerte_tiltak['Tiltaksnummer'] == tiltaksnummer]
    if tiltak_data.empty:
        return
    tiltak_data = tiltak_data.iloc[0]
    for felt_navn, komponent_key in FIELD_MAP.items():
        if felt_navn in tiltak_data:
            st.session_state[komponent_key] = tiltak_data[felt_navn]