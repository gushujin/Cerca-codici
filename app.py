import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Configuratore Prodotti", layout="wide")

# 2. CARICAMENTO DATI (Cache per velocità)
@st.cache_data
def load_all_data():
    file_path = "Master_Data.xlsx"
    try:
        df_map = pd.read_excel(file_path, sheet_name='Mapping')
        df_black = pd.read_excel(file_path, sheet_name='Blacklist')
        df_ambiti = pd.read_excel(file_path, sheet_name='Ambiti')
        
        # Pulizia spazi bianchi accidentali
        for df in [df_map, df_black, df_ambiti]:
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.strip()
        return df_map, df_black, df_ambiti
    except Exception as e:
        st.error(f"Errore nel caricamento del file Excel: {e}")
        return None, None, None

df_map, df_black, df_ambiti = load_all_data()

if df_map is not None:
    # --- SIDEBAR: SELEZIONE BRAND E AMBITO ---
    st.sidebar.header("Filtri Principali")
    lista_brand = df_ambiti['Brand'].unique()
    brand_sel = st.sidebar.selectbox("Seleziona Brand", lista_brand)
    
    ambiti_disp = df_ambiti[df_ambiti['Brand'] == brand_sel]['Ambito_Utente'].unique()
    ambito_sel = st.sidebar.selectbox("Ambito", ambiti_disp)
    
    # Determina la Famiglia automaticamente
    famiglia_sel = df_ambiti[(df_ambiti['Brand'] == brand_sel) & 
                             (df_ambiti['Ambito_Utente'] == ambito_sel)]['Famiglia_Sistema'].values[0]

    st.title(f"Configuratore: {brand_sel} - {famiglia_sel}")
    st.markdown("---")

    # --- LOGICA FILTRO BLACKLIST ---
    def get_clean_options(param_name, all_options):
        esclusioni = df_black[(df_black['Famiglia'] == famiglia_sel) & 
                              (df_black['Parametro'] == param_name)]['Valore_da_Escludere'].astype(str).tolist()
        return [v for v in all_options if str(v) not in esclusioni]

    # --- UI: CARATTERISTICHE TECNICHE (DINAMICHE DA EXCEL) ---
    st.subheader("Parametri Tecnici")
    col1, col2, col3, col4 = st.columns(4)
    
    # Filtriamo il mapping per la famiglia corrente
    df_f = df_map[df_map['Famiglia'] == famiglia_sel]

    with col1:
        opt_poli = sorted(df_f[df_f['Parametro'] == 'Poli']['Valore_Reale'].unique())
        sel_poli = st.selectbox("Poli", get_clean_options("Poli", opt_poli))

    with col2:
        # Nota: Qui usiamo 'Pdi' perché è il nome che hai usato nell'ultima Legenda Excel
        opt_pdi = sorted(df_f[df_f['Parametro'] == 'Pdi']['Valore_Reale'].unique())
        sel_pdi = st.selectbox("Potere Interruzione", get_clean_options("Pdi", opt_pdi))

    with col3:
        opt_in = sorted(df_f[df_f['Parametro'] == 'Corrente']['Valore_Reale'].unique())
        sel_in = st.selectbox("Corrente (In)", get_clean_options("Corrente", opt_in))

    with col4:
        opt_curva = sorted(df_f[df_f['Parametro'] == 'Curva']['Valore_Reale'].unique())
        sel_curva = st.selectbox("Curva", get_clean_options("Curva", opt_curva))

    # --- GENERAZIONE CODICE ARTICOLO ---
    def fetch_segment(param, valore):
        try:
            res = df_f[(df_f['Parametro'] == param) & (df_f['Valore_Reale'].astype(str) == str(valore))]
            return str(res['Segmento_Codice'].values[0]), res['Posizione'].values[0]
        except:
            return "??", 99

    parti_codice = []
    
    # 1. Prefisso (sempre presente per famiglia)
    try:
        pref = df_f[df_f['Parametro'] == 'Prefisso']['Segmento_Codice'].values[0]
        parti_codice.append({"val": str(pref), "pos": 1, "label": "Serie"})
    except:
        parti_codice.append({"val": "ERR", "pos": 1, "label": "Serie"})

    # 2. Pezzi dinamici
    v_poli, p_poli = fetch_segment("Poli", sel_poli)
    parti_codice.append({"val": v_poli, "pos": p_poli, "label": "Poli"})
    
    v_in, p_in = fetch_segment("Corrente", sel_in)
    parti_codice.append({"val": v_in, "pos": p_in, "label": "Ampere"})

    # Ordinamento e composizione finale
    parti_codice.sort(key=lambda x: x['pos'])
    codice_finale = "".join([p['val'] for p in parti_codice])

    # --- DISPLAY RISULTATO ---
    st.markdown("### Risultato Configurazione")
    res_cols = st.columns(len(parti_codice))
    for i, p in enumerate(parti_codice):
        res_cols[i].metric(p['label'], p['val'])

    st.success(f"Codice Articolo Generato: **{codice_finale}**")
