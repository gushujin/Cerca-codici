import streamlit as st

st.set_page_config(page_title="Siemens Code Finder", page_icon="⚡")

st.title("⚡ Configuratore Codici Siemens SENTRON")
st.markdown("Strumento basato sul Catalogo Rapido 2019 per l'identificazione dei componenti.")

# Sidebar per la scelta principale
categoria = st.sidebar.selectbox(
    "Seleziona Categoria",
    ["Magnetotermici (5SY)", "Differenziali Puri (5SV)", "Antincendio (5SV6)"]
)

st.divider()

if categoria == "Magnetotermici (5SY)":
    st.subheader("Configurazione Serie 5SY")
    col1, col2 = st.columns(2)
    with col1:
        potere = st.selectbox("Potere di interruzione", ["4 (10kA)", "7 (15kA)"])
        poli = st.selectbox("Poli", ["1 (1P)", "2 (2P)", "5 (1P+N)", "4 (4P)", "6 (3P+N)"])
    with col2:
        ampere = st.text_input("Corrente Nominale (es. 06, 10, 16, 32)", value="16")
        curva = st.selectbox("Curva di intervento", ["6 (B)", "7 (C)", "8 (D)"])
    
    codice = f"5SY{potere[0]}{poli[0]}{ampere}-{curva[0]}"
    st.info(f"**Codice Identificato:** {codice}")

elif categoria == "Differenziali Puri (5SV)":
    st.subheader("Configurazione Serie 5SV")
    c1, c2, c3 = st.columns(3)
    with c1:
        esec = st.selectbox("Esecuzione", ["3 (Top)", "4 (Standard)", "5 (Residenziale)"])
        sens = st.selectbox("Sensibilità (IΔn)", ["1 (10mA)", "3 (30mA)", "6 (300mA)"])
    with c2:
        poli = st.selectbox("Poli", ["1 (1P+N)", "4 (3P+N)"])
        amp = st.selectbox("Corrente (In)", ["2 (25A)", "4 (40A)", "6 (63A)"])
    with c3:
        tipo = st.selectbox("Classe/Tipo", ["0 (AC)", "6 (A)", "3 (F)", "4 (B)"])
    
    codice = f"5SV{esec[0]}{sens[0]}{poli[0]}{amp[0]}-{tipo[0]}"
    st.info(f"**Codice Identificato:** {codice}")

elif categoria == "Antincendio (5SV6)":
    st.subheader("Configurazione Serie 5SV6 (AFDD)")
    amp = st.select_slider("Corrente Nominale (A)", options=["10", "13", "16", "20", "25", "32", "40"])
    curva = st.radio("Curva Magnetotermica", ["B", "C"], horizontal=True)
    
    codice = f"5SV6016-{curva}{amp}"
    st.info(f"**Codice Identificato:** {codice}")

st.success("Codice pronto per l'ordine nel catalogo Siemens.")
