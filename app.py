import streamlit as st

st.set_page_config(page_title="Siemens SENTRON Master Configurator", layout="wide")

st.title("⚡ Siemens SENTRON - Catalogo Ottobre 2019")
st.subheader("Configurazione Precisa Apparecchi Modulari")

tab1, tab2, tab3 = st.tabs(["Magnetotermici (MCB)", "Differenziali (RCCB)", "AFDD (SIARC)"])

# --- MAGNETOTERMICI ---
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        p_int = st.selectbox("Potere Interruzione", ["4,5 kA", "6 kA", "10 kA", "15 kA"])
        tipo = st.radio("Ingombro/Poli", ["Compatto 1P+N (1UM)", "Standard 1P+N (2UM)", "Standard 2P (2UM)", "Serie Industriale (1P-4P)"])
    
    with c2:
        amp = st.selectbox("Corrente Nominale (In)", ["02", "04", "06", "08", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
        curva = st.radio("Curva", ["B (6)", "C (7)", "D (8)"])
        cur_c = curva[-2]

    # Logica Codice basata su Tabelle Catalogo pag. 3/3 e 3/4
    pref = "5SL3" if "4,5" in p_int else "5SL6" if "6" in p_int else "5SY4" if "10" in p_int else "5SY7"
    
    if "Compatto" in tipo:
        pref = pref[:4] + "0" # es. 5SL30
    elif "Standard 1P+N" in tipo:
        pref = pref[:4] + "5" # es. 5SL35
    elif "Standard 2P" in tipo:
        pref = pref[:4] + "2" # es. 5SL32
        
    cod_mcb = f"{pref}{amp}-{cur_c}"
    st.success(f"**Codice Magnetotermico:** {cod_mcb}")

# --- DIFFERENZIALI ---
with tab2:
    d1, d2 = st.columns(2)
    with d1:
        classe = st.selectbox("Tipo Differenziale", ["AC (Standard)", "A (Impulsiva)", "A-K (Immunizzato)", "A-S (Selettivo)", "F", "B"])
        sens = st.selectbox("IΔn", ["30 mA", "300 mA"])
    with d2:
        poli = st.radio("Poli Differenziale", ["1P+N", "3P+N"])
        in_d = st.selectbox("In (A)", ["16", "25", "40", "63", "80"])

    # Logica semplificata codifica 5SV (pag. 3/5)
    t_map = {"AC": "0", "A": "6", "A-K": "6KK01", "A-S": "8", "F": "3", "B": "4"}
    cod_sv = f"5SV3{sens[0]}{'1' if '1P' in poli else '4'}{in_d[0]}-{t_map[classe.split()[0]]}"
    st.success(f"**Codice Differenziale:** {cod_sv}")

# --- AFDD ---
with tab3:
    st.info("Serie 5SV6: Protezione AFDD + Magnetotermico in 1 Modulo (6kA)")
    a_af = st.select_slider("Ampere", ["06", "10", "13", "16", "20", "25", "32", "40"])
    c_af = st.radio("Curva AFDD", ["B", "C"])
    st.success(f"**Codice AFDD:** 5SV6016-{c_af}{a_af}")
