import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Configuratore Elettrotecnico", layout="wide")

# 2. FUNZIONE CARICAMENTO DATI
@st.cache_data
def load_data():
    """Carica i fogli di lavoro dal file Excel Master."""
    file_path = "Master_Data.xlsx" 
    try:
        # Carichiamo i tre fogli fondamentali
        Mapping = pd.read_excel(file_path, sheet_name='Mapping')
        Blacklist = pd.read_excel(file_path, sheet_name='Blacklist')
        # Il foglio 'Ambito' associa Brand + Scelta Utente alla Famiglia prodotto
        Ambiti = pd.read_excel(file_path, sheet_name='Ambiti')
        return Mapping, Blacklist, Ambiti
    except Exception as e:
        st.error(f"Errore nel caricamento del file Excel: {e}")
        return None, None, None

df_map, df_Black, df_Ambiti = load_data()

if df_map is not None:
    # --- UI: HEADER ---
    st.title("⚡ Reverse Engineering Prodotto")
    st.info("Parti dalle caratteristiche tecniche per generare il codice articolo corretto.")

    # --- SIDEBAR: LE SCELTE DELL'UTENTE ---
    st.sidebar.header("1. Contesto")
    brand_scelto = st.sidebar.selectbox("Seleziona il Brand", df_map['Brand'].unique())
    
    # Filtriamo gli ambiti disponibili per quel Brand specifico
    Ambiti_disponibili = df_Ambiti[df_Ambiti['Brand'] == brand_scelto]['Ambito_Utente'].unique()
    Ambito_scelto = st.sidebar.selectbox("Campo Applicativo", Ambiti_disponibili)

    # Identifichiamo la Famiglia di sistema in base alle scelte
    famiglia_selezionata = df_Ambiti[(df_Ambiti['Brand'] == brand_scelto) & 
                                     (df_Ambiti['Ambito_Utente'] == Ambito_scelto)]['Famiglia_Sistema'].values[0]

    st.sidebar.markdown(f"**Famiglia Corrente:** `{famiglia_selezionata}`")
    st.sidebar.markdown("---")

    # --- LOGICA A SOTTRAZIONE (PULIZIA MENU) ---
    def filter_menu(parametro, lista_master):
        """Nasconde i valori presenti nella Blacklist per la famiglia corrente."""
        esclusioni = df_Black[(df_Black['Famiglia'] == famiglia_selezionata) & 
                              (df_Black['Parametro'] == parametro)]['Valore_da_Escludere'].tolist()
        # Convertiamo tutto in stringa per il confronto
        esclusioni = [str(e) for e in esclusioni]
        return [opt for opt in lista_master if str(opt) not in esclusioni]

    # Liste Master Universali (possono essere spostate in un foglio Excel dedicato in futuro)
    master_poli = ["1P", "1P+N", "2P", "3P", "4P"]
    master_ka = ["4.5kA", "6kA", "10kA", "15kA", "20kA", "25kA", "36kA"]
    master_in = ["6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
    master_curve = ["B", "C", "D", "K", "Z"]

    # --- UI: CONFIGURAZIONE TECNICA ---
    st.subheader("2. Caratteristiche Tecniche")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        sel_poli = st.selectbox("Poli", filter_menu("Poli", master_poli))
    with col2:
        sel_ka = st.selectbox("Potere Interruzione", filter_menu("Potere_Interruzione", master_ka))
    with col3:
        sel_in = st.selectbox("Corrente Nominale (In)", filter_menu("Corrente", master_in))
    with col4:
        sel_curva = st.selectbox("Curva intervento", filter_menu("Curva", master_curve))

    # --- LOGICA DI COMPOSIZIONE CODICE (MAPPING) ---
    st.markdown("---")
    
    # Filtriamo il mapping per la famiglia attiva
    map_famiglia = df_map[df_map['Famiglia'] == famiglia_selezionata]

    def get_segment(parametro, valore_reale):
        """Trova il pezzo di codice corrispondente al valore tecnico scelto."""
        try:
            res = map_famiglia[(map_famiglia['Parametro'] == parametro) & 
                               (map_famiglia['Valore_Reale'].astype(str) == str(valore_reale))]
            return res['Segmento_Codice'].values[0], res['Posizione'].values[0]
        except:
            return "??", 99

    # Costruiamo i blocchi del codice
    blocchi = []
    
    # Aggiungiamo il Prefisso fisso della famiglia (Posizione 1)
    prefisso_val = map_famiglia[map_famiglia['Parametro'] == 'Prefisso']['Segmento_Codice'].values[0]
    blocchi.append({"testo": str(prefisso_val), "label": "Serie", "pos": 1})

    # Aggiungiamo i parametri variabili (Poli, Corrente...)
    seg_poli, pos_poli = get_segment("Poli", sel_poli)
    blocchi.append({"testo": str(seg_poli), "label": "Poli", "pos": pos_poli})

    seg_in, pos_in = get_segment("Corrente", sel_in)
    blocchi.append({"testo": str(seg_in), "label": "Ampere", "pos": pos_in})

    # Ordiniamo per posizione definita nell'Excel
    blocchi_ordinati = sorted(blocchi, key=lambda x: x['pos'])
    codice_finale = "".join([b['testo'] for b in blocchi_ordinati])

    # --- UI: CODE VISUALIZER (CASSETTE GRAFICHE) ---
    st.subheader("3. Codice Risultante")
    
    # Creiamo tante colonne quanti sono i blocchi
    grid = st.columns(len(blocchi_ordinati))
    for i, b in enumerate(blocchi_ordinati):
        with grid[i]:
            st.metric(label=b['label'], value=b['testo'])

    # Visualizzazione codice completo
    st.code(codice_finale, language="text")

    # --- UI: AZIONI E LINK ---
    url_base = map_famiglia['URL_Base'].iloc[0]
    full_url = f"{url_base}{codice_finale}"

    c1, c2 = st.columns(2)
    with c1:
        st.link_button(f"🌐 Verifica sul sito {brand_scelto}", full_url)
    with c2:
        st.button("📄 Scarica Scheda Tecnica (PDF)")

else:
    st.warning("Assicurati che il file 'Master_Data.xlsx' sia presente nella stessa cartella dello script.")
