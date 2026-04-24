import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Multibrand MCB Selector Pro", layout="wide", page_icon="⚡")

# --- STILE CSS PERSONALIZZATO (Responsive) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .result-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 10px solid #015F73; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .pos-box { text-align:center; padding:10px; border:1px solid #015F73; border-radius:8px; background-color:white; min-width: 70px; margin: 5px; flex: 1; }
    .pos-label { font-size: 11px; color: #666; font-weight: bold; margin-bottom: 5px; }
    .pos-val { color:#e63946; font-size:22px; font-weight: bold; }
    .btn-link { display: inline-block; padding: 10px 20px; background-color: #015F73; color: white !important; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px; text-align: center; width: 100%; }
    
    /* Container per i box dell'analisi codice */
    .analysis-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 10px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SELEZIONE ---
st.sidebar.title("⚙️ Configurazione")

# AGGIORNAMENTO: Nuove categorie inserite nel menù a tendina
elenco_categorie = [
    "Magnetotermici (MCB)", 
    "Differenziali Puri", 
    "Magnetotermici Differenziali", 
    "Blocchi Differenziali"
]
categoria = st.sidebar.selectbox("Seleziona Categoria", elenco_categorie)

# SCORCIATOIA LOGICA: Abilita i menù specifici solo per MCB
is_mcb = (categoria == "Magnetotermici (MCB)")

brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS", "SCHNEIDER", "HAGER", "ABB", "GEWISS", "BTICINO"])

st.title("🔌 Portale Tecnico Multibrand")
st.divider()

col_params, col_res = st.columns([1.8, 1.2])

with col_params:
    st.subheader(f"🛠️ {categoria} - {brand}")
    
    # Inizializzazione variabili comuni per evitare NameError
    codice_final = "N/D"
    pos_data = [] 
    url_base = ""
    pdi_val = poli_val = amp_val = curva_val = ""

    # Se la categoria NON è MCB, mostra un avviso (da implementare in futuro)
    if not is_mcb:
        st.warning(f"La logica per **{categoria}** è in fase di implementazione. Al momento è attivo solo il configuratore Magnetotermici.")

    # --- LOGICA SIEMENS (Abilitata solo se is_mcb è True) ---
    if brand == "SIEMENS" and is_mcb:
        c1, c2 = st.columns(2)
        with c1:
            serie_val = st.selectbox("Serie (POS.3)", ["L=Standard", "Y=Industriale", "P=Di Potenza"])
            serie_code = serie_val[0]
            pdi_val = st.selectbox("Potere Interruzione (PDI - POS.4)", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            pdi_map = {"4.5 kA":"3", "6 kA":"6", "10 kA":"4", "15 kA":"7", "25 kA":"8"}
            p_code = pdi_map.get(pdi_val)
        with c2:
            poli_val = st.selectbox("Poli (POS.5)", ["1P", "2P", "3P", "4P", "1P+N", "3P+N"])
            pol_map = {"1P":"1", "2P":"2", "3P":"3", "4P":"4", "1P+N":"5", "3P+N":"6"}
            pol_code = pol_map.get(poli_val)
            amp_val = st.selectbox("Corrente (In - POS.6-7)", ["6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"])
            amp_fixed = amp_val.replace("A", "").zfill(2)
            curva_val = st.selectbox("Curva (POS.8)", ["Curva B", "Curva C", "Curva D"])
            curv_map = {"Curva B":"6", "Curva C":"7", "Curva D":"8"}
            c_code = curv_map.get(curva_val)

        codice_final = f"5S{serie_code}{p_code}{pol_code}{amp_fixed}{c_code}"
        pos_data = [("1-2", "5S"), ("3", serie_code), ("4", p_code), ("5", pol_code), ("6-7", amp_fixed), ("8", c_code)]
        url_base = "https://support.industry.siemens.com/cs/products?search="
    # --- LOGICA SCHNEIDER (Interattiva e Vincolata - Basata su PDF e Decoder) ---
    if brand == "SCHNEIDER" and is_mcb:
        c1, c2 = st.columns(2)
        
        with c1:
            # POS.1-2: Prefisso Gamma
            gamma_val = st.selectbox("Gamma (POS.1-2)", ["Acti9 (A9)", "Resi9 (R9F)", "Resi9 Compatto (R9P)"])
            fam_prefix = "A9" if "Acti9" in gamma_val else ("R9F" if "R9F" in gamma_val else "R9P")

            # POS.3: Famiglia (Vincolata alla Gamma)
            if fam_prefix == "A9":
                serie_opts = {"iC60 (Standard)": "F", "iC40 (Compatto)": "P", "C120/NG125": "N"}
                serie_val = st.selectbox("Famiglia (POS.3)", list(serie_opts.keys()))
                serie_code = serie_opts[serie_val]
            else:
                serie_code = "" # Per Resi9 il prefisso è già completo
                serie_val = "Resi9"

            # POS.4: Livello Prestazione (Vincolato alla Serie)
            if serie_code == "P": # iC40
                pdi_map = {"iC40a (4.5 kA)": "4", "iC40N (6 kA)": "5", "iC40H (10 kA)": "6"}
            elif serie_code == "N": # NG125
                pdi_map = {"NG125a (25 kA)": "2", "NG125N (36 kA)": "3", "NG125H (70 kA)": "4", "NG125L (100 kA)": "5"}
            elif fam_prefix.startswith("R9"): # Resi9
                pdi_map = {"Base (4.5 kA)": "0", "Standard (6 kA)": "1"}
            else: # iC60
                pdi_map = {"versione 'a' (6 kA)": "4", "versione N (10 kA)": "7", "versione H (15 kA)": "8", "versione L (25 kA)": "9"}
            
            pdi_sel = st.selectbox("Prestazione (POS.4)", list(pdi_map.keys()))
            p_code = pdi_map[pdi_sel]

        with c2:
            # POS.5: Curva (Vincolata)
            if fam_prefix.startswith("R9"):
                curv_map = {"Curva C": "4"}
            else:
                curv_map = {"Curva B": "3", "Curva C": "4", "Curva D": "5", "Curva Z": "2", "Curva MA": "0"}
            
            curva_val = st.selectbox("Curva (POS.5)", list(curv_map.keys()))
            c_code = curv_map[curva_val]

            # POS.6: Poli (Vincolo iC40/Resi9)
            if serie_code == "P" or fam_prefix == "R9P":
                pol_map = {"1P+N (Vigi)": "6", "3P+N (Vigi)": "7"}
            else:
                pol_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
            
            poli_val = st.selectbox("Poli (POS.6)", list(pol_map.keys()))
            pol_code = pol_map[poli_val]

            # POS.7-8: Corrente (Vincolata alla Serie)
            if serie_code == "N":
                amp_opts = ["10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A", "80A", "100A", "125A"]
            elif serie_code == "P" or fam_prefix.startswith("R9"):
                amp_opts = ["02A", "04A", "06A", "10A", "13A", "16A", "20A", "25A", "32A", "40A"]
            else:
                amp_opts = ["01A", "02A", "04A", "06A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
            
            amp_val = st.selectbox("Corrente (POS.7-8)", amp_opts)
            amp_fixed = amp_val.replace("A", "").zfill(2)

        # COMPOSIZIONE CODICE
        codice_final = f"{fam_prefix}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        
        # Struttura per visualizzazione quadratini (come Siemens)
        pos_data = [
            ("1-2", fam_prefix), 
            ("3", serie_code if serie_code else "-"), 
            ("4", p_code), 
            ("5", c_code), 
            ("6", pol_code), 
            ("7-8", amp_fixed)
        ]
        
        # Link ricerca ufficiale e Layout
        st.markdown(f"### Codice Generato: `{codice_final}`")
        url_base = "https://www.se.com/it/it/search/"
        st.write(f"[Vai alla ricerca sul sito del produttore]({url_base}{codice_final})")    
    
    
    # --- LOGICA HAGER (Abilitata solo se is_mcb è True) ---
    elif brand == "HAGER" and is_mcb:
        c1, c2 = st.columns(2)
        with c1:
            pdi_val = st.selectbox("PDI", ["6 kA", "10 kA", "15 kA"])
            pdi_map = {"6 kA": "B", "10 kA": "C", "15 kA": "D"}
            p_let = pdi_map.get(pdi_val)
            curva_val = st.selectbox("Curva", ["Curva B", "Curva C", "Curva D"])
            curv_map = {"Curva B": "A", "Curva C": "B", "Curva D": "C"}
            c_let = curv_map.get(curva_val)
        with c2:
            poli_val = st.selectbox("Poli", ["1P", "2P", "3P", "4P"])
            pol_num = poli_val[0]
            amp_val = st.selectbox("Corrente (In)", ["6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"])
            amp_fixed = amp_val.replace("A", "").zfill(2)

        codice_final = f"M{p_let}{c_let}{pol_num}{amp_fixed}"
        pos_data = [("1", "M"), ("2", p_let), ("3", c_let), ("4", pol_num), ("5-6", amp_fixed)]
        url_base = "https://hager.com/it/ricerca?q="

    # --- BOX ANALISI COMUNE ---
    if pos_data:
        st.markdown("---")
        st.write(f"🔍 **Analisi Struttura Codice {brand}**")
        boxes_html = "".join([f'<div class="pos-box"><div class="pos-label">POS.{l}</div><div class="pos-val">{v}</div></div>' for l, v in pos_data])
        st.markdown(f'<div class="analysis-container">{boxes_html}</div>', unsafe_allow_html=True)

with col_res:
    st.subheader("📌 Scheda Prodotto")
    if codice_final != "N/D":
        st.markdown(f"""
            <div class="result-box">
                <h2 style='color:#015F73; margin-top:0;'>{brand}</h2>
                <p><b>Categoria:</b> {categoria}</p>
                <hr>
                <p style='font-size:14px; color:#555;'><b>Parametri Selezionati:</b><br>
                {pdi_val} | {poli_val} | {amp_val} | {curva_val}</p>
                <div style='background:#f9f9f9; padding:15px; border-radius:8px; text-align:center;'>
                    <span style='font-size:12px; color:#888;'>CODICE ARTICOLO COMPLETO</span><br>
                    <span style='font-size:28px; font-weight:bold; color:#e63946;'>{codice_final}</span>
                </div>
                <a href="{url_base}{codice_final}" target="_blank" class="btn-link">Vai al Catalogo Ufficiale ↗</a>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Configura i parametri per generare il codice articolo.")
