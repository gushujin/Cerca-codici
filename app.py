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

    # --- LOGICA SCHNEIDER REVISIONATA (Relazioni Incrociate Totali da PDF) ---
    elif brand == "SCHNEIDER" and is_mcb:
        c1, c2 = st.columns(2)
        
        with c1:
            # 1. SERIE (Determina la struttura di tutto il resto)
            # Dati estratti da PDF: iC60 (Ind.), iC40/DPN (Compatti), Resi9 (Civile)
            serie_sel = st.selectbox("Serie (POS.3)", [
                "iC60N (Standard)", "iC60H (High)", "iC60L (Limiters)", 
                "iC40N (Compact 6kA)", "iDPN (Salvaspazio 4.5kA)", "Resi9"
            ])

            # Mappatura POS 1-2-3
            if "Resi9" in serie_sel:
                fam_code, serie_code = "R9", "F"
            elif "iC40" in serie_sel:
                fam_code, serie_code = "A9", "P"
            elif "iDPN" in serie_sel:
                fam_code, serie_code = "A9", "N"
            else: # iC60
                fam_code = "A9"
                serie_code = "F" if "iC60N" in serie_sel else ("H" if "iC60H" in serie_sel else "L")

            # 2. PDI (POS.4) - Filtrato per Serie
            if "iC60L" in serie_sel: pdi_opts = {"15 kA": "9", "25 kA": "L"}
            elif "iC60H" in serie_sel: pdi_opts = {"10 kA": "8", "15 kA": "9"}
            elif "iC60N" in serie_sel: pdi_opts = {"6 kA": "7", "10 kA": "8"}
            elif "iC40N" in serie_sel: pdi_opts = {"6 kA": "7"}
            elif "iDPN" in serie_sel: pdi_opts = {"4.5 kA": "6"}
            else: # Resi9
                pdi_opts = {"4.5 kA": "0", "6 kA": "1"}
            
            pdi_val = st.selectbox("PDI (POS.4)", list(pdi_opts.keys()))
            p_code = pdi_opts[pdi_val]

            # 3. CURVA (POS.5) - Filtrato per Serie
            # PDF indica: Resi9 = C, iC40 = B/C, iC60 = B/C/D
            if "Resi9" in serie_sel: 
                curva_opts = {"Curva C": "4"}
            elif "iC40" in serie_sel or "iDPN" in serie_sel:
                curva_opts = {"Curva B": "3", "Curva C": "4"}
            else:
                curva_opts = {"Curva B": "3", "Curva C": "4", "Curva D": "5"}
            
            curva_val = st.selectbox("Curva (POS.5)", list(curva_opts.keys()))
            c_code = curva_opts[curva_val]

        with c2:
            # 4. POLI (POS.6) - Relazione critica
            # DPN e iC40 sono SOLO 1P+N o 3P+N (PDF A-4/A-5)
            if "iC40" in serie_sel or "iDPN" in serie_sel:
                pol_opts = {"1P+N": "5", "3P+N": "6"}
            elif "Resi9" in serie_sel:
                pol_opts = {"1P+N": "5", "2P": "2", "4P": "4"}
            else: # iC60
                pol_opts = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
            
            poli_val = st.selectbox("Poli (POS.6)", list(pol_opts.keys()))
            pol_code = pol_opts[poli_val]

            # 5. AMPERAGGIO (POS.7-8) - Relazione con Poli e Serie
            # Gestione restrizione: iC40/Resi9 max 40A. 0.5A solo su iC60 >= 2P.
            if "iC40" in serie_sel or "iDPN" in serie_sel:
                amp_list = ["2A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A"]
            elif "Resi9" in serie_sel:
                amp_list = ["6A", "10A", "16A", "20A", "25A", "32A", "40A"]
            else: # iC60
                if pol_code == "1": # 1P non ha solitamente 0.5A in pronta consegna
                    amp_list = ["1A", "2A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
                else:
                    amp_list = ["0.5A", "1A", "2A", "3A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
            
            amp_sel = st.selectbox("Corrente (POS.7-8)", amp_list)
            
            # Mappatura speciale Amperaggi (PDF A-9)
            amp_map = {
                "0.5A": "70", "1A": "01", "2A": "02", "3A": "03", "4A": "04", 
                "6A": "06", "10A": "10", "16A": "16", "20A": "20", "25A": "25", 
                "32A": "32", "40A": "40", "50A": "50", "63A": "63"
            }
            amp_fixed = amp_map[amp_sel]

        # COMPOSIZIONE E OUTPUT
        codice_final = f"{fam_code}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        
        # Analisi struttura per il layout grafico (uniformato a Siemens)
        pos_data = [
            ("1-2", fam_code), ("3", serie_code), ("4", p_code), 
            ("5", c_code), ("6", pol_code), ("7-8", amp_fixed)
        ]
        
        # Link alla ricerca ufficiale Schneider
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
