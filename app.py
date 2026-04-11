import streamlit as st

st.set_page_config(page_title="Siemens SENTRON Master", layout="wide")

st.title("⚡ Siemens SENTRON - Configurazione Integrale")
st.markdown("Basato su Catalogo Ottobre 2019: Magnetotermici (4.5/6/10/15kA) e Differenziali Puri/Magnetotermici.")

tab1, tab2, tab3 = st.tabs(["Magnetotermici (MCB)", "Differenziali (RCCB/RCBO)", "Antincendio (AFDD)"])

# --- SEZIONE MAGNETOTERMICI (5SL / 5SY) ---
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        potere = st.selectbox("Potere Interruzione", ["4,5 kA", "6 kA", "10 kA", "15 kA"], key="mcb_pot")
        # Logica prefissi estratti dalle tabelle
        mapping = {
            "4,5 kA": {"1P+N (1UM)": "5SL30", "1P+N (2UM)": "5SL35", "2P": "5SL32"},
            "6 kA": {"1P+N (1UM)": "5SL60", "1P+N (2UM)": "5SL65", "2P": "5SL62"},
            "10 kA": {"1P": "5SY41", "2P": "5SY42", "3P": "5SY43", "4P": "5SY44", "1P+N": "5SY45", "3P+N": "5SY46"},
            "15 kA": {"1P": "5SY71", "2P": "5SY72", "3P": "5SY73", "4P": "5SY74", "1P+N": "5SY75", "3P+N": "5SY76"}
        }
        tipo_mcb = st.selectbox("Esecuzione/Poli", list(mapping[potere].keys()))
    with c2:
        amp_mcb = st.selectbox("In (A)", ["0,5", "1", "2", "3", "4", "6", "10", "13", "16", "20", "25", "32", "40", "50", "63"], index=8)
        a_code = amp_mcb.replace(",", "").zfill(2)
    with c3:
        curva = st.radio("Curva", ["B (6)", "C (7)", "D (8)"], index=1)
    
    codice_mcb = f"{mapping[potere][tipo_mcb]}{a_code}-{curva[-2]}"
    st.info(f"**Codice Magnetotermico:** {codice_mcb}")

# --- SEZIONE DIFFERENZIALI (PURI 5SV / COMPATTI 5SV1) ---
with tab2:
    st.subheader("Configurazione Differenziali")
    st.markdown("*Nota: Include Serie 5SV (Puri) e Serie 5SV1 (Magnetotermici Differenziali 1UM)*")
    
    cat_diff = st.radio("Categoria", ["Puri (RCCB - 5SV)", "Magnetotermici Differenziali (RCBO - 5SV1)"], horizontal=True)
    
    d1, d2, d3 = st.columns(3)
    
    if cat_diff == "Puri (RCCB - 5SV)":
        with d1:
            classe = st.selectbox("Classe/Tipo", ["AC (0)", "A (6)", "F (3)", "B (4)"])
            sens = st.selectbox("Sensibilità (IΔn)", ["10mA (1)", "30mA (3)", "300mA (6)"])
        with d2:
            poli_sv = st.selectbox("Poli", ["1P+N (1)", "3P+N (4)"])
            in_sv = st.selectbox("Corrente Nominale (In)", ["16A (1)", "25A (2)", "40A (4)", "63A (6)", "80A (8)"])
        with d3:
            var = st.multiselect("Varianti", ["K (Superimmunizzato)", "S (Selettivo)"])
            
        # Costruzione codice 5SV
        suff = ""
        if "K (Superimmunizzato)" in var: suff = "KK01"
        if "S (Selettivo)" in var: 
            base_code = f"5SV36{poli_sv[-2]}{in_sv[-2]}-8" # I selettivi solitamente finiscono in -8
        else:
            base_code = f"5SV3{sens[-2]}{poli_sv[-2]}{in_sv[-2]}-{classe[-2]}"
        st.success(f"**Codice Differenziale Puro:** {base_code}{suff}")

    else: # RCBO 5SV1 (Magnetotermici Differenziali 1 modulo)
        with d1:
            p_int_rcbo = st.selectbox("Potere Interruzione", ["4,5 kA", "6 kA"])
            classe_rcbo = st.selectbox("Tipo", ["AC", "A"])
        with d2:
            amp_rcbo = st.selectbox("Corrente (In)", ["6", "10", "13", "16", "20", "25", "32", "40"])
            curva_rcbo = st.radio("Curva", ["B", "C"])
        
        pref_rcbo = "5SV1313" if p_int_rcbo == "4,5 kA" else "5SV1316"
        cod_rcbo = f"{pref_rcbo}-{curva_rcbo}{amp_rcbo.zfill(2)}"
        st.success(f"**Codice RCBO (1 Modulo):** {cod_rcbo}")

# --- SEZIONE AFDD ---
with tab3:
    st.info("Serie 5SV6: Protezione AFDD + Magnetotermico integrato (6kA)")
    a_af = st.selectbox("Corrente AFDD", ["06", "10", "13", "16", "20", "25", "32", "40"], index=3)
    c_af = st.radio("Curva Caratteristica", ["B", "C"], key="afdd_c")
    st.success(f"**Codice AFDD:** 5SV6016-{c_af}{a_af}")
