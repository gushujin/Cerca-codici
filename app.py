import streamlit as st

st.set_page_config(page_title="Siemens SENTRON Configurator V4", layout="wide")

st.title("⚡ Configuratore Siemens SENTRON - Catalogo Completo")
st.markdown("Identificazione codici basata su serie 5SL3, 5SL6, 5SY4, 5SY7 e 5SV6.")

# --- MAPPATURA DATI TECNICI DA IMMAGINI ---
# Struttura: {Potere: {Tipo: Prefisso}}
DATA_MAP = {
    "4,5 kA": {
        "1P+N (1 Modulo - 1UM)": "5SL30",
        "1P+N (2 Moduli - 2UM)": "5SL35",
        "2 Poli (2P)": "5SL32"
    },
    "6 kA": {
        "1P+N (1 Modulo - 1UM)": "5SL60",
        "1P+N (2 Moduli - 2UM)": "5SL65",
        "2 Poli (2P)": "5SL62"
    },
    "10 kA": {
        "1P": "5SY41", "2P": "5SY42", "3P": "5SY43", "4P": "5SY44", "1P+N": "5SY45", "3P+N": "5SY46"
    },
    "15 kA": {
        "1P": "5SY71", "2P": "5SY72", "3P": "5SY73", "4P": "5SY74", "1P+N": "5SY75", "3P+N": "5SY76"
    }
}

tab1, tab2, tab3 = st.tabs(["Magnetotermici", "Differenziali Puri", "Antincendio (AFDD)"])

with tab1:
    st.subheader("Interruttori Magnetotermici")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        p_sel = st.selectbox("Potere di Interruzione", ["4,5 kA", "6 kA", "10 kA", "15 kA"])
        # Filtra le configurazioni in base al potere scelto
        config_options = list(DATA_MAP[p_sel].keys())
        conf_sel = st.selectbox("Configurazione / Poli", config_options)
        
    with c2:
        # Range correnti (In) - Gestione automatica zeri
        ampere = st.selectbox("Corrente Nominale (In)", ["0,5", "1", "1,6", "2", "3", "4", "6", "8", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
        a_code = ampere.replace(",", "")
        if len(a_code) == 1: a_code = "0" + a_code
        
    with c3:
        curva = st.radio("Curva", ["B (6)", "C (7)", "D (8)"])
        cur_code = curva[-2]

    # Generazione Codice
    prefix = DATA_MAP[p_sel][conf_sel]
    # Se il prefisso ha già 5 cifre (es 5SY41), aggiungiamo solo ampere e curva
    if len(prefix) == 5:
        codice_mcb = f"{prefix}{a_code}-{cur_code}"
    else:
        # Per 5SL30/60 il formato è Prefisso + Ampere + -Curva
        codice_mcb = f"{prefix}{a_code}-{cur_code}"

    st.info(f"**Codice Prodotto Identificato:**\n### {codice_mcb}")

with tab2:
    st.subheader("Differenziali Puri 5SV")
    col_a, col_b = st.columns(2)
    with col_a:
        t_sv = st.selectbox("Tipo", ["AC (0)", "A (6)", "F (3)", "B (4)"])
        s_sv = st.selectbox("Sensibilità (IΔn)", ["30mA (3)", "300mA (6)"])
    with col_b:
        p_sv = st.selectbox("Poli", ["1P+N (1)", "3P+N (4)"])
        i_sv = st.selectbox("Corrente (In)", ["16A (1)", "25A (2)", "40A (4)", "63A (6)", "80A (8)"])
    
    codice_sv = f"5SV3{s_sv[-2]}{p_sv[-2]}{i_sv[-2]}-{t_sv[-2]}"
    st.info(f"**Codice Differenziale:**\n### {codice_sv}")

with tab3:
    st.subheader("AFDD 5SV6")
    a_afdd = st.select_slider("Ampere (In)", options=["06", "10", "13", "16", "20", "25", "32", "40"])
    c_afdd = st.radio("Curva Magnetotermica", ["B", "C"], horizontal=True)
    st.info(f"**Codice AFDD:**\n### 5SV6016-{c_afdd}{a_afdd}")
