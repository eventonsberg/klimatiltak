import streamlit as st
import pandas as pd
import altair as alt
from formatering import formater_nummer

def vis_sammenligning_av_unngaatte_utslipp(utslippsreduksjon_nytt_tiltak, tiltak_ids_sammenligning, registrerte_tiltak):
    utslippsreduksjon = [{
        "Tiltak": "Nytt tiltak",
        "Utslippsreduksjon": utslippsreduksjon_nytt_tiltak/1000
    }]
    for tiltak in registrerte_tiltak:
        if tiltak['ID-nummer'] in tiltak_ids_sammenligning:
            utslippsreduksjon.append({
                "Tiltak": f"Tiltak {tiltak['ID-nummer']}",
                "Utslippsreduksjon": tiltak.get('Unngåtte utslipp, totalt [kg CO2-ekv.]', 0)/1000
            })
    df = pd.DataFrame(utslippsreduksjon)
    chart = alt.Chart(df, height=alt.Step(30)).mark_bar().encode(
        y=alt.Y('Tiltak:N', title=None),
        x=alt.X('Utslippsreduksjon:Q', title='Utslippsreduksjon [tonn CO2-ekv.]'),
        tooltip=['Tiltak', 'Utslippsreduksjon']
    ).properties(
        title='Unngåtte utslipp, totalt'
    ).configure_title(
        anchor='middle'
    )
    st.altair_chart(chart)

def vis_sammenligning_av_naaverdi(naaverdi_nytt_tiltak, tiltak_ids_sammenligning, registrerte_tiltak):
    naaverdi = [{
        "Tiltak": "Nytt tiltak",
        "Nåverdi": naaverdi_nytt_tiltak
    }]
    for tiltak in registrerte_tiltak:
        if tiltak['ID-nummer'] in tiltak_ids_sammenligning:
            naaverdi.append({
                "Tiltak": f"Tiltak {tiltak['ID-nummer']}",
                "Nåverdi": tiltak.get('Tiltakets nåverdi [NOK]', 0)
            })
    df = pd.DataFrame(naaverdi)
    df['Nåverdi_formatert'] = df['Nåverdi'].apply(lambda x: formater_nummer(x, 0))
    chart = alt.Chart(df, height=alt.Step(30)).mark_bar().encode(
        y=alt.Y('Tiltak:N', title=None),
        x=alt.X('Nåverdi:Q', title='Nåverdi [NOK]'),
        tooltip=[
            alt.Tooltip('Tiltak:N', title='Tiltak'),
            alt.Tooltip('Nåverdi_formatert:N', title='Nåverdi')
        ]
    ).properties(
        title='Nåverdi'
    ).configure_title(
        anchor='middle'
    )
    st.altair_chart(chart)

def vis_sammenligning_av_tiltakskostnad(tiltakskostnad_nytt_tiltak, tiltak_ids_sammenligning, registrerte_tiltak):
    tiltakskostnad = [{
        "Tiltak": "Nytt tiltak",
        "Tiltakskostnad": tiltakskostnad_nytt_tiltak
    }]
    for tiltak in registrerte_tiltak:
        if tiltak['ID-nummer'] in tiltak_ids_sammenligning:
            tiltakskostnad.append({
                "Tiltak": f"Tiltak {tiltak['ID-nummer']}",
                "Tiltakskostnad": tiltak.get('Tiltakskostnad [NOK/tonn CO2-ekv.]', 0)
            })
    df = pd.DataFrame(tiltakskostnad)
    df['Tiltakskostnad_formatert'] = df['Tiltakskostnad'].apply(lambda x: formater_nummer(x, 0))
    chart = alt.Chart(df, height=alt.Step(30)).mark_bar().encode(
        y=alt.Y('Tiltak:N', title=None),
        x=alt.X('Tiltakskostnad:Q', title='Tiltakskostnad [NOK per tonn CO2-ekv.]'),
        tooltip=[
            alt.Tooltip('Tiltak:N', title='Tiltak'),
            alt.Tooltip('Tiltakskostnad_formatert:N', title='Tiltakskostnad')
        ]
    ).properties(
        title='Tiltakskostnad'
    ).configure_title(
        anchor='middle'
    )
    st.altair_chart(chart)