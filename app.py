import streamlit as st

# --- CONFIGURAZIONE PORTALE ---
st.set_page_config(page_title="SENTRON Selector Pro V9", layout="wide", page_icon="⚡")

# --- CSS PER LOOK PROFESSIONALE ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-box { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .pos-box { text-align:center; padding:5px; border:1px solid #015F73; border-radius:5px; background-color:white; min-width: 45px; }
    .pos-label { font-size: 10px; color: #666; font-weight: bold; }
    .pos-val { color:#015F73; font-size:18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IMPOSTAZIONI ---
st.sidebar.title("🛠️ System Settings")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Siemens-logo.svg", width=150)
st.sidebar.title("Configuratore Multibrand")
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS (Original)", "ABB (Equivalent)", "Schneider (Equivalent)"])
st.sidebar.divider()
st.sidebar.markdown("### Supporto Tecnico\nBasato su Tabelle POS 2024")

# --- TITOLO PRINCIPALE ---
st.title("🔌 Portale Tecnico Siemens SENTRON")
st.write(f"Configurazione attiva: **{brand}** | Rif. Documenti: **Tabelle POS.1-12**")

# --- SELEZIONE CATEGORIA ---
categoria = st.selectbox("Seleziona Categoria Prodotto", [
    "Magnetotermici (MCB)", 
    "Magnetotermici Differenziali (RCBO)", 
    "Differenziali Puri (RCCB)", 
    "Magnetotermici Scatolati (MCCB)"
])

st.divider()

col_params, col_res = st.columns([2, 1])

with col_params:
    st.subheader("🛠️ Specifiche Tecniche")
    codice_final = "N/D"
    
    # --- 1. MAGNETOTERMICI (MCB) - LOGICA TABELLE POS ---
    if categoria == "Magnetotermici (MCB)":
        c1, c2 = st.columns(2)
        with c1:
            # POS.4: PDI
            pdi = st.selectbox("Potere Interruzione (PDI)", ["4.5 kA (3)", "6 kA (6)", "10 kA (4)", "15 kA (7)", "70 kA (8)"])
            # POS.5: POLI
            poli = st.selectbox("Poli", ["1P (1)", "2P (2)", "3P (3)", "4P (4)", "1P+N 2UM (5)", "1P+N 1UM (0)"])
        with c2:
            # POS.6-7: AMPERE
            amp = st.selectbox("Corrente (In)", ["6A (06)", "10A (10)", "16A (16)", "40A (40)", "63A (63)"])
            # POS.8: CURVA
            curva = st.selectbox("Curva", ["A (5)", "B (6)", "C (7)", "D (8)", "Solo Mag (8BB08)"])
           
        if "SIEMENS" in brand:
            # Estrazione valori tra parentesi dalle selectbox
            pdi_val = pdi.split("(")[1][0]
            poli_val = poli.split("(")[1][0]
            amp_val = amp.split("(")[1].replace(")", "")
            curva_val = curva.split("(")[1].replace(")", "")

    # --- LOGICA ABB ---
                    
            # Costruzione MLFB Siemens (Esempio: 5S Y 6 1 7 16 KK)
            # Nota: La serie (POS.3) dipende dal PDI nella tua tabella
            serie_val = "L" if "4.5" in pdi or "6" in pdi else "Y"
            
            codice_final = f"5S{serie_val}{pdi_val}{poli_val}{amp_val}{curva_val}KK"

            # --- ANALISI POSIZIONI ---
            st.markdown("---")
            st.write("🔍 **Analisi Posizioni Codice MLFB (Tabella POS.1-12)**")
            
            # Visualizzazione a box per le posizioni principali
            pos_data = [
                ("1-2", "5S"), ("3", serie_val), ("4", pdi_val), 
                ("5", poli_val), ("6-7", amp_val), ("8", curva_val), ("9-10", "KK")
            ]
            p_cols = st.columns(len(pos_data))
            for idx, (label, val) in enumerate(pos_data):
                with p_cols[idx]:
                    st.markdown(f"""<div class="pos-box"><div class="pos-label">POS.{label}</div><div class="pos-val">{val}</div></div>""", unsafe_allow_html=True)
        else:
            codice_final = f"EQUIV-{brand[:3]}-{amp.split(' ')[0]}"

    # --- 2. ALTRE CATEGORIE (PLACEHOLDER) ---
    elif categoria == "Differenziali Puri (RCCB)":
        codice_final = "5SV3..."
    else:
        st.info("Logica in fase di caricamento per questa categoria.")

# --- COLONNA RISULTATO (DESTRA) ---
with col_res:
    st.subheader("📌 Risultato")
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    if codice_final != "N/D":
        st.success(f"### `{codice_final}`")
        st.caption(f"Codice identificativo per {brand}")
        st.divider()
        st.write("**Riepilogo:**")
        st.write(f"- Brand: {brand.split(' ')[0]}")
        st.write(f"- Categoria: {categoria}")
    else:
        st.warning("Configura i parametri a sinistra.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("Strumento basato su specifiche tecniche Siemens SENTRON. Verificare sempre sui cataloghi ufficiali.")
