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
    # --- LOGICA SCHNEIDER: STRUTTURA PER FAMIGLIE INDIPENDENTI ---
    elif brand == "SCHNEIDER" and is_mcb:
        # Selettore radice: definisce la "grammatica" del codice
        linea = st.selectbox("Seleziona Famiglia Prodotto", [
            "Resi9 (Civile/Residenziale)", 
            "Acti9 iC60 (Industriale)", 
            "Acti9 iC40 / iDPN (Compatto)"
        ])
        
        st.divider()
        c1, c2 = st.columns(2)

    # --- LOGICA SCHNEIDER DEFINITIVA (Vincoli Rigidi da Decoder e PDF) ---
    elif brand == "SCHNEIDER" and is_mcb:
        st.subheader("Configuratore Schneider Electric")
        
        # 1. SELEZIONE LINEA (Reset dinamico delle opzioni)
        linea_sel = st.selectbox("Seleziona Linea Prodotto", [
            "Acti9 iC60 (Industriale Standard)", 
            "Acti9 iC40 / iDPN (Compatto)", 
            "Acti9 C120 / NG125 (Alta Corrente)",
            "Resi9 (Residenziale)"
        ])
        
        st.divider()
        c1, c2 = st.columns(2)

        # Inizializzazione variabili per evitare errori di riferimento
        fam_prefix, serie_code, p_code, c_code, pol_code, amp_fixed = "", "", "", "", "", ""

        # --- A. LOGICA IC60 (A9F...) ---
        if "iC60" in linea_sel:
            fam_prefix, serie_code = "A9", "F"
            with c1:
                pdi_map = {"iC60a (6 kA)": "4", "iC60N (10 kA)": "7", "iC60H (15 kA)": "8", "iC60L (25 kA)": "9"}
                p_code = pdi_map[st.selectbox("Prestazione (POS.4)", list(pdi_map.keys()))]
                curva_map = {"B": "3", "C": "4", "D": "5", "Z": "2", "MA": "0"}
                c_code = curva_map[st.selectbox("Curva (POS.5)", list(curva_map.keys()))]
            with c2:
                pol_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
                pol_code = pol_map[st.selectbox("Poli (POS.6)", list(pol_map.keys()))]
                amp_list = ["01", "02", "03", "04", "06", "10", "16", "20", "25", "32", "40", "50", "63"]
                amp_fixed = st.selectbox("Amperaggio (POS.7-8)", amp_list)

        # --- B. LOGICA IC40 / IDPN (A9P...) ---
        elif "iC40" in linea_sel:
            fam_prefix, serie_code = "A9", "P"
            with c1:
                pdi_map = {"iC40a (4.5 kA)": "4", "iC40N (6 kA)": "5", "iC40H (10 kA)": "6"}
                p_code = pdi_map[st.selectbox("Prestazione (POS.4)", list(pdi_map.keys()))]
                curva_map = {"B": "3", "C": "4"} # iC40 limitato a B e C
                c_code = curva_map[st.selectbox("Curva (POS.5)", list(curva_map.keys()))]
            with c2:
                # VINCOLO POLI: iC40 ha solo 1P+N (6) o 3P+N (7) secondo decoder
                pol_map = {"1P+N": "6", "3P+N": "7"}
                pol_code = pol_map[st.selectbox("Poli (POS.6)", list(pol_map.keys()))]
                amp_list = ["02", "04", "06", "10", "16", "20", "25", "32", "40"]
                amp_fixed = st.selectbox("Amperaggio (POS.7-8)", amp_list)

        # --- C. LOGICA NG125 (A9N...) ---
        elif "NG125" in linea_sel:
            fam_prefix, serie_code = "A9", "N"
            with c1:
                pdi_map = {"NG125a (25kA)": "2", "NG125N (36kA)": "3", "NG125H (70kA)": "4", "NG125L (100kA)": "5"}
                p_code = pdi_map[st.selectbox("Prestazione (POS.4)", list(pdi_map.keys()))]
                c_code = st.selectbox("Curva (POS.5)", ["3", "4", "5"]) # B, C, D
            with c2:
                pol_code = st.selectbox("Poli (POS.6)", ["2", "3", "4"])
                amp_list = ["10", "16", "20", "25", "32", "40", "50", "63", "80", "100", "125"]
                amp_fixed = st.selectbox("Amperaggio (POS.7-8)", amp_list)

        # --- D. LOGICA RESI9 (R9F...) ---
        elif "Resi9" in linea_sel:
            fam_prefix, serie_code = "R9", "F" # Standard residenziale
            with c1:
                p_code = st.selectbox("PDI (POS.4)", ["0", "1"]) # 4.5kA o 6kA
                c_code = "2" # Resi9 usa il 2 per la Curva C secondo logica R9F
                st.info("Curva C preimpostata (POS.5 = 2)")
            with c2:
                pol_map = {"1P+N": "6", "2P": "2", "4P": "4"}
                pol_code = pol_map[st.selectbox("Poli (POS.6)", list(pol_map.keys()))]
                amp_list = ["06", "10", "13", "16", "20", "25", "32", "40"]
                amp_fixed = st.selectbox("Amperaggio (POS.7-8)", amp_list)

        # COMPOSIZIONE CODICE FINALE
        codice_final = f"{fam_prefix}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        
        # Struttura per visualizzazione grafica (uniformata a Siemens)
        pos_data = [
            ("1-2", fam_prefix), ("3", serie_code if serie_code else "-"), 
            ("4", p_code), ("5", c_code), ("6", pol_code), ("7-8", amp_fixed)
        ]
        url_base = f"https://www.se.com/it/it/product/{codice_final}"   

    
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
