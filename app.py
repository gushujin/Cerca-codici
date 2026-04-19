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

# --- SIDEBAR: IMPOSTAZIONI DI SISTEMA ---
st.sidebar.title("🛠️ System Settings")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Siemens-logo.svg", width=150)
st.sidebar.title("Configuratore Multibrand")
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS (Original)", "ABB (Equivalent)", "Schneider (Equivalent)"])
st.sidebar.divider()
st.sidebar.markdown("### Supporto Tecnico\nBasato su Catalogo SENTRON 10/2019")

# --- TITOLO ---
st.title("🔌 Portale Tecnico Siemens SENTRON")
st.write(f"Configurazione attiva: **{brand}** | Rif. Documenti: **33_CF, 5_CF e 5SV1**")

# --- SELEZIONE CATEGORIA ---
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
    
   # --- 1. MAGNETOTERMICI STANDARD (MULTIBRAND) ---
    if categoria.startswith("Magnetotermici (Serie: 5SL"):
        c1, c2 = st.columns(2)
        with c1:
            pdi = st.selectbox("Potere Interruzione", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            poli = st.selectbox("Poli", ["1P", "1P+N (1UM)", "1P+N (2UM)", "2P", "3P", "3P+N", "4P"])
        with c2:
            amp = st.selectbox("Corrente (In)", ["06", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
            curva = st.radio("Curva", ["B", "C", "D"], horizontal=True)

        # --- LOGICA DI DEFINIZIONE PREFISSI PER BRAND ---
        if "SIEMENS" in brand:
            pref = "5SL3" if "4.5" in pdi else "5SL6" if "6" in pdi else "5SL4" if "10" in pdi else "5SY7" if "15" in pdi else "5SY8"
            p_map = {"1P": "1", "1P+N (1UM)": "0", "1P+N (2UM)": "5", "2P": "2", "3P": "3", "3P+N": "6", "4P": "4"}
            # Costruzione MLFB Siemens: Prefisso + Polo + Amp - Curva + Amp
            codice_final = f"{pref}{p_map[poli]}{amp}-{curva[0]}{amp}"

        elif "ABB" in brand:
            # Esempio: S201-C16 (S200 è la serie standard 6kA)
            pref_abb = "S201L" if "4.5" in pdi else "S200" if "6" in pdi else "S200M" if "10" in pdi else "S200P"
            p_count = poli.split("P")[0] # Estrae il numero di poli
            codice_final = f"{pref_abb}-{curva[0]}{int(amp)}" # ABB non usa lo 0 davanti (es. C6, non C06)

        elif "Schneider" in brand:
            # Esempio: A9F74116 (iC60N) o R9P35616 (Resi9)
            if "6 kA" in pdi:
                pref_sn = "R9P" # Serie Resi9 per il residenziale
            else:
                pref_sn = "A9F" # Serie Acti9 iC60 per il terziario/industria
            codice_final = f"{pref_sn} [LOGICA SPECIFICA SCHNEIDER]"

# --- VISUALIZZAZIONE DATI DI TARGA ---
        st.markdown("---")
        st.markdown(f"#### 📝 Specifiche Tecniche {brand.split(' ')[0]}")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Serie", pref if "SIEMENS" in brand else "Equiv.")
        m2.metric("PDI", pdi)
        m3.metric("Poli", poli)
        m4.metric("In", f"{int(amp)}A")
    
   # --- 1. MAGNETOTERMICI STANDARD (LOGICA POSIZIONI 1-12) ---
if categoria.startswith("Magnetotermici (Serie: 5SL"):
    c1, c2 = st.columns(2)
    with c1:
        pdi = st.selectbox("Potere Interruzione (Pos. 4)", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
        poli_label = st.selectbox("Poli (Pos. 5)", ["1P", "1P+N (1UM)", "1P+N (2UM)", "2P", "3P", "3P+N", "4P"])
        p_map = {"1P": "1", "1P+N (1UM)": "0", "1P+N (2UM)": "5", "2P": "2", "3P": "3", "3P+N": "6", "4P": "4"}
        
    with c2:
        amp = st.selectbox("Corrente Nominale (Pos. 6-7 e 11-12)", ["06", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
        curva_label = st.radio("Curva (Pos. 10)", ["B", "C", "D"], horizontal=True)
        c_map = {"B": "5", "C": "7", "D": "8"}

    if "SIEMENS" in brand:
        # Identificazione Serie (Posizioni 1-3 e 4)
        if "4.5" in pdi: pref = "5SL3"
        elif "6" in pdi: pref = "5SL6"
        elif "10" in pdi: pref = "5SL4"
        elif "15" in pdi: pref = "5SY7"
        else: pref = "5SY8"

        # Costruzione stringa MLFB (12 Posizioni teoriche)
        # Pos 1-4: Serie/PDI | Pos 5: Poli | Pos 6-7: Ampere | Pos 8: Trattino | Pos 10: Curva | Pos 11-12: Ampere
        pos1_4 = pref
        pos5 = p_map[poli_label]
        pos6_7 = amp
        pos8 = "-"
        pos10 = c_map[curva_label]
        pos11_12 = amp
        
        codice_final = f"{pos1_4}{pos5}{pos6_7}{pos8}{pos10}{pos11_12}"

        # --- SEZIONE IDENTIFICAZIONE POSIZIONI ---
        st.markdown("---")
        st.subheader("🔍 Analisi Posizioni Codice MLFB")
        
        # Creazione di una griglia visiva per le posizioni
        pos_cols = st.columns(len(codice_final.replace("-", "")))
        full_code_no_dash = codice_final.replace("-", "")
        
        # Visualizzazione Cifra per Cifra
        for i, char in enumerate(codice_final):
            with st.container():
                st.markdown(f"""
                <div style="text-align:center; padding:5px; border:1px solid #ddd; border-radius:5px; background-color:white;">
                    <small>Pos.{i+1}</small><br>
                    <b style="color:#015F73; font-size:20px;">{char}</b>
                </div>
                """, unsafe_allow_html=True)

        # Tabella di Spiegazione Posizioni
        with st.expander("📖 Legenda Posizioni (Dettaglio Tecnico)", expanded=True):
            st.write(f"""
            | Posizione | Valore | Descrizione |
            | :--- | :--- | :--- |
            | **1 - 3** | `{pos1_4[:3]}` | **Famiglia:** Interruttore Magnetotermico SENTRON |
            | **4** | `{pos1_4[3]}` | **Potere Interruzione:** {pdi} |
            | **5** | `{pos5}` | **Configurazione Poli:** {poli_label} |
            | **6 - 7** | `{pos6_7}` | **Corrente Nominale (In):** {amp}A |
            | **8** | `-` | **Separatore Standard** |
            | **10** | `{pos10}` | **Curva di Intervento:** {curva_label} ({pos10}) |
            | **11 - 12** | `{pos11_12}` | **Suffisso Corrente:** {amp}A |
            """)

    else:
        st.warning(f"La mappatura delle posizioni per {brand} è in fase di implementazione.")
        codice_final = f"EQUIV-{amp}"

    # --- 3. DIFFERENZIALI PURI (5SV) ---
    elif categoria == "Differenziali Puri (5SV)":
        c1, c2 = st.columns(2)
        with c1:
            sens = st.selectbox("Sensibilità (IΔn)", ["30 mA (3)", "10 mA (1)", "300 mA (6)"])
            amp_d = st.selectbox("Corrente (In)", ["25 A", "40 A", "63 A", "16 A"])
        with c2:
            poli_d = st.radio("Poli", ["1P+N (1)", "3P+N (4)"])
            classe_d = st.selectbox("Classe", ["A (6)", "AC (0)", "F (3)", "B (4)"])
        codice_final = f"5SV3{sens[-2]}{poli_d[-2]}{amp_d[0]}-{classe_d[-2]}"

    # --- 4. MAGNETOTERMICI SCATOLATI (3VA) ---
    elif categoria == "Magnetotermici Scatolati (3VA)":
        c1, c2 = st.columns(2)
        with c1:
            taglia = st.selectbox("Taglia (Frame)", ["3VA10 (100A)", "3VA11 (160A)", "3VA12 (250A)"])
            f_code = taglia[3:5]
            pdi_va = st.selectbox("Potere Interruzione (415V)", ["25 kA (B)", "36 kA (C)", "55 kA (S)", "70 kA (M)"])
            p_va_code = pdi_va.split("(")[1][0]
        with c2:
            poli_va = st.selectbox("Poli", ["3 Poli", "4 Poli"])
            po_code = "3" if "3" in poli_va else "4"
            sganciatore = st.selectbox("Sganciatore", ["TM210 (Fisso)", "TM240 (Regolabile)"])
            s_code = "ED" if "210" in sganciatore else "EF"
            amp_va = st.selectbox("Corrente Nominale (In)", ["16", "25", "40", "63", "100", "160"])
        
        # Generazione codice radice 3VA
        codice_final = f"3VA1{f_code}-{p_va_code}EE{po_code}2-{s_code}0"

    # --- 5. ALTRE CATEGORIE ---
    else:
        st.info("Configurazione in fase di aggiornamento per Accessori e AFDD.")
        codice_final = "IN ELABORAZIONE"

with col_res:
    st.subheader("📌 Risultato")
    if "SIEMENS" in brand:
        st.success(f"### `{codice_final}`")
        st.caption("Codice d'ordinazione Siemens (Radice)")
    else:
        st.warning(f"Cercando equivalente {brand}...")
        st.info(f"Parametri selezionati per: {categoria}")

st.divider()
st.caption("Strumento di supporto tecnico - Verificare sempre sui cataloghi ufficiali Schneider/Siemens/ABB prima dell'ordine.")
