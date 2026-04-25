import streamlit as st
import pandas as pd

st.set_page_config(page_title="Configuratore Siemens", layout="wide")

@st.cache_data
def load_all_data():
    file_path = "Master_Data.xlsx"
    try:
        # Carichiamo i fogli
        df_map = pd.read_excel(file_path, sheet_name='Mapping')
        df_ambiti = pd.read_excel(file_path, sheet_name='Ambiti')
        
        # Pulizia totale spazi bianchi ovunque
        df_map = df_map.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df_ambiti = df_ambiti.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df_map, df_ambiti
    except Exception as e:
        st.error(f"Errore caricamento Excel: {e}")
        return None, None

df_map, df_ambiti = load_all_data()

if df_map is not None:
    st.sidebar.header("Selezione Prodotto")
    brand_sel = st.sidebar.selectbox("Brand", df_ambiti['Brand'].unique())
    
    ambiti_disp = df_ambiti[df_ambiti['Brand'] == brand_sel]['Ambito_Utente'].unique()
    ambito_sel = st.sidebar.selectbox("Ambito Applicativo", ambiti_disp)
    
    famiglia_sel = df_ambiti[(df_ambiti['Brand'] == brand_sel) & 
                             (df_ambiti['Ambito_Utente'] == ambito_sel)]['Famiglia_Sistema'].values[0]

    st.title(f"Configuratore: {brand_sel} - {famiglia_sel}")
    st.markdown("---")

    df_f = df_map[df_map['Famiglia'] == famiglia_sel]
    
    # --- INTERFACCIA SELEZIONE ---
    col1, col2, col3, col4 = st.columns(4)

    # Funzione di supporto per evitare crash se il parametro non esiste nell'Excel
    def get_options(param_name):
        return sorted(df_f[df_f['Parametro'] == param_name]['Valore_Reale'].unique())

    with col1:
        sel_poli = st.selectbox("Poli", get_options('Poli'))
    with col2:
        sel_pdi = st.selectbox("Pdi (kA)", get_options('Pdi'))
    with col3:
        sel_curva = st.selectbox("Curva", get_options('Curva'))
    with col4:
        sel_in = st.selectbox("Corrente (In)", get_options('Corrente'))

    # --- LOGICA DI COSTRUZIONE CODICE ---
    def fetch_segment(param_name, valore_scelto):
        riga = df_f[(df_f['Parametro'] == param_name) & 
                    (df_f['Valore_Reale'].astype(str) == str(valore_scelto))]
        if not riga.empty:
            return str(riga['Segmento_Codice'].values[0]), riga['Posizione'].values[0]
        return "??", 99

    parti = []
    # Aggiungiamo i pezzi
    parti.append({"label": "Serie", "val": fetch_segment("Prefisso", "Universale")[0], "pos": 1})
    parti.append({"label": "Poli", "val": fetch_segment("Poli", sel_poli)[0], "pos": fetch_segment("Poli", sel_poli)[1]})
    parti.append({"label": "PDI", "val": fetch_segment("Pdi", sel_pdi)[0], "pos": fetch_segment("Pdi", sel_pdi)[1]})
    parti.append({"label": "Curva", "val": fetch_segment("Curva", sel_curva)[0], "pos": fetch_segment("Curva", sel_curva)[1]})
    parti.append({"label": "Ampere", "val": fetch_segment("Corrente", sel_in)[0], "pos": fetch_segment("Corrente", sel_in)[1]})

    # Ordiniamo per posizione
    parti.sort(key=lambda x: x['pos'])
    
    # Generazione stringa finale
    codice_generato = "".join([p['val'] for p in parti if p['val'] != "??"])

    # --- DISPLAY ---
    st.subheader("Risultato")
    res_cols = st.columns(len(parti))
    for i, p in enumerate(parti):
        res_cols[i].metric(p['label'], p['val'])

    if len(codice_generato) < 5: # Lunghezza minima indicativa
        st.error("Errore: Il mapping non è completo per questa combinazione.")
    else:
        st.success(f"Codice Articolo: **{codice_generato}**")
