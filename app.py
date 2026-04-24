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

    # --- LOGICA SCHNEIDER (Basata su Catalogo PDF) ---
    elif brand == "SCHNEIDER" and is_mcb:
        c1, c2 = st.columns(2)
        
        with c1:
            # 1. Famiglia (A9 = Acti9, R9 = Resi9)
            fam_code = st.selectbox("Famiglia (POS.1-2)", ["A9", "R9"])
            
            # 2. Serie (POS.3) - Relazioni reali dal catalogo
            if fam_code == "R9":
                serie_map = {"Resi9 (Civile)": "F"}
            else:
                # Dal PDF: F=iC60N, H=iC60H, L=iC60L, P=iC40/iDPN
                serie_map = {
                    "iC60N (Standard)": "F", 
                    "iC60H (High)": "H", 
                    "iC60L (Limiters)": "L", 
                    "iC40N / iDPN (Compact)": "P"
                }
            serie_sel = st.selectbox("Serie (POS.3)", list(serie_map.keys()))
            serie_code = serie_map[serie_sel]

            # 3. PDI (POS.4) - Relazioni reali
            if "iC60L" in serie_sel:
                pdi_map = {"15 kA": "8", "25 kA": "9"}
            elif "iC60H" in serie_sel:
                pdi_map = {"10 kA": "7", "15 kA": "8"}
            elif "iC40" in serie_sel or "iDPN" in serie_sel:
                pdi_map = {"4.5 kA": "3", "6 kA": "6"} # Tipico iC40/DPN
            else: # iC60N o Resi9
                pdi_map = {"6 kA": "6", "10 kA": "7"}
            
            pdi_val = st.selectbox("PDI (POS.4)", list(pdi_map.keys()))
            p_code = pdi_map[pdi_val]

            # 4. Curva (POS.5) - In Schneider la curva precede i poli nel codice
            curva_map = {"Curva B": "3", "Curva C": "4", "Curva D": "5"}
            curva_sel = st.selectbox("Curva (POS.5)", list(curva_map.keys()))
            c_code = curva_map[curva_sel]

        with c2:
            # 5. Poli (POS.6) - RELAZIONE CRITICA DAL PDF
            # Gli interruttori iC40 e iDPN (Serie P) sono tipicamente combinati
            if "iC40" in serie_sel or "iDPN" in serie_sel:
                pol_map = {"1P+N (Salvaspazio)": "5", "3P+N (Salvaspazio)": "6"}
            else:
                pol_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
            
            poli_val = st.selectbox("Poli (POS.6)", list(pol_map.keys()))
            pol_code = pol_map[poli_val]

            # 6. Corrente (POS.7-8) - RELAZIONE REALE AMBIENTE/TAGLIO
            # La serie compatta (P) arriva raramente a 63A, si ferma a 40A (A-4 / A-5 PDF)
            if "iC40" in serie_sel or "Resi9" in serie_sel:
                amp_list = ["2A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A"]
            else:
                amp_list = ["0.5A", "1A", "2A", "3A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
            
            amp_sel = st.selectbox("Corrente (POS.7-8)", amp_list)
            
            # Mapping speciale Schneider per piccoli tagli e standard
            amp_special_map = {
                "0.5A": "70", "1A": "01", "2A": "02", "3A": "03", "4A": "04", 
                "6A": "06", "10A": "10", "16A": "16", "20A": "20", "25A": "25", 
                "32A": "32", "40A": "40", "50A": "50", "63A": "63"
            }
            amp_fixed = amp_special_map[amp_sel]

        # Composizione finale (Struttura corretta: FAM + SERIE + PDI + CURVA + POLI + AMP)
        codice_final = f"{fam_code}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        
        pos_data = [
            ("1-2", fam_code), ("3", serie_code), ("4", p_code), 
            ("5", c_code), ("6", pol_code), ("7-8", amp_fixed)
        ]
        url_base = "https://www.se.com/it/it/search/"



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
