import streamlit as st

# Configurazione del Portale
st.set_page_config(page_title="SENTRON Selector Pro V9", layout="wide", page_icon="⚡")

# --- CSS PER LOOK PROFESSIONALE ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-box { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .result-card { background-color: #005f73; color: white; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IMPOSTAZIONI ---
st.sidebar.title("⚙️ Impostazioni")
brand = st.sidebar.selectbox("Produttore", ["SIEMENS", "ABB", "Schneider"])
st.sidebar.divider()
st.sidebar.info("Dati basati su Catalogo SENTRON 10/2019 e serie compatte 5SV1.")

# --- TITOLO ---
st.title("🔌 Portale Tecnico Siemens SENTRON")
st.write(f"Configurazione attiva: **{brand}** | Rif. Documenti: **33_CF, 5_CF e 5SV1**")

# --- SELEZIONE CATEGORIA (MULTI-SCELTA) ---
categoria = st.selectbox("Seleziona Categoria Prodotto", [
    "Magnetotermici (5SL, 5SY, 5SP)", 
    "Magnetotermici Differenziali (5SU1, 5SV1 COMPATTI)", 
    "Differenziali Puri (5SV)", 
    "Magnetotermici Scatolati (3VA)", 
    "Accessori e AFDD"
])

st.divider()

col_params, col_res = st.columns([2, 1])

with col_params:
    st.subheader("🛠️ Specifiche Tecniche")
    
    # --- 1. MAGNETOTERMICI STANDARD ---
    if categoria == "Magnetotermici (5SL, 5SY, 5SP)":
        c1, c2 = st.columns(2)
        with c1:
            pdi = st.selectbox("Potere Interruzione", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            poli = st.selectbox("Poli", ["1P", "1P+N (1UM)", "1P+N (2UM)", "2P", "3P", "3P+N", "4P"])
        with c2:
            amp = st.selectbox("Corrente (In)", ["06", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
            curva = st.radio("Curva", ["B", "C", "D"], horizontal=True)
        
        pref = "5SL3" if "4.5" in pdi else "5SL6" if "6" in pdi else "5SY4" if "10" in pdi else "5SY7" if "15" in pdi else "5SY8"
        p_map = {"1P": "1", "1P+N (1UM)": "0", "1P+N (2UM)": "5", "2P": "2", "3P": "3", "3P+N": "6", "4P": "4"}
        codice_final = f"{pref}{p_map[poli]}{amp.replace(',','')}-{curva[0]}{amp}"

    # --- 2. MAGNETOTERMICI DIFFERENZIALI (INTEGRAZIONE 5SV1) ---
    elif categoria == "Magnetotermici Differenziali (5SU1, 5SV1 COMPATTI)":
        tipo_md = st.radio("Scegli Modello", ["Standard (2 Moduli - 5SU1)", "Compatto (1 Modulo - 5SV1)"], horizontal=True)
        
        if tipo_md == "Compatto (1 Modulo - 5SV1)":
            c1, c2 = st.columns(2)
            with c1:
                pdi_sv = st.selectbox("Potere Interruzione", ["4.5 kA (5SV1...3)", "6 kA (5SV1...6)"])
                p_code = "3" if "4.5" in pdi_sv else "6"
                tipo_sv = st.radio("Classe", ["AC (Standard)", "A (Impulsiva)"])
                t_code = "3" if "AC" in tipo_sv else "6"
            with c2:
                curva_sv = st.selectbox("Curva", ["B", "C"])
                amp_sv = st.selectbox("Ampere", ["06", "10", "13", "16", "20", "25", "32"])
            codice_final = f"5SV1{t_code}1{p_code}-{curva_sv}{amp_sv}"
        else:
            codice_final = "5SU1..." # Logica standard

    # --- 3. DIFFERENZIALI PURI ---
    elif categoria == "Differenziali Puri (5SV)":
        c1, c2 = st.columns(2)
        with c1:
            sens = st.selectbox("Sensibilità (IΔn)", ["30 mA (3)", "10 mA (1)", "300 mA (6)"])
            amp_d = st.selectbox("Corrente (In)", ["25 A", "40 A", "63 A", "16 A"])
        with c2:
            poli_d = st.radio("Poli", ["1P+N (1)", "3P+N (4)"])
            classe_d = st.selectbox("Classe", ["A (6)", "AC (0)", "F (3)", "B (4)"])
        codice_final = f"5SV3{sens[-2]}{poli_d[-2]}{amp_d[0]}-{classe_d[-2]}"

    # --- ALTRE CATEGORIE ---
    else:
        st.info("Configurazione in fase di aggiornamento per Scatolati e Accessori.")
        codice_final = "IN ELABORAZIONE"

with col_res:
    st.subheader("📌 Risultato")
    if brand == "SIEMENS":
        st.success(f"### `{codice_final}`")
        st.caption("Codice d'ordinazione Siemens")
    else:
        st.warning(f"Cercando equivalente {brand}...")
        st.info(f"Parametri: {categoria}")

st.divider()
st.caption("Strumento di supporto tecnico - Verificare sempre sul catalogo ufficiale prima dell'ordine.")
