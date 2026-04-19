import streamlit as st

# --- CONFIGURAZIONE PORTALE ---
st.set_page_config(page_title="SENTRON Selector Pro V9", layout="wide", page_icon="⚡")

# --- CSS PER LOOK PROFESSIONALE ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-box { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .pos-box { text-align:center; padding:5px; border:1px solid #015F73; border-radius:5px; background-color:white; min-width: 40px; }
    .pos-label { font-size: 10px; color: #666; }
    .pos-val { color:#015F73; font-size:18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IMPOSTAZIONI ---
st.sidebar.title("🛠️ System Settings")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Siemens-logo.svg", width=150)
st.sidebar.title("Configuratore Multibrand")
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS (Original)", "ABB (Equivalent)", "Schneider (Equivalent)"])
st.sidebar.divider()
st.sidebar.markdown("### Supporto Tecnico\nBasato su Catalogo SENTRON 2024")

# --- TITOLO PRINCIPALE ---
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
    codice_final = "" # Inizializzazione variabile
    
    # --- 1. MAGNETOTERMICI STANDARD ---
    if categoria.startswith("Magnetotermici (5SL"):
        c1, c2 = st.columns(2)
        with c1:
            pdi = st.selectbox("Potere Interruzione (Pos. 4)", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            poli_label = st.selectbox("Poli (Pos. 5)", ["1P", "1P+N (1UM)", "1P+N (2UM)", "2P", "3P", "3P+N", "4P"])
            p_map = {"1P": "1", "1P+N (1UM)": "0", "1P+N (2UM)": "5", "2P": "2", "3P": "3", "3P+N": "6", "4P": "4"}
        with c2:
            amp = st.selectbox("Corrente Nominale (Pos. 6-7)", ["06", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
            curva_label = st.radio("Curva (Pos. 10)", ["B", "C", "D"], horizontal=True)
            c_map = {"B": "5", "C": "7", "D": "8"}

        if "SIEMENS" in brand:
            # Determinazione Prefisso
            if "4.5" in pdi: pref = "5SL3"
            elif "6" in pdi: pref = "5SL6"
            elif "10" in pdi: pref = "5SL4"
            elif "15" in pdi: pref = "5SY7"
            else: pref = "5SY8"

            # Composizione MLFB
            codice_final = f"{pref}{p_map[poli_label]}{amp}-{c_map[curva_label]}{amp}"

            # --- ANALISI POSIZIONI (Grafica) ---
            st.markdown("---")
            st.write("🔍 **Analisi Posizioni Codice MLFB**")
            p_cols = st.columns(len(codice_final))
            for i, char in enumerate(codice_final):
                with p_cols[i]:
                    st.markdown(f"""<div class="pos-box"><div class="pos-label">P.{i+1}</div><div class="pos-val">{char}</div></div>""", unsafe_allow_html=True)
        else:
            codice_final = f"EQUIV-{brand[:3]}-{amp}"

    # --- 2. MAGNETOTERMICI DIFFERENZIALI ---
    elif categoria.startswith("Magnetotermici Differenziali"):
        tipo_md = st.radio("Scegli Modello", ["Standard (2 Moduli - 5SU1)", "Compatto (1 Modulo - 5SV1)"], horizontal=True)
        if tipo_md == "Compatto (1 Modulo - 5SV1)":
            c1, c2 = st.columns(2)
            with c1:
                pdi_sv = st.selectbox("Potere Interruzione", ["4.5 kA", "6 kA"])
                tipo_sv = st.radio("Classe", ["AC (Standard)", "A (Impulsiva)"])
            with c2:
                curva_sv = st.selectbox("Curva", ["B", "C"])
                amp_sv = st.selectbox("Ampere", ["06", "10", "13", "16", "20", "25", "32"])
            
            p_code = "3" if "4.5" in pdi_sv else "6"
            t_code = "3" if "AC" in tipo_sv else "6"
            codice_final = f"5SV1{t_code}1{p_code}-{curva_sv}{amp_sv}"
        else:
            codice_final = "5SU1..."

    # --- 3. DIFFERENZIALI PURI ---
    elif categoria.startswith("Differenziali Puri"):
        c1, c2 = st.columns(2)
        with c1:
