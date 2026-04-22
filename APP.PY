import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Multibrand MCB Selector Pro", layout="wide", page_icon="⚡")

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .result-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 10px solid #015F73; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .pos-box { text-align:center; padding:5px; border:1px solid #015F73; border-radius:5px; background-color:white; min-width: 60px; margin: 2px; }
    .pos-label { font-size: 10px; color: #666; font-weight: bold; }
    .pos-val { color:#e63946; font-size:18px; font-weight: bold; }
    .btn-link { display: inline-block; padding: 10px 20px; background-color: #015F73; color: white !important; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SELEZIONE CATEGORIA E BRAND ---
st.sidebar.title("⚙️ Configurazione")
categoria = st.sidebar.selectbox("Seleziona Categoria", ["Magnetotermici (MCB)", "Differenziali"])
brand = st.sidebar.selectbox("Brand Selezionato", ["HAGER", "SIEMENS", "SCHNEIDER", "ABB", "GEWISS", "BTICINO"])

st.title("🔌 Portale Tecnico Multibrand")
st.divider()

col_params, col_res = st.columns([1.8, 1.2])

with col_params:
    st.subheader("🛠️ Specifiche Tecniche")
    codice_final = "N/D"
    pos_data = [] 
    url_base = ""

    if categoria == "Magnetotermici (MCB)":
        c1, c2 = st.columns(2)
        with c1:
            pdi_val = st.selectbox("Potere Interruzione (PDI)", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            poli_val = st.selectbox("Poli", ["1P", "2P", "3P", "4P", "1P+N", "3P+N"])
        with c2:
            amp_val = st.selectbox("Corrente Nominale (In)", ["6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"])
            curva_val = st.selectbox("Curva", ["Curva B", "Curva C", "Curva D"])

        # Preparazione variabili comuni
        amp_num = amp_val.replace("A", "")
        amp_fixed = amp_num.zfill(2) # Forza sempre 2 cifre (es. 06 invece di 6)
        pol_num = poli_val[0]
        curv_let = curva_val[-1] # B, C o D

        # --- LOGICHE BRAND (Basate sulle tabelle POS) ---

        if brand == "HAGER":
            pdi_map = {"6 kA": "B", "10 kA": "C", "15 kA": "D"}
            curv_map = {"Curva B": "A", "Curva C": "B", "Curva D": "C"}
            p_let = pdi_map.get(pdi_val, "B")
            c_let = curv_map.get(curva_val, "B")
            codice_final = f"M{p_let}{c_let}{pol_num}{amp_fixed}"
            pos_data = [("1", "M"), ("2", p_let), ("3", c_let), ("4", pol_num), ("5-6", amp_fixed)]
            url_base = "https://hager.com/it/ricerca?q="

        elif brand == "SIEMENS":
            pdi_map = {"4.5 kA":"3", "6 kA":"6", "10 kA":"4", "15 kA":"7", "25 kA":"8"}
            curv_map = {"Curva B":"6", "Curva C":"7", "Curva D":"8"}
            p_code = pdi_map.get(pdi_val, "6")
            c_code = curv_map.get(curva_val, "7")
            codice_final = f"5SL{p_code}{pol_num}{amp_fixed}-{c_code}"
            pos_data = [("1-2", "5S"), ("3", "L"), ("4", p_code), ("5", pol_num), ("6-7", amp_fixed), ("8", c_code)]
            url_base = "https://sie.ag/search?q="

        elif brand == "SCHNEIDER":
            pdi_map = {"6 kA":"7", "10 kA":"8", "15 kA":"9"}
            curv_map = {"Curva B":"3", "Curva C":"4", "Curva D":"2"}
            p_code = pdi_map.get(pdi_val, "7")
            c_code = curv_map.get(curva_val, "4")
            codice_final = f"A9F{p_code}{c_code}{pol_num}{amp_fixed}"
            pos_data = [("1-2", "A9"), ("3", "F"), ("4", p_code), ("5", c_code), ("6", pol_num), ("7-8", amp_fixed)]
            url_base = "https://www.se.com/it/it/search/"

        elif brand == "ABB":
            pdi_map = {"4.5 kA":"L", "10 kA":"M", "25 kA":"P"}
            p_code = pdi_map.get(pdi_val, "M")
            codice_final = f"S20{pol_num}-{curv_let}{amp_fixed}"
            pos_data = [("1-2", "S2"), ("3", "0"), ("4", p_code), ("5", pol_num), ("6", curv_let), ("7-8", amp_fixed)]
            url_base = "https://new.abb.com/products/it/"

        elif brand == "GEWISS":
            pdi_ser = {"4.5 kA":"40", "6 kA":"41", "10 kA":"42"}.get(pdi_val, "41")
            pdi_spec = {"4.5 kA":"1", "6 kA":"2", "10 kA":"3", "15 kA":"4"}.get(pdi_val, "2")
            codice_final = f"GW{pdi_ser}{curv_let}{pdi_spec}0{pol_num}{amp_fixed}"
            pos_data = [("1-2", "GW"), ("3-4", pdi_ser), ("5", curv_let), ("6", pdi_spec), ("7-8", f"0{pol_num}"), ("9-10", amp_fixed)]
            url_base = "https://www.gewiss.com/it/it/products/search?q="

        elif brand == "BTICINO":
            ser_map = {"4.5 kA":"1", "6 kA":"2", "10 kA":"3"}
            pdi_map = {"4.5 kA":"A", "6 kA":"N", "10 kA":"H", "16 kA":"S"}
            s_code = ser_map.get(pdi_val, "2")
            p_code = pdi_map.get(pdi_val, "N")
            codice_final = f"F8{s_code}{p_code}{curv_let}{pol_num}{amp_fixed}"
            pos_data = [("1-2", "F8"), ("3", s_code), ("4", p_code), ("5", curv_let), ("6", pol_num), ("7-8", amp_fixed)]
            url_base = "https://catalogo.bticino.it/search?q="

        # --- BOX ANALISI ---
        if pos_data:
            st.markdown("---")
            st.write(f"🔍 **Analisi Struttura Codice {brand}**")
            p_cols = st.columns(len(pos_data))
            for i, (label, val) in enumerate(pos_data):
                with p_cols[i]:
                    st.markdown(f"""<div class="pos-box"><div class="pos-label">POS.{label}</div><div class="pos-val">{val}</div></div>""", unsafe_allow_html=True)

with col_res:
    st.subheader("📌 Scheda Prodotto")
    if codice_final != "N/D":
        st.markdown(f"""
            <div class="result-box">
                <h2 style='color:#015F73; margin-top:0;'>{brand}</h2>
                <p><b>Categoria:</b> {categoria}</p>
                <hr>
                <p style='font-size:14px; color:#555;'><b>Parametri:</b><br>
                {pdi_val} | {poli_val} | {amp_val} | {curva_val}</p>
                <div style='background:#f9f9f9; padding:15px; border-radius:8px; text-align:center;'>
                    <span style='font-size:12px; color:#888;'>CODICE ARTICOLO COMPLETO</span><br>
                    <span style='font-size:26px; font-weight:bold; color:#e63946;'>{codice_final}</span>
                </div>
                <a href="{url_base}{codice_final}" target="_blank" class="btn-link">Vai al Catalogo Ufficiale ↗</a>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Configura i parametri tecnici.")
