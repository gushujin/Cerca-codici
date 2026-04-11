import streamlit as st

st.set_page_config(page_title="Configuratore Siemens SENTRON", layout="wide")

st.title("⚡ Configuratore Professionale Siemens SENTRON")
st.markdown("### Selezione guidata basata sul Catalogo Ottobre 2019")

# Definizione dei dati estratti dal catalogo
DATI_MCB = {
    "4,5 kA (Serie 5SL3)": {"prefisso": "5SL3", "poli_options": ["1P+N (0)", "2P (2)", "1P+N 2UM (5)"]},
    "6 kA (Serie 5SL6)": {"prefisso": "5SL6", "poli_options": ["1P+N (0)", "2P (2)", "1P+N 2UM (5)"]},
    "10 kA (Serie 5SY4)": {"prefisso": "5SY4", "poli_options": ["1P (1)", "2P (2)", "1P+N (5)", "3P (3)", "4P (4)", "3P+N (6)"]},
    "15 kA (Serie 5SY7)": {"prefisso": "5SY7", "poli_options": ["1P (1)", "2P (2)", "1P+N (5)", "3P (3)", "4P (4)", "3P+N (6)"]}
}

tab1, tab2, tab3 = st.tabs(["Magnetotermici (MCB)", "Differenziali (RCCB)", "Antincendio (AFDD)"])

# --- TAB MAGNETOTERMICI ---
with tab1:
    st.subheader("Interruttori Magnetotermici (5SL / 5SY)")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        potere = st.selectbox("Potere di Interruzione (Icn)", list(DATI_MCB.keys()))
        info = DATI_MCB[potere]
        poli = st.selectbox("Configurazione Poli", info["poli_options"])
        
    with c2:
        ampere = st.selectbox("Corrente Nominale (In)", 
                             ["0,5", "1", "1,6", "2", "3", "4", "6", "8", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
        # Formattazione ampere per codice
        a_code = ampere.replace(",", "")
        if len(a_code) == 1: a_code = "0" + a_code
        elif a_code == "05": a_code = "05" # Caso 0,5A -> 05
            
    with c3:
        curva = st.radio("Curva di Intervento", ["B (6)", "C (7)", "D (8)"])
        curva_code = curva.split("(")[1][0]

    # Logica di costruzione codice
    pref = info["prefisso"]
    p_code = poli.split("(")[1][0]
    
    codice_finale = f"{pref}{p_code}{a_code}-{curva_code}"
    st.success(f"**Codice Prodotto:** {codice_finale}")

# --- TAB DIFFERENZIALI ---
with tab2:
    st.subheader("Interruttori Differenziali Puri (5SV)")
    d1, d2, d3 = st.columns(3)
    
    with d1:
        tipo = st.selectbox("Tipo/Classe", ["AC (0)", "A (6)", "F (3)", "B (4)"])
        sens = st.selectbox("Sensibilità (IΔn)", ["30mA (3)", "300mA (6)", "500mA (7)"])
        
    with d2:
        p_sv = st.selectbox("Poli", ["1P+N (1)", "3P+N (4)"])
        a_sv = st.selectbox("Corrente (In)", ["16A (1)", "25A (2)", "40A (4)", "63A (6)", "80A (8)"])
        
    with d3:
        special = st.multiselect("Versioni Speciali", ["K (Antidisturbo/Immunizzato)", "S (Selettivo)"])
    
    # Costruzione codice 5SV
    # Esempio: 5SV3 3 1 4 - 6 (Tipo A, 30mA, 1P+N, 40A)
    esec = "3" # Top di default
    suffisso = ""
    if "K (Antidisturbo/Immunizzato)" in special: suffisso = "KK01"
    if "S (Selettivo)" in special: esec = "3"; sens = "6"; suffisso = "8" # Logica specifica catalogo

    codice_sv = f"5SV{esec}{sens[0]}{p_sv.split('(')[1][0]}{a_sv.split('(')[1][0]}-{tipo.split('(')[1][0]}{suffisso}"
    st.success(f"**Codice Prodotto:** {codice_sv}")

# --- TAB AFDD ---
with tab3:
    st.subheader("Protezione Antincendio 5SV6 (1 Modulo)")
    st.info("Protezione AFDD + Magnetotermico integrato in soli 18mm.")
    a_afdd = st.select_slider("Ampere (In)", options=["06", "10", "13", "16", "20", "25", "32", "40"])
    c_afdd = st.radio("Curva", ["B", "C"], horizontal=True)
    
    st.success(f"**Codice Prodotto:** 5SV6016-{c_afdd}{a_afdd}")
