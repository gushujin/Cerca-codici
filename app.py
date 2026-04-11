import streamlit as st

st.set_page_config(page_title="Siemens Code Generator 33_CF", layout="wide")
st.title("⚡ Generatore Codici Siemens SENTRON (Ver. 33_CF)")

menu = st.sidebar.radio("Seleziona Prodotto", ["Magnetotermici (MCB)", "Differenziali (RCCB)"])

if menu == "Magnetotermici (MCB)":
    st.header("Configurazione MCB (5SL / 5SY)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        p_int = st.selectbox("Potere di Interruzione", ["4.5kA (5SL3)", "6kA (5SL6)", "10kA (5SY4/5SL4)", "15kA (5SY7)", "25kA (5SY8)"])
        radice = p_int.split('(')[1][:4]
        poli = st.selectbox("Poli", ["1P", "1P+N (1 modulo)", "1P+N (2 moduli)", "2P", "3P", "3P+N", "4P"])
        
    with col2:
        amp = st.selectbox("Corrente Nominale (In)", ["06", "10", "13", "16", "20", "25", "32", "40", "50", "63", "01", "02", "04", "05"])
        curva = st.radio("Curva di Intervento", ["B", "C", "D"])
        curva_map = {"B": "6", "C": "7", "D": "8"}

    # Logica Poli basata su pag. 1 del file 33_CF
    poli_map = {"1P": "1", "1P+N (1 modulo)": "0", "1P+N (2 moduli)": "5", "2P": "2", "3P": "3", "3P+N": "6", "4P": "4"}
    
    # Costruzione Codice
    codice_finale = f"{radice}{poli_map[poli]}{amp}-{curva_map[curva]}"
    st.info(f"**CODICE IDENTIFICATO:** {codice_finale}")

else:
    st.header("Configurazione Differenziali Puri (5SV)")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        tipo = st.selectbox("Classe", ["AC", "A", "A-Selettivo", "A-Immunizzato (AK)", "F", "B"])
        sens = st.selectbox("Sensibilità (IΔn)", ["10mA", "30mA", "300mA", "500mA"])
    with c2:
        poli_sv = st.radio("Poli", ["1P+N", "3P+N"])
        in_sv = st.selectbox("Corrente (In)", ["16A", "25A", "40A", "63A", "80A"])
    
    # Mappatura secondo pag. 2 del file 33_CF
    s_map = {"10mA": "1", "30mA": "3", "300mA": "6", "500mA": "7"}
    p_map = {"1P+N": "1", "3P+N": "4"}
    i_map = {"16A": "1", "25A": "2", "40A": "4", "63A": "6", "80A": "8"}
    t_map = {"AC": "-0", "A": "-6", "A-Selettivo": "-8", "A-Immunizzato (AK)": "-6KK01", "F": "-3", "B": "-4"}
    
    codice_sv = f"5SV3{s_map[sens]}{p_map[poli_sv]}{i_map[in_sv]}{t_map[tipo]}"
    st.info(f"**CODICE IDENTIFICATO:** {codice_sv}")

st.success("Analisi completata con successo secondo il documento 33_CF.")
