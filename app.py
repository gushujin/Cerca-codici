import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Configuratore Siemens", layout="wide")

@st.cache_data
def load_all_data():
    file_path = "Master_Data.xlsx"
    try:
        # Carichiamo i fogli (aggiunta gestione errore nomi fogli)
        df_map = pd.read_excel(file_path, sheet_name='Mapping')
        df_ambiti = pd.read_excel(file_path, sheet_name='Ambiti')
        
        # Pulizia: tutto in stringa e senza spazi ai bordi
        df_map = df_map.astype(str).apply(lambda x: x.str.strip())
        df_ambiti = df_ambiti.astype(str).apply(lambda x: x.str.strip())
        
        return df_map, df_ambiti
    except Exception as e:
        st.error(f"Errore caricamento Excel: {e}")
        return None, None

df_map, df_ambiti = load_all_data()

if df_map is not None:
    # --- SIDEBAR ---
    st.sidebar.header("Selezione Prodotto")
    brand_sel = st.sidebar.selectbox("Brand", df_ambiti['Brand'].unique())
    
    ambiti_disp = df_ambiti[df_ambiti['Brand'] == brand_sel]['Ambito_Utente'].unique()
    ambito_sel = st.sidebar.selectbox("Ambito Applicativo", ambiti_disp)
    
    famiglia_sel = df_ambiti[(df_ambiti['Brand'] == brand_sel) & 
                             (df_ambiti['Ambito_Utente'] == ambito_sel)]['Famiglia_Sistema'].values[0]

    st.title(f"Configuratore: {brand_sel} - {famiglia_sel}")
    st.markdown("---")

    # Filtriamo il mapping per la famiglia selezionata
    df_f = df_map[df_map['Famiglia'] == famiglia_sel]
    
    # --- INTERFACCIA SELEZIONE ---
    col1, col2, col3, col4 = st.columns(4)

    def get_options(param_name):
        opts = df_f[df_f['Parametro'] == param_name]['Valore_Reale'].unique()
        return sorted(opts)

    with col1: sel_poli = st.selectbox("Poli", get_options('Poli'))
    with col2: sel_pdi = st.selectbox("Pdi (kA)", get_options('Pdi'))
    with col3: sel_curva = st.selectbox("Curva", get_options('Curva'))
    with col4: sel_in = st.selectbox("Corrente (In)", get_options('Corrente'))

    # --- LOGICA DI GENERAZIONE ---
    def fetch_segment(param_name, valore_scelto):
        # Confronto super-flessibile: togliamo unità di misura e spazi
        def clean(v): return re.sub(r'[^a-zA-Z0-9+]', '', str(v)).upper()
        
        target = clean(valore_scelto)
        # Cerchiamo nella colonna Valore_Reale
        for _, row in df_f[df_f['Parametro'] == param_name].iterrows():
            if clean(row['Valore_Reale']) == target:
                return str(row['Segmento_Codice']), int(row['Posizione'])
        return "??", 99

    parti = []
    # 1. Prefisso (sempre presente)
    pref_row = df_f[df_f['Parametro'] == 'Prefisso']
    if not pref_row.empty:
        parti.append({"label": "Serie", "val": str(pref_row['Segmento_Codice'].values[0]), "pos": 1})

    # 2. Gli altri parametri
    for p_name, p_sel, p_label in [("Poli", sel_poli, "Poli"), 
                                   ("Pdi", sel_pdi, "PDI"), 
                                   ("Curva", sel_curva, "Curva"), 
                                   ("Corrente", sel_in, "Ampere")]:
        val, pos = fetch_segment(p_name, p_sel)
        parti.append({"label": p_label, "val": val, "pos": pos})

    # Ordiniamo e creiamo il codice
    parti.sort(key=lambda x: x['pos'])
    codice_generato = "".join([p['val'] for p in parti if p['val'] != "??"])

    # --- DISPLAY ---
    st.subheader("Risultato")
    cols = st.columns(len(parti))
    for i, p in enumerate(parti):
        cols[i].metric(p['label'], p['val'])

    if "??" in [x['val'] for x in parti]:
        st.error("Errore: Alcuni valori non hanno un corrispettivo nel Mapping Excel.")
    else:
        st.success(f"Codice Articolo Generato: **{codice_generato}**")
