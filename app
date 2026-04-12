import streamlit as st

# Titolo dell'applicazione
st.title("Generatore di Codice Tecnico")

# Creazione di 3 colonne affiancate
col1, col2, col3 = st.columns(3)

# Configurazione Colonna 1
with col1:
    st.header("Opzione 1")
    produttore_1 = st.selectbox("Scegli Produttore", ["Produttore A", "Produttore B"], key="p1")
    caratteristica_1 = st.selectbox("Caratteristica", ["Standard", "Premium", "Custom"], key="c1")
    if st.button("Genera Codice 1"):
        st.code(f"# Codice per {produttore_1}\n# Tipo: {caratteristica_1}")

# Configurazione Colonna 2
with col2:
    st.header("Opzione 2")
    produttore_2 = st.selectbox("Scegli Produttore", ["Produttore A", "Produttore B"], key="p2")
    caratteristica_2 = st.selectbox("Caratteristica", ["Standard", "Premium", "Custom"], key="c2")
    if st.button("Genera Codice 2"):
        st.code(f"# Codice per {produttore_2}\n# Tipo: {caratteristica_2}")

# Configurazione Colonna 3
with col3:
    st.header("Opzione 3")
    produttore_3 = st.selectbox("Scegli Produttore", ["Produttore A", "Produttore B"], key="p3")
    caratteristica_3 = st.selectbox("Caratteristica", ["Standard", "Premium", "Custom"], key="c3")
    if st.button("Genera Codice 3"):
        st.code(f"# Codice per {produttore_3}\n# Tipo: {caratteristica_3}")
