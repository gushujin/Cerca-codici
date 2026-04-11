import streamlit as st

st.set_page_config(page_title="SENTRON Selector Pro V7", layout="wide")

# --- INTERFACCIA DI CONSULTAZIONE ---
st.title("⚡ Portale Tecnico Siemens SENTRON")
st.sidebar.header("Impostazioni Portale")
mode = st.sidebar.radio("Modalità", ["Configuratore Codici", "Cambio Produttore"])
brand_target = st.sidebar.selectbox("Produttore Alternativo", ["ABB", "Schneider", "Eaton"])

# --- SELEZIONE CATEGORIA ---
categoria = st.selectbox("Seleziona Categoria Prodotto", [
    "Magnetotermici (5SL, 5SY, 5SP)",
    "Magnetotermici Scatolati (3VA)",
    "Differenziali Puri (5SV)",
    "Magnetotermici Differenziali (5SU1/5SV1)",
    "Accessori (Contatti, Sganciatori)",
    "Compatti (AFDD 5SV6)"
])

st.divider()

col_input, col_output = st.columns([2, 1])

with col_input:
    if categoria == "Magnetotermici (5SL, 5SY, 5SP)":
        c1, c2 = st.columns(2)
        with c1:
            serie = st.selectbox("Serie / Potere Interruzione", ["5SL3 (4.5kA)", "5SL6 (6kA)", "5SY4 (10kA)", "5SY7 (15kA)", "5SP4 (Alto Amperaggio)"])
            poli = st.selectbox("Poli", ["1P (1)", "1P+N 1UM (0)", "1P+N 2UM (5)", "2P (2)", "3P (3)", "4P (4)"])
        with c2:
            amp = st.selectbox("Corrente (In)", ["06", "10", "13", "16", "20", "25", "32", "40", "50", "63", "80", "100"])
            curva = st.radio("Curva", ["B (6)", "C (7)", "D (8)"], horizontal=True)
        
        # Generazione Codice
        prefix = serie.split()[0]
        p_code = poli.split('(')[1][0]
        codice = f"{prefix}{p_code}{amp}-{curva[-2]}"

    elif categoria == "Differenziali Puri (5SV)":
        c1, c2 = st.columns(2)
        with c1:
            sens = st.selectbox("Sensibilità (IΔn)", ["30mA (3)", "10mA (1)", "300mA (6)", "500mA (7)"])
            in_d = st.selectbox("Corrente (In)", ["25A (2)", "40A (4)", "63A (6)", "80A (8)", "16A (1)"])
        with c2:
            poli_d = st.radio("Poli", ["1P+N (1)", "3P+N (4)"])
            tipo = st.selectbox("Tipo", ["A (6)", "AC (0)", "F (3)", "B (4)", "A-Selettivo (8)", "A-Immunizzato (6KK01)"])
        
        # Generazione Codice Rettificata
        t_val = tipo.split('(')[1][:-1]
        codice = f"5SV3{sens[-2]}{poli_d[-2]}{in_d[-2]}-{t_val}"

    elif categoria == "Magnetotermici Scatolati (3VA)":
        st.info("Configurazione 3VA1 (Termomagnetico) / 3VA2 (Elettronico)")
        grandezza = st.select_slider("Frame Size", options=["100", "160", "250", "400", "630"])
        codice = f"3VA11{grandezza[:2]}..."

with col_output:
    st.subheader("Risultato")
    st.markdown(f"### `{codice}`")
    
    if mode == "Cambio Produttore":
        st.warning(f"Equivalente {brand_target} in fase di elaborazione...")
        st.caption(f"Verifica serie {brand_target} con PDI e Poli selezionati.")

st.divider()
st.caption("Dati verificati secondo Catalogo Rapido SENTRON 10/2019")
