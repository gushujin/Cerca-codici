import streamlit as st
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Configuratore Elettrico", layout="wide")

# Funzione per caricare i dati (Carica da GitHub o locale)
@st.cache_data
def load_data():
    # Sostituire con il link 'raw' di GitHub una volta caricato
    file_path = "Master_Data.xlsx" 
    df_map = pd.read_excel(file_path, sheet_name='Mapping')
    df_black = pd.read_excel(file_path, sheet_name='Blacklist')
    return df_map, df_black

try:
    df_map, df_black = load_data()

    st.title("⚡ Reverse Engineering Part Number")
    st.markdown("---")

    # --- SIDEBAR: FILTRI INIZIALI ---
    st.sidebar.header("Impostazioni Base")
    brand = st.sidebar.selectbox("Seleziona Brand", df_map['Brand'].unique())
    ambito = st.sidebar.selectbox("Ambito Applicativo", ["Residenziale", "Industriale"])

    # Logica per determinare la Famiglia (esempio semplificato)
    if ambito == "Residenziale":
        famiglia = "Resi9" if brand == "Schneider" else "Serie_Res"
    else:
        famiglia = "iC60N" if brand == "Schneider" else "Serie_Ind"

    st.sidebar.info(f"Famiglia identificata: **{famiglia}**")

    # --- LOGICA A SOTTRAZIONE ---
    def get_filtered_options(parametro, lista_universale):
        blacklist = df_black[(df_black['Famiglia'] == famiglia) & 
                             (df_black['Parametro_da_Escludere'] == parametro)]['Valore_da_Nascondere'].tolist()
        return [opt for opt in lista_universale if opt not in blacklist]

    # Liste Master (Universali)
    master_poli = ["1P", "1P+N", "2P", "3P", "4P"]
    master_ka = ["4.5kA", "6kA", "10kA", "15kA", "25kA"]
    master_in = ["6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
    master_curve = ["B", "C", "D"]

    # Menu filtrati
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sel_poli = st.selectbox("Poli", get_filtered_options("Poli", master_poli))
    with col2:
        sel_ka = st.selectbox("Potere Interruzione", get_filtered_options("Potere_Interruzione", master_ka))
    with col3:
        sel_in = st.selectbox("Corrente Nominale (In)", get_filtered_options("Corrente", master_in))
    with col4:
        sel_curva = st.selectbox("Curva", get_filtered_options("Curva", master_curve))

    # --- COMPOSIZIONE CODICE ---
    # Cerchiamo i pezzi di codice nel mapping
    mask = (df_map['Brand'] == brand) & (df_map['Famiglia'] == famiglia)
    mapping_f = df_map[mask].sort_values('Posizione')

    # Costruiamo il dizionario dei risultati
    code_segments = []
    
    # Prefisso (Posizione 1)
    prefisso = mapping_f[mapping_f['Parametro'] == 'Prefisso']['Segmento_Codice'].values[0]
    code_segments.append({"val": str(prefisso), "desc": "Famiglia"})

    # Poli (Posizione 2) - Esempio di ricerca valore specifico
    val_poli = mapping_f[(mapping_f['Parametro'] == 'Poli') & (mapping_f['Valore_Reale'] == sel_poli)]['Segmento_Codice'].values[0]
    code_segments.append({"val": str(val_poli), "desc": "Poli"})

    # Corrente (Posizione 3)
    val_in = mapping_f[(mapping_f['Parametro'] == 'Corrente') & (mapping_f['Valore_Reale'] == sel_in)]['Segmento_Codice'].values[0]
    code_segments.append({"val": str(val_in), "desc": "Amperaggio"})

    full_code = "".join([s['val'] for s in code_segments])

    # --- UI: CODE VISUALIZER ---
    st.subheader("Codice Prodotto Generato")
    cols_code = st.columns(len(code_segments))
    for i, seg in enumerate(code_segments):
        with cols_code[i]:
            st.metric(label=seg['desc'], value=seg['val'])

    st.success(f"**Codice Finale: {full_code}**")

    # --- ACTION BUTTONS ---
    url_base = mapping_f['URL_Base'].iloc[0]
    final_url = f"{url_base}{full_code}"
    
    c1, c2 = st.columns(2)
    with c1:
        st.link_button(f"🔍 Verifica su sito {brand}", final_url)
    with c2:
        st.button("📄 Scarica Datasheet (PDF)")

except Exception as e:
    st.error(f"Carica il file 'Master_Data.xlsx' per iniziare. Errore: {e}")
