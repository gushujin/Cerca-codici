import streamlit as st

# --- CONFIGURAZIONE PORTALE ---
st.set_page_config(page_title="SENTRON Selector Pro V9", layout="wide", page_icon="⚡")

# --- CSS LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-box { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .pos-box { text-align:center; padding:5px; border:1px solid #015F73; border-radius:5px; background-color:white; min-width: 45px; }
    .pos-label { font-size: 10px; color: #666; font-weight: bold; }
    .pos-val { color:#015F73; font-size:18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("🛠️ System Settings")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Siemens-logo.svg", width=150)
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS (Original)", "ABB (Equivalent)", "Schneider (Equivalent)"])

# --- TITOLO ---
st.title("🔌 Portale Tecnico Siemens SENTRON")
categoria = st.selectbox("Seleziona Categoria Prodotto", ["Magnetotermici (MCB)", "Differenziali Puri (RCCB)"])

st.divider()

col_params, col_res = st.columns([2, 1])

with col_params:
    st.subheader("🛠️ Specifiche Tecniche")
    codice_final = "N/D"
    
    if categoria == "Magnetotermici (MCB)":
        c1, c2 = st.columns(2)
        with c1:
            pdi = st.selectbox("Potere Interruzione (PDI)", ["4.5 kA (3)", "6 kA (6)", "10 kA (4)", "15 kA (7)"])
            poli = st.selectbox("Poli", ["1P (1)", "2P (2)", "3P (3)", "4P (4)"])
        with c2:
            amp = st.selectbox("Corrente (In)", ["6A (06)", "10A (10)", "16A (16)", "32A (32)", "63A (63)"])
            curva = st.selectbox("Curva", ["B (6)", "C (7)", "D (8)"])

        # Estrazione dati universali
        poli_val = poli.split("(")[1][0]
        amp_val = amp.split("(")[1].replace(")", "")
        curva_val = curva.split("(")[1][0]

        # --- LOGICA SIEMENS ---
        if "SIEMENS" in brand:
            pdi_val_siemens = pdi.split("(")[1][0]
            serie_val = "L" if "6" in pdi or "4.5" in pdi else "Y"
            codice_final = f"5S{serie_val}{pdi_val_siemens}{poli_val}{amp_val}-{curva_val}{amp_val}"
            
            st.markdown("---")
            st.write("🔍 **Analisi Posizioni Codice MLFB (Siemens)**")
            pos_data = [("1-2", "5S"), ("3", serie_val), ("4", pdi_val_siemens), ("5", poli_val), ("6-7", amp_val), ("8", "-"), ("10", curva_val)]
            
        # --- LOGICA SCHNEIDER ---
        elif "Schneider" in brand:
            # Mappatura PDI Schneider (64, 74, 84)
            pdi_sch = "64" if "6" in pdi else "74" if "10" in pdi else "84"
            codice_final = f"A9F{pdi_sch}{poli_val}{amp_val}"
            
            st.markdown("---")
            st.write("🔍 **Analisi Posizioni Codice Schneider (Acti9)**")
            pos_data = [("1-3", "A9F"), ("4-5", pdi_sch), ("6", poli_val), ("7-8", amp_val)]

        # --- RENDER BOX GRAFICI (Comune) ---
        if codice_final != "N/D":
            p_cols = st.columns(len(pos_data))
            for i, (label, val) in enumerate(pos_data):
                with p_cols[i]:
                    st.markdown(f"""<div class="pos-box"><div class="pos-label">POS.{label}</div><div class="pos-val">{val}</div></div>""", unsafe_allow_html=True)

# --- COLONNA RISULTATO ---
with col_res:
    st.subheader("📌 Risultato")
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    if codice_final != "N/D":
        st.success(f"### `{codice_final}`")
        st.write(f"**Brand:** {brand}")
    else:
        st.warning("Configura i parametri.")
    st.markdown('</div>', unsafe_allow_html=True)
