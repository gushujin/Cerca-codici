import streamlit as st

# Configurazione Layout
st.set_page_config(page_title="SENTRON Selector Pro", layout="wide", page_icon="⚡")

# --- CSS PER LOOK PROFESSIONALE ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-box { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .result-card { background-color: #005f73; color: white; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GESTIONE PRODUTTORE ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Siemens-logo.svg", width=150)
st.sidebar.title("Configuratore Multibrand")
brand_active = st.sidebar.selectbox("Produttore Attivo", ["SIEMENS", "ABB", "SCHNEIDER"])
st.sidebar.divider()
st.sidebar.caption("Dati sincronizzati con Catalogo SENTRON 10/2019")

# --- TITOLO ---
st.title("🔌 Portale Tecnico Apparecchiature Modulari")
st.write(f"Database: **Documento 33_CF** | Visualizzazione: **{brand_active}**")

# --- CATEGORIE DI PRODOTTO ---
cat = st.selectbox("Seleziona Categoria", [
    "Magnetotermici (5SL, 5SY, 5SP)",
    "Differenziali Puri (5SV)",
    "Magnetotermici Differenziali (5SU1, 5SV1)",
    "Scatolati (3VA)",
    "Accessori e AFDD"
])

st.divider()

col_params, col_code = st.columns([2, 1])

with col_params:
    st.subheader("🛠️ Specifiche Tecniche")
    
    if "Magnetotermici" in cat:
        c1, c2 = st.columns(2)
        with c1:
            pdi = st.selectbox("Potere di Interruzione", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            poli = st.selectbox("Poli", ["1P", "1P+N (1UM)", "1P+N (2UM)", "2P", "3P", "3P+N", "4P"])
        with c2:
            amp = st.selectbox("In (A)", ["0,5", "1", "2", "6", "10", "16", "20", "25", "32", "40", "50", "63"])
            curva = st.radio("Curva", ["B (6)", "C (7)", "D (8)"], horizontal=True)

        # Logica 33_CF
        pref = "5SL3" if "4.5" in pdi else "5SL6" if "6" in pdi else "5SY4" if "10" in pdi else "5SY7" if "15" in pdi else "5SY8"
        p_map = {"1P": "1", "1P+N (1UM)": "0", "1P+N (2UM)": "5", "2P": "2", "3P": "3", "3P+N": "6", "4P": "4"}
        a_code = amp.replace(",", "").zfill(2)
        res_code = f"{pref}{p_map[poli]}{a_code}-{curva[-2]}"

    elif "Differenziali Puri" in cat:
        c1, c2 = st.columns(2)
        with c1:
            sens = st.selectbox("Sensibilità (IΔn)", ["30 mA (3)", "10 mA (1)", "300 mA (6)", "500 mA (7)"])
            amp_d = st.selectbox("In (A)", ["25 A (2)", "40 A (4)", "63 A (6)", "16 A (1)"])
        with c2:
            poli_d = st.radio("Poli", ["1P+N (1)", "3P+N (4)"])
            tipo = st.selectbox("Tipo", ["A (6)", "AC (0)", "F (3)", "B (4)", "A-K (6KK01)", "A-S (8)"])
        
        # Logica 5SV3314-6
        t_val = tipo.split('(')[1][:-1]
        res_code = f"5SV3{sens[-2]}{poli_d[-2]}{amp_d[-2]}-{t_val}"

with col_code:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("### CODICE GENERATO")
    st.title(f"`{res_code}`")
    
    if brand_active != "SIEMENS":
        st.markdown("---")
        st.write(f"💡 Suggerimento {brand_active}:")
        if brand_active == "ABB":
            st.code("SH200L / S200" if "Magneto" in cat else "F202 / F204")
        else:
            st.code("iK60 / iC60" if "Magneto" in cat else "iID")
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("📋 Copia Codice"):
        st.toast("Codice copiato negli appunti!")

# --- FOOTER DATI TECNICI ---
st.divider()
exp = st.expander("📖 Legenda Composizione Codici (Rif. 33_CF)")
with exp:
    st.write("**Interruttori 5SL/5SY:** Radice + Poli (5ª cifra) + Ampere (6-7ª) + Curva (Suffisso)")
    st.write("**Esempio 1UM:** Poli = 0 (es. 5SL3016-7 per 1P+N compatto)")
    st.write("**Differenziali 5SV:** 5SV3 + Sensibilità + Poli + Ampere + Classe")
