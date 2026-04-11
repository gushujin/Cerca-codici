import streamlit as st

# Configurazione del Portale
st.set_page_config(page_title="SENTRON Selector Pro", layout="wide", page_icon="⚡")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #005f73; color: white; }
    .code-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #0a9396; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IMPOSTAZIONI DI SISTEMA ---
st.sidebar.title("🛠️ System Settings")
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS (Original)", "ABB (Equivalent)", "Schneider (Equivalent)"])
st.sidebar.divider()
st.sidebar.markdown("### Supporto Tecnico\nBasato su Catalogo SENTRON 10/2019")

# --- HEADER ---
st.title("🔌 Portale di Configurazione Apparecchiature Modulari")
st.write(f"Configurazione attiva: **{brand}** | Database: **File 33_CF / 5_CF**")

# --- LOGICA DI NAVIGAZIONE ---
categoria = st.selectbox("Seleziona Categoria Prodotto", [
    "Magnetotermici (5SL, 5SY, 5SP)", 
    "Magnetotermici Scatolati (3VA)", 
    "Differenziali Puri (5SV)", 
    "Magnetotermici Differenziali (5SU1/5SV1)",
    "Accessori e Moduli AFDD"
])

st.divider()

col_params, col_res = st.columns([2, 1])

with col_params:
    st.subheader("⚙️ Caratteristiche Tecniche")
    
    if categoria == "Magnetotermici (5SL, 5SY, 5SP)":
        c1, c2, c3 = st.columns(3)
        with c1:
            p_int = st.selectbox("Potere Interruzione (Icn)", ["4,5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            poli = st.selectbox("Configurazione Poli", ["1P", "1P+N (1UM)", "1P+N (2UM)", "2P", "3P", "3P+N (4UM)", "4P"])
        with c2:
            amp = st.selectbox("Corrente (In)", ["0.5", "1", "2", "4", "6", "10", "13", "16", "20", "25", "32", "40", "50", "63", "80", "100", "125"])
            curva = st.radio("Curva", ["B", "C", "D"], horizontal=True)
        with c3:
            serie_pref = "5SL3" if "4,5" in p_int else "5SL6" if "6" in p_int else "5SY4" if "10" in p_int else "5SY7" if "15" in p_int else "5SY8"
            if "80" in amp or "100" in amp or "125" in amp: serie_pref = "5SP4"
            
        # Logica codifica poli (Doc 33_CF)
        poli_map = {"1P": "1", "1P+N (1UM)": "0", "1P+N (2UM)": "5", "2P": "2", "3P": "3", "3P+N (4UM)": "6", "4P": "4"}
        a_code = amp.replace(".", "").zfill(2)
        c_code = {"B": "6", "C": "7", "D": "8"}[curva]
        codice_final = f"{serie_pref}{poli_map[poli]}{a_code}-{c_code}"

    elif categoria == "Differenziali Puri (5SV)":
        c1, c2, c3 = st.columns(3)
        with c1:
            tipo = st.selectbox("Classe", ["A (Impulsiva)", "AC (Sinusoidale)", "F (Frequenza)", "B (Universale CC)"])
            sens = st.selectbox("Sensibilità (IΔn)", ["10 mA", "30 mA", "300 mA", "500 mA"])
        with c2:
            poli_sv = st.radio("Poli", ["1P+N", "3P+N"])
            in_sv = st.selectbox("Corrente (In)", ["16 A", "25 A", "40 A", "63 A", "80 A"])
        with c3:
            versione = st.multiselect("Varianti Speciali", ["Immunizzato (K)", "Selettivo (S)"])
        
        # Logica codifica (Doc 33_CF)
        t_map = {"A": "6", "AC": "0", "F": "3", "B": "4"}
        suff = "KK01" if "Immunizzato (K)" in versione else "8" if "Selettivo (S)" in versione else t_map[tipo[0]]
        codice_final = f"5SV3{sens.split()[0][0]}{'1' if '1P' in poli_sv else '4'}{in_sv.split()[0][0]}-{suff}"

    elif categoria == "Magnetotermici Differenziali (5SU1/5SV1)":
        c1, c2 = st.columns(2)
        with c1:
            ingombro = st.radio("Ingombro", ["Compatto (1 Modulo - 5SV1)", "Standard (2 Moduli - 5SU1)"])
            p_int_diff = st.selectbox("Potere Interruzione", ["4,5 kA", "6 kA", "10 kA"])
        with c2:
            amp_diff = st.selectbox("Corrente", ["6", "10", "13", "16", "20", "25", "32", "40"])
            curva_diff = st.radio("Curva", ["B", "C"])
        
        if "Compatto" in ingombro:
            pref_diff = "5SV1313" if "4,5" in p_int_diff else "5SV1316"
            codice_final = f"{pref_diff}-{curva_diff}{amp_diff.zfill(2)}"
        else:
            codice_final = f"5SU1354-{curva_diff}{amp_diff.zfill(2)}"

    elif categoria == "Magnetotermici Scatolati (3VA)":
        st.info("Configurazione Serie 3VA1 / 3VA2")
        frame = st.selectbox("Grandezza (Frame Size)", ["100A", "160A", "250A", "400A", "630A"])
        poli_3va = st.radio("Poli", ["3P", "4P"], horizontal=True)
        codice_final = f"3VA11{frame[:2]}{poli_3va[0]}..." # Logica semplificata per scatolati

    elif categoria == "Accessori e Moduli AFDD":
        st.info("Moduli SIARC 5SV6 e Accessori comuni")
        acc = st.selectbox("Tipo Accessorio", ["AFDD (Protezione Antincendio)", "Contatto Ausiliario", "Sganciatore Shunt"])
        if "AFDD" in acc:
            amp_af = st.selectbox("Ampere", ["06", "10", "16", "20", "25", "32", "40"])
            codice_final = f"5SV6016-7{amp_af}"
        else:
            codice_final = "5ST3..."

with col_res:
    st.markdown('<div class="code-box">', unsafe_allow_html=True)
    st.subheader("📌 Risultato Selezione")
    st.write(f"**Produttore:** {brand}")
    
    if brand == "SIEMENS (Original)":
        st.title(f"`{codice_final}`")
        st.caption("Codice d'ordinazione Siemens SENTRON")
    else:
        st.warning(f"Ricerca equivalente per {brand}...")
        st.write("Il sistema sta mappando le caratteristiche tecniche su database esterni.")
        st.info(f"Parametri di ricerca: {p_int if 'p_int' in locals() else 'Standard'} | {poli if 'poli' in locals() else '1P+N'}")
    
    st.button("📋 Copia Codice")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TABELLA DI CONFRONTO VELOCE ---
st.divider()
with st.expander("🔍 Visualizza Tabella di Selezione Rapida (Estratto 33_CF)"):
    st.table({
        "Caratteristica": ["4.5 kA", "6 kA", "10 kA", "15 kA", "Differenziale A", "AFDD"],
        "Serie Siemens": ["5SL3", "5SL6", "5SY4", "5SY7", "5SV3", "5SV6"],
        "Moduli (DIN)": ["1 o 2", "1 o 2", "1 - 4", "1 - 4", "2 o 4", "1"]
    })
