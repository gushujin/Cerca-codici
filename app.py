import streamlit as st

st.set_page_config(page_title="Siemens Specialist Configurator", layout="wide")
st.title("🛠️ Selettore Tecnico Siemens SENTRON V6")

# --- DATABASE INTEGRALE DAL PDF ---
mcb_data = {
    "4,5 kA (Serie 5SL3)": "5SL3",
    "6 kA (Serie 5SL6)": "5SL6",
    "10 kA (Serie 5SY4)": "5SY4",
    "15 kA (Serie 5SY7)": "5SY7",
    "25 kA (Serie 5SY8)": "5SY8"
}

tab_mcb, tab_rccb = st.tabs(["MAGNETOTERMICI", "DIFFERENZIALI PURI"])

with tab_mcb:
    st.subheader("Configurazione Interruttore Automatico")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        pot = st.selectbox("Potere Interruzione", list(mcb_data.keys()))
        prefisso_base = mcb_data[pot]
        
    with c2:
        poli = st.selectbox("Poli", ["1P", "1P+N (1 modulo)", "1P+N (2 moduli)", "2P", "3P", "3P+N", "4P"])
        # Logica poli specifica Siemens
        poli_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4", "1P+N (2 moduli)": "5", "3P+N": "6"}
        
    with c3:
        amp = st.selectbox("Corrente (In)", ["0.5", "1", "2", "3", "4", "6", "10", "13", "16", "20", "25", "32", "40", "50", "63"])
        a_code = amp.replace(".", "").zfill(2)
        
    with c4:
        curva = st.radio("Curva", ["B", "C", "D"])
        curva_map = {"B": "6", "C": "7", "D": "8"}

    # LOGICA DI COSTRUZIONE FINALE
    if poli == "1P+N (1 modulo)":
        codice = f"{prefisso_base[:4]}0{a_code}-{curva_map[curva]}"
    else:
        codice = f"{prefisso_base}{poli_map[poli]}{a_code}-{curva_map[curva]}"
    
    st.code(f"CODICE PRODOTTO: {codice}", language="markdown")

with tab_rccb:
    st.subheader("Configurazione Differenziale Puro 5SV")
    r1, r2, r3 = st.columns(3)
    with r1:
        tipo = st.selectbox("Classe", ["A (Impulsiva)", "AC (Sinusoidale)", "F (Inverter monofase)", "B (Universale CC)"])
        sens = st.selectbox("Sensibilità (IΔn)", ["30 mA", "10 mA", "300 mA", "500 mA"])
    with r2:
        poli_d = st.radio("Poli", ["1P+N", "3P+N"])
        in_d = st.selectbox("Corrente Nominale", ["25 A", "40 A", "63 A", "80 A", "16 A"])
    with r3:
        opt = st.multiselect("Esecuzioni Speciali", ["Superimmunizzato (K)", "Selettivo (S)"])

    # Logica differenziali
    t_map = {"A": "6", "AC": "0", "F": "3", "B": "4"}
    s_map = {"30 mA": "3", "10 mA": "1", "300 mA": "6", "500 mA": "7"}
    p_map = {"1P+N": "1", "3P+N": "4"}
    i_map = {"16 A": "1", "25 A": "2", "40 A": "4", "63 A": "6", "80 A": "8"}
    
    suff = ""
    if "Superimmunizzato (K)" in opt: suff = "KK01"
    
    codice_sv = f"5SV3{s_map[sens]}{p_map[poli_d]}{i_map[in_d]}-{t_map[tipo.split()[0]]}{suff}"
    st.code(f"CODICE PRODOTTO: {codice_sv}", language="markdown")
