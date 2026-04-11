import streamlit as st

# Configurazione Layout Wide (Professionale)
st.set_page_config(page_title="SENTRON Consultant Portal", layout="wide", page_icon="🔌")

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IMPOSTAZIONI GLOBALI ---
st.sidebar.title("⚙️ Impostazioni Portale")
produttore_selezionato = st.sidebar.selectbox("Produttore Attivo", ["SIEMENS (Default)", "ABB (Equivalente)", "Schneider (Equivalente)"])
st.sidebar.divider()
st.sidebar.info(f"Dati tecnici validati secondo: Catalogo SENTRON 10/2019 (File 33_CF)")

# --- LOGICA CAMBIO PRODUTTORE (MAPPING) ---
mapping_brand = {
    "SIEMENS (Default)": {"4.5kA": "5SL3", "6kA": "5SL6", "10kA": "5SY4", "15kA": "5SY7"},
    "ABB (Equivalente)": {"4.5kA": "SH200L", "6kA": "S200", "10kA": "S200M", "15kA": "S200P"},
    "Schneider (Equivalente)": {"4.5kA": "iK60N", "6kA": "iC60N", "10kA": "iC60H", "15kA": "iC60L"}
}

# --- PORTALE PRINCIPALE ---
st.title("🔌 Portale di Consultazione Apparecchiature")
st.write(f"Stai consultando il catalogo per: **{produttore_selezionato}**")

tab1, tab2 = st.tabs(["📊 CONFIGURATORE CODICI", "📑 SPECIFICHE TECNICHE"])

with tab1:
    col_input, col_output = st.columns([2, 1])

    with col_input:
        st.subheader("Selezione Parametri")
        c1, c2 = st.columns(2)
        
        with c1:
            p_int = st.selectbox("Potere di Interruzione (Icn)", ["4.5kA", "6kA", "10kA", "15kA"])
            poli = st.selectbox("Configurazione Poli", ["1P", "1P+N (1UM)", "1P+N (2UM)", "2P", "3P", "3P+N", "4P"])
            
        with c2:
            amp = st.selectbox("Corrente Nominale (In)", ["06", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
            curva = st.radio("Curva di Intervento", ["B", "C", "D"], horizontal=True)

    with col_output:
        st.subheader("Risultato")
        
        # Logica di costruzione codice Siemens (basata su 33_CF)
        prefix = mapping_brand["SIEMENS (Default)"][p_int]
        poli_map = {"1P": "1", "1P+N (1UM)": "0", "1P+N (2UM)": "5", "2P": "2", "3P": "3", "3P+N": "6", "4P": "4"}
        curva_map = {"B": "6", "C": "7", "D": "8"}
        
        codice_siemens = f"{prefix}{poli_map[poli]}{amp}-{curva_map[curva]}"
        
        # Visualizzazione Metriche
        st.metric(label="Codice Siemens", value=codice_siemens)
        
        if produttore_selezionato != "SIEMENS (Default)":
            prefix_alt = mapping_brand[produttore_selezionato][p_int]
            st.warning(f"Equivalente {produttore_selezionato}: {prefix_alt} (Verificare poli/curva su catalogo specifico)")

with tab2:
    st.subheader("Estratto Struttura Codice (Rif. Documento 33_CF)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        **Composizione MCB (Magnetotermici):**
        * **Cifra 1-4:** Serie (es. 5SL3 = 4.5kA)
        * **Cifra 5:** Poli (0=1UM, 5=1P+N 2UM, 2=2P)
        * **Cifra 6-7:** Ampere (es. 16 = 16A)
        * **Suffisso:** Curva (-7 = C)
        """)
    with col_b:
        st.markdown("""
        **Composizione RCCB (Differenziali):**
        * **Radice:** 5SV3
        * **Cifra 5:** Sensibilità (3 = 30mA)
        * **Cifra 6:** Poli (1 = 1P+N, 4 = 3P+N)
        * **Cifra 7:** Ampere (4 = 40A)
        """)

st.divider()
st.caption("Strumento di consultazione ad uso interno - Dati basati su Catalogo Siemens Ottobre 2019")
