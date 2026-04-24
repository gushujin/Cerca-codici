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

    elif brand == "SCHNEIDER" and is_mcb:
        c1, c2 = st.columns(2)
        
        with c1:
            # 1. & 2. FAMIGLIA E SERIE (Logica accorpata per coerenza codici PDF)
            serie_sel = st.selectbox("Serie", [
                "iC60N (6kA)", "iC60H (10kA)", "iC60L (15kA)", 
                "iC40a (4.5kA)", "iC40N (6kA)", 
                "Resi9 (Salvaspazio)", "Resi9 (Standard)"
            ])

            # Inizializzazione variabili POS
            if "Resi9" in serie_sel:
                fam_code = "R9"
                serie_code = "P" if "Salvaspazio" in serie_sel else "F"
                # Mappatura fissa POS.4-5 per Resi9 (4500A Curva C)
                p_code = "3" if serie_code == "P" else "3" 
                c_code = "56" if serie_code == "P" else "76"
            else:
                fam_code = "A9"
                if "iC40" in serie_sel:
                    serie_code = "P"
                    p_code = "2" if "iC40a" in serie_sel else "4" # POS.4
                    c_code = "6" # POS.5 (Standard per iC40)
                else: # iC60
                    serie_code = "F"
                    p_code = {"iC60N (6kA)": "7", "iC60H (10kA)": "8", "iC60L (15kA)": "9"}[serie_sel]
                    c_code = "4" # Default Curva C (verrà sovrascritto sotto)

            # 3. CURVA (Solo se non è Resi9, che è fissa C nel PDF)
            if "Resi9" not in serie_sel:
                curva_map = {"B": "3", "C": "4", "D": "5"}
                curva_val = st.selectbox("Curva (POS.5)", ["B", "C", "D"], index=1)
                # Per iC60 la POS.5 è la curva, per iC40 la curva è parte della POS.4/5
                if "iC60" in serie_sel:
                    c_code = curva_map[curva_val]
                else: # iC40: Curva B=4, Curva C=5 in POS.4
                    p_code = "4" if curva_val == "B" else "5"
            else:
                st.info("Resi9: Curva C predefinita (da catalogo)")

        with c2:
            # 4. POLI
            if "iC40" in serie_sel or "Resi9" in serie_sel:
                pol_map = {"1P+N": "6" if "Resi9" in serie_sel else "2", "3P+N": "7" if "Resi9" in serie_sel else "4"}
                # Nota: iC40/Resi9 usano mappature poli specifiche (POS.6)
                if "iC40" in serie_sel:
                    pol_map = {"1P+N": "6", "3P+N": "7"} # iC40 usa 6 per 1P+N
            else:
                pol_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
            
            poli_val = st.selectbox("Poli (POS.6)", list(pol_map.keys()))
            pol_code = pol_map[poli_val]

            # 5. AMPERAGGIO (Filtri Reali PDF)
            if "Resi9" in serie_sel:
                amp_list = ["6A", "10A", "16A", "20A", "25A", "32A"]
            elif "iC40" in serie_sel:
                amp_list = ["2A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A"]
            else:
                amp_list = ["0.5A", "1A", "2A", "3A", "4A", "6A", "10A", "13A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
            
            amp_sel = st.selectbox("Corrente (POS.7-8)", amp_list)
            amp_fixed = amp_sel.replace("A", "").zfill(2) if amp_sel != "0.5A" else "70"

        # COMPOSIZIONE
        # Esempio iC60N: A9F 7 4 2 16 (A9F, PDI 7, Curva 4, 2 Poli, 16A)
        # Esempio iC40N: A9P 5 4 6 16 (A9P, Curva C 5, PDI 4, Poli 6, 16A)
        codice_final = f"{fam_code}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"


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
