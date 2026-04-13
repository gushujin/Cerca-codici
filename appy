import streamlit as st

# Impostazione pagina larga
st.set_page_config(layout="wide")

st.title("Generatore Codici Siemens")

# Creazione delle 3 colonne
col1, col2, col3 = st.columns(3)

# Funzione per creare i blocchi (così non sbagliamo a scrivere 3 volte la stessa cosa)
def crea_configurazione(id_colonna):
    st.subheader(f"Configurazione {id_colonna}")
    prod = st.selectbox(f"Produttore", ["Siemens", "Altro"], key=f"p{id_colonna}")
    tipo = st.selectbox(f"Modello", ["S7-1200", "S7-1500", "ET200SP"], key=f"m{id_colonna}")
    
    if st.button(f"Genera Codice {id_colonna}", key=f"b{id_colonna}"):
        st.success("Codice Generato:")
        st.code(f"// Configurazione {prod}\n// Modello: {tipo}\nSTART_PLC();")

# Riempiamo le colonne
with col1:
    crea_configurazione(1)
with col2:
    crea_configurazione(2)
with col3:
    crea_configurazione(3)
