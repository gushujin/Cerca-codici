import streamlit as st

st.set_page_config(page_title="Siemens SENTRON Full Configurator", layout="wide")

st.title("⚡ Configuratore Siemens SENTRON - Dati Completi")
st.write("Integrazione serie 4,5kA / 6kA / 10kA / 15kA e Differenziali")

# --- DATABASE LOGICO ESTRATTO DALLE IMMAGINI ---
# Mappa: (Potere, Moduli) -> Prefisso
SERIE_MAP = {
    ("4,5 kA", "Compatto (1 Modulo)"): "5SL30",
    ("4,5 kA", "Standard (2 Moduli)"): "5SL35", # Per 1P+N
    ("6 kA", "Compatto (1 Modulo)"): "5SL60",
    ("6 kA", "Standard (2 Moduli)"): "5SL65",  # Per 1P+N
    ("10 kA", "Standard"): "5SY4",
    ("15 kA", "Standard"): "5SY7"
}

tab_mcb, tab_rccb, tab_afdd = st.tabs(["Magnetotermici", "Differenziali Puri", "Antincendio"])

with tab_mcb:
    st.subheader("Configurazione Interruttori Magnetotermici")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        potere = st.selectbox("Potere di Interruzione (Icn)", ["4,5 kA", "6 kA", "10 kA", "15 kA"])
        tipo_ingombro = st.radio("Ingombro", ["Compatto (1 Modulo)", "Standard (2 Moduli)"]) if potere in ["4,5 kA", "6 kA"] else "Standard"
        poli = st.selectbox("Poli", ["1P+N", "2P", "3P", "4P"])
    
    with col2:
        # Range correnti completo da catalogo
        ampere = st.selectbox("In (A)", ["02", "04", "06", "08", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
        curva = st.radio("Curva", ["B", "C", "D"])
        c_code = "6" if curva == "B" else "7" if curva == "C" else "8"

    with col3:
        # Logica di generazione prefisso dinamica
        if "SY" in (pref := SERIE_MAP.get((potere, tipo_ingombro), "5SY4")):
            p_code = {"1P+N": "5", "2P": "2", "3P": "3", "4P": "4"}[poli]
            codice = f"{pref}{p_code}{ampere}-{c_code}"
        else:
            # Per serie 5SL (4.5/6kA)
            pref_sl = SERIE_MAP.get((potere, tipo_ingombro))
            codice = f"{pref_sl}{ampere}-{c_code}"
            
        st.info(f"**Codice Siemens Identificato:** \n# {codice}")

with tab_rccb:
    st.subheader("Differenziali Puri 5SV")
    c1, c2 = st.columns(2)
    with c1:
        tipo_diff = st.selectbox("Tipo", ["AC (Standard)", "A (Impulsiva)", "F (Frequenza)", "B (Universale)"])
        sensibilita = st.selectbox("IΔn", ["30 mA", "300 mA"])
        s_code = sensibilita[0] # Prende '3' o '6'
    with c2:
        in_diff = st.selectbox("In (A)", ["25A", "40A", "63A", "80A"])
        a_code = {"25A": "2", "40A": "4", "63A": "6", "80A": "8"}[in_diff]
        poli_diff = st.radio("Poli", ["1P+N (1)", "3P+N (4)"])
        
    tipo_code = {"AC": "0", "A": "6", "F": "3", "B": "4"}[tipo_diff[:2].strip()]
    codice_sv = f"5SV3{s_code}{poli_diff[-2]}{a_code}-{tipo_code}"
    st.info(f"**Codice 5SV:** \n# {codice_sv}")

with tab_afdd:
    st.subheader("Protezione Antincendio 5SV6")
    a_af = st.selectbox("Corrente", ["06", "10", "13", "16", "20", "25", "32", "40"], index=3)
    curva_af = st.radio("Curva", ["B", "C"], index=1)
    st.info(f"**Codice 5SV6 (6kA):** \n# 5SV6016-{curva_af}{a_af}")
