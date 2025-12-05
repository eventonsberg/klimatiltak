from bakgrunnsdata import utslippskilder, CO2_avgiftsnivå

def beregn_aarlig_tiltaksmengde(antall, forbruk, reduksjon_absolutt, reduksjon_prosent):
    aarlig_tiltaksmengde = 0
    if reduksjon_absolutt > 0 and antall > 0:
        aarlig_tiltaksmengde = antall * reduksjon_absolutt
    elif reduksjon_prosent > 0 and forbruk > 0 and antall > 0:
        aarlig_tiltaksmengde = antall * forbruk * (reduksjon_prosent / 100)
    return aarlig_tiltaksmengde

def beregn_total_tiltaksmengde(aarlig_tiltaksmengde, levetid):
    total_tiltaksmengde = 0
    if aarlig_tiltaksmengde > 0 and levetid > 0:
        total_tiltaksmengde = aarlig_tiltaksmengde * levetid
    return total_tiltaksmengde

def beregn_aarlig_utslippsreduksjon(aarlig_tiltaksmengde, utslippskilde, materiell):
    aarlig_utslippsreduksjon = 0
    if (utslippskilde in utslippskilder and
        "Utslippsfaktor" in utslippskilder[utslippskilde] and
        materiell in utslippskilder[utslippskilde]["Utslippsfaktor"]):
        utslippsfaktor = utslippskilder[utslippskilde]["Utslippsfaktor"][materiell]
        aarlig_utslippsreduksjon = aarlig_tiltaksmengde * utslippsfaktor
    return aarlig_utslippsreduksjon

def beregn_total_utslippsreduksjon(aarlig_utslippsreduksjon, levetid):
    total_utslippsreduksjon = 0
    if aarlig_utslippsreduksjon > 0 and levetid > 0:
        total_utslippsreduksjon = aarlig_utslippsreduksjon * levetid
    return total_utslippsreduksjon

def beregn_karbonprisjustert_merkostnad_foerste_aar(aarlig_utslippsreduksjon, aar, merkostnad):
    karbonprisjustert_merkostnad_foerste_aar = 0
    if aar in CO2_avgiftsnivå:
        CO2_avgift = aarlig_utslippsreduksjon * CO2_avgiftsnivå[aar]
        karbonprisjustert_merkostnad_foerste_aar = merkostnad - CO2_avgift
    return karbonprisjustert_merkostnad_foerste_aar