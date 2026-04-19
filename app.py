import streamlit as st

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SENTRON Selector Pro V9", layout="wide", page_icon="⚡")

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
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS (Original)", "ABB (Equivalent)", "Schneider (Equivalent)"])

st.title("🔌 Portale Tecnico Multibrand")
categoria = st.selectbox("Seleziona Categoria", ["Magnetotermici (MCB)", "Differenziali"])

st.divider()

col_params, col_res = st.columns([2, 1])

with col_params:
    st.subheader("🛠️ Specifiche Tecniche")
    codice_final = "N/D"
    pos_data = [] # Inizializziamo la lista per evitare NameError

    if categoria == "Magnetotermici (MCB)":
        c1, c2 = st.columns(2)
        with c1:
            pdi = st.selectbox("Potere Interruzione (PDI)", ["6 kA (6)", "10 kA (4)", "15 kA (7)"])
            poli = st.selectbox("Poli", ["1P (1)", "2P (2)", "3P (3)", "4P (4)"])
        with c2:
            amp = st.selectbox("Corrente (In)", ["6A (06)", "10A (10)", "16A (16)", "32A (32)", "63A (63)"])
            curva = st.selectbox("Curva", ["B (6)", "C (7)", "D (8)"])

        # Estrazione dati base
        p_val = poli.split("(")[1][0]
        a_val = amp.split("(")[1].replace(")", "")
        c_val = curva.split("(")[1][0]

        # --- LOGICA SIEMENS ---
        if "SIEMENS" in brand:
            pdi_s = pdi.split("(")[1][0]
            serie = "5SL" if "6" in pdi else "5SY"
            codice_final = f"{serie}{pdi_s}{p_val}{a_val}-{c_val}{a_val}"
            pos_data = [("1-3", serie), ("4", pdi_s), ("5", p_val), ("6-7", a_val), ("8", "-"), ("10", c_val)]

        # --- LOGICA SCHNEIDER ---
        elif "Schneider" in brand:
            # Mappatura PDI Schneider dalla tua tabella
            pdi_sch = "64" if "6" in pdi else "74" if "10" in pdi else "84"
            codice_final = f"A9F{pdi_sch}{p_val}{a_val}"
            pos_data = [("1-3", "A9F"), ("4-5", pdi_sch), ("6", p_val), ("7-8", a_val)]

        # --- VISUALIZZAZIONE BOX (Se i dati esistono) ---
        if pos_data:
            st.markdown("---")
            st.write(f"🔍 **Analisi Posizioni Codice {brand.split(' ')[0]}**")
            p_cols = st.columns(len(pos_data))
            for i, (label, val) in enumerate(pos_data):
                with p_cols[i]:
                    st.markdown(f"""<div class="pos-box"><div class="pos-label">POS.{label}</div><div class="pos-val">{val}</div></div>""", unsafe_allow_html=True)

with col_res:
    st.subheader("📌 Risultato")
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    if codice_final != "N/D":
        st.success(f"### `{codice_final}`")
        st.write(f"**Configurazione:** {brand}")
    else:
        st.warning("Seleziona i parametri")
    st.markdown('</div>', unsafe_allow_html=True)
