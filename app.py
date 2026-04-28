import pandas as pd
import streamlit as st

# --- CARICAMENTO DATI (Da inserire all'inizio o in una funzione cache) ---
@st.cache_data
def load_schneider_data(file_path):
    # Legge tutte le tabelle tranne 'Legenda'
    xl = pd.ExcelFile(file_path)
    sheets = [sheet for sheet in xl.sheet_names if sheet != "Legenda"]
    df_list = [xl.parse(s) for s in sheets]
    return pd.concat(df_list, ignore_index=True)

# Supponiamo che il file sia già caricato come 'df_schneider'
# df_schneider = load_schneider_data("tuo_file.xlsx")

# --- LOGICA SCHNEIDER DINAMICA ---
elif brand == "SCHNEIDER" and is_mcb:
    st.subheader("Configuratore Schneider basato su Database")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # 1. Selezione Famiglia
        famiglie_disponibili = df_schneider['Famiglia'].unique()
        famiglia_sel = st.selectbox("Famiglia (POS.3)", famiglie_disponibili)
        
        # Filtro il dataframe per la famiglia scelta
        df_fam = df_schneider[df_schneider['Famiglia'] == famiglia_sel]

        # 2. Selezione Potere di Interruzione (PDI)
        pdi_disponibili = df_fam['PDI'].unique()
        pdi_sel = st.selectbox("Potere di Interruzione (POS.4)", pdi_disponibili)
        
        # Filtro per PDI
        df_pdi = df_fam[df_fam['PDI'] == pdi_sel]

    with c2:
        # 3. Selezione Curva
        curve_disponibili = df_pdi['Curva'].unique()
        curva_sel = st.selectbox("Curva di intervento (POS.5)", curve_disponibili)
        
        # Filtro per Curva
        df_curva = df_pdi[df_pdi['Curva'] == curva_sel]

        # 4. Selezione Poli
        poli_disponibili = df_curva['Poli'].unique()
        poli_sel = st.selectbox("Poli (POS.6)", poli_disponibili)
        
        # Filtro per Poli
        df_poli = df_curva[df_curva['Poli'] == poli_sel]

        # 5. Selezione Corrente (Amperaggio)
        amp_disponibili = df_poli['Amperaggio'].unique()
        amp_sel = st.selectbox("Corrente nominale In (POS.7-8)", amp_disponibili)

    # --- ESTRAZIONE CODICI E GENERAZIONE ---
    # Cerchiamo la riga finale nel database che corrisponde a tutte le selezioni
    risultato = df_poli[df_poli['Amperaggio'] == amp_sel]

    if not risultato.empty:
        # Estraiamo i singoli segmenti dai dati del file (se presenti come colonne)
        # Altrimenti manteniamo la logica di concatenazione stringhe
        f_code = str(risultato.iloc[0].get('Codice_Famiglia', ''))
        p_code = str(risultato.iloc[0].get('Codice_PDI', ''))
        c_code = str(risultato.iloc[0].get('Codice_Curva', ''))
        pol_code = str(risultato.iloc[0].get('Codice_Poli', ''))
        amp_code = str(risultato.iloc[0].get('Codice_Amp', ''))
        
        codice_final = f"A9{f_code}{p_code}{c_code}{pol_code}{amp_code}"
        
        st.success(f"Codice Generato: **{codice_final}**")
        
        pos_data = [
            ("1-2", "A9"), ("3", f_code), ("4", p_code), 
            ("5", c_code), ("6", pol_code), ("7-8", amp_code)
        ]
    else:
        st.error("Configurazione non trovata nel database.")
