import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Configuratore Siemens", layout="wide")

# 2. CARICAMENTO DATI
@st.cache_data
def load_all_data():
    file_path = "Master_Data.xlsx"
    try:
        df_map = pd.read_excel(file_path, sheet_name='Mapping')
        df_ambiti = pd.read_excel(file_path, sheet_name='Ambiti')
        
        # Pulizia preventiva di tutti i testi nell'Excel
        for df in [df_map, df_ambiti]:
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.strip()
        return df_map, df_ambiti
    except Exception as e:
        st.error(f"Errore caricamento Excel: {e}")
        return None, None

df_map, df_ambiti = load_all_data()

if df_map is not None:
    # --- SIDEBAR: FILTRI ---
    st.sidebar.header("Selezione Prodotto")
    lista_brand = df_ambiti['Brand'].unique()
    brand_sel = st.sidebar.selectbox("Brand", lista_brand)
    
    ambiti_disp = df_ambiti[df_ambiti['Brand'] == brand_sel]['Ambito_Utente'].unique()
    ambito_sel = st.sidebar.selectbox("Ambito Applicativo", ambiti_disp)
    
    # Identifica la famiglia (es. 5SY, 5SL, 5SP)
    famiglia_sel = df_ambiti[(df_ambiti['Brand'] == brand_sel) & 
                             (df_ambiti['Ambito_Utente'] == ambito_sel)]['Famiglia_Sistema'].values[0]

    st.title(f"Configuratore: {brand_sel} - {famiglia_sel}")
    st.markdown("---")

    # --- UI: PARAMETRI TECNICI ---
    df_f = df_map[df_map['Famiglia'] == famiglia_sel]
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        opt_poli = sorted(df_f[df_f['Parametro'] == 'Poli']['Valore_Reale'].unique())
        sel_poli = st.selectbox("Poli", opt_poli)

    with col2:
        opt_pdi = sorted(df_f[df_f['Parametro'] == 'Pdi']['Valore_Reale'].unique())
        sel_pdi = st.selectbox("Potere Interruzione (Pdi)", opt_pdi)

    with col3:
        opt_curva = sorted(df_f[df_f['Parametro'] == 'Curva']['Valore_Reale'].unique())
        sel_curva = st.selectbox("Curva d'intervento", opt_curva)

    with col4:
        opt_in = sorted(df_f[df_f['Parametro'] == 'Corrente']['Valore_Reale'].unique())
        sel_in = st.selectbox("Corrente Nominale (In)", opt_in)

    # --- GENERAZIONE CODICE ARTICOLO (VERSIONE OTTIMIZZATA) ---
    def fetch_segment(param_name, valore_scelto):
        try:
            val_str = str(valore_scelto).strip()
            # Cerca la riga corrispondente pulendo eventuali spazi
            riga = df_f[(df_f['Parametro'] == param_name) & 
                        (df_f['Valore_Reale'].astype(str).str.strip() == val_str)]
            
            if not riga.empty:
                return str(riga['Segmento_Codice'].values[0]), riga['Posizione'].values[0]
            return "??", 99
        except:
            return "??", 99

    parti_codice = []
    
    # 1. Recupero Prefisso
    pref_row = df_f[df_f['Parametro'] == 'Prefisso']
    if not pref_row.empty:
        parti_codice.append({"val": str(pref_row['Segmento_Codice'].values[0]), "pos": 1, "label": "Serie"})

    # 2. Recupero Parametri Dinamici
    parti_codice.append({"val": fetch_segment("Poli", sel_poli)[0], "pos": fetch_segment("Poli", sel_poli)[1], "label": "Poli"})
    parti_codice.append({"val": fetch_segment("Pdi", sel_pdi)[0], "pos": fetch_segment("Pdi", sel_pdi)[1], "label": "PDI"})
    parti_codice.append({"val": fetch_segment("Curva", sel_curva)[0], "pos": fetch_segment("Curva", sel_curva)[1], "label": "Curva"})
    parti_codice.append({"val": fetch_segment("Corrente", sel_in)[0], "pos": fetch_segment("Corrente", sel_in)[1], "label": "Ampere"})

    # Ordinamento per posizione definita nell'Excel
    parti_codice.sort(key=lambda x: x['pos'])
    
    # Composizione stringa finale (ignora i pezzi non trovati ??)
    codice_finale = "".join([p['val'] for p in parti_codice if p['val'] != "??"])

    # --- DISPLAY RISULTATO ---
    st.markdown("### Risultato Configurazione")
    
    if "??" in [p['val'] for p in parti_codice]:
        st.warning("Attenzione: Alcuni segmenti non sono stati trovati nel Mapping. Verifica i nomi nell'Excel.")

    # Mostra i quadratini delle metriche
    res_cols = st.columns(len(parti_codice))
    for i, p in enumerate(parti_codice):
        res_cols[i].metric(p['label'], p['val'])

    st.success(f"Codice Articolo Siemens Generato: **{codice_finale}**")
