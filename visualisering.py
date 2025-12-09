import streamlit as st
import pandas as pd
import altair as alt
from formatering import formater_nummer
from bakgrunnsdata import CO2_avgiftsnivå
from beregninger import beregn_karbonprisjustert_merkostnad

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

def vis_avgiftsbaner(aarlig_utslippsreduksjon, merkostnad):
    data = []
    relevante_aar = [aar for aar in CO2_avgiftsnivå.keys() if aar >= 2026]
    for aar in relevante_aar:
        karbonprisjustert_merkostnad = beregn_karbonprisjustert_merkostnad(aarlig_utslippsreduksjon, aar, merkostnad)
        naaverdi = karbonprisjustert_merkostnad / ((1.04) ** (aar - 2025))
        CO2_avgift = aarlig_utslippsreduksjon * CO2_avgiftsnivå[aar]
        data.append({
            "År": aar,
            "Karbonprisjustert merkostnad": karbonprisjustert_merkostnad,
            "Nåverdi": naaverdi,
            "CO2-avgiftsbesparelse": CO2_avgift
        })
    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=['År'], value_vars=['Karbonprisjustert merkostnad', 'Nåverdi', 'CO2-avgiftsbesparelse'],
                        var_name='Type', value_name='Verdi')
    chart = alt.Chart(df_melted).mark_line(strokeWidth=3).encode(
        x=alt.X('År:O', title='År', axis=alt.Axis(grid=True)),
        y=alt.Y('Verdi:Q', title='Verdi [NOK]'),
        color=alt.Color('Type:N', title='Type',
                        legend=alt.Legend(orient='bottom', title=None, padding=0, offset=0, labelLimit=200)),
        tooltip=[
            alt.Tooltip('År:O', title='År'),
            alt.Tooltip('Verdi:Q', title='Verdi')
        ]
    ).properties(
        title='Avgiftsbaner'
    ).configure_title(
        anchor='middle'
    )
    st.altair_chart(chart)