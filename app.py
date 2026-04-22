import streamlit as st

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Multibrand MCB Selector", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    /* Box Unico Risultato */
    .result-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 10px solid #015F73; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .pos-box { text-align:center; padding:5px; border:1px solid #015F73; border-radius:5px; background-color:white; min-width: 55px; margin: 2px; }
    .pos-label { font-size: 10px; color: #666; font-weight: bold; }
    .pos-val { color:#e63946; font-size:18px; font-weight: bold; }
    .btn-link { display: inline-block; padding: 10px 20px; background-color: #015F73; color: white !important; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("⚙️ Parametri di Sistema")
categoria = st.sidebar.selectbox("Seleziona Categoria", ["Magnetotermici (MCB)", "Differenziali"])
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS", "SCHNEIDER", "ABB", "GEWISS", "BTICINO", "HAGER"])

st.title("🔌 Portale Tecnico Multibrand")
st.divider()

col_params, col_res = st.columns([1.8, 1.2])

with col_params:
    st.subheader("🛠️ Specifiche Tecniche")
    codice_final = "N/D"
    pos_data = [] 
    url_produttore = "#"

    if categoria == "Magnetotermici (MCB)":
        c1, c2 = st.columns(2)
        with c1:
            pdi_val = st.selectbox("Potere Interruzione (PDI)", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            poli_val = st.selectbox("Poli", ["1P", "2P", "3P", "4P", "1P+N", "3P+N"])
        with c2:
            amp_val = st.selectbox("Corrente Nominale (In)", ["6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"])
            curva_val = st.selectbox("Curva", ["Curva B", "Curva C", "Curva D"])

        amp = amp_val.replace("A", "")
        pol = poli_val[0]

        # --- LOGICA GENERAZIONE CODICI E LINK ---
        if brand == "SIEMENS":
            pdi_map = {"4.5 kA":"3", "6 kA":"6", "10 kA":"4", "15 kA":"7", "25 kA":"8"}
            curva_map = {"Curva B":"6", "Curva C":"7", "Curva D":"8"}
            pdi_code = pdi_map.get(pdi_val, "6")
            curv_code = curva_map.get(curva_val, "7")
            codice_final = f"5SL{pdi_code}{pol}{amp}-{curv_code}"
            pos_data = [("1-2", "5S"), ("3", "L"), ("4", pdi_code), ("5", pol), ("6-7", amp), ("8", curv_code)]
            url_produttore = f"https://sie.ag/search?q={codice_final}"

        elif brand == "SCHNEIDER":
            pdi_map = {"6 kA":"7", "10 kA":"8", "15 kA":"9"}
            curva_map = {"Curva B":"3", "Curva C":"4", "Curva D":"2"}
            pdi_code = pdi_map.get(pdi_val, "7")
            curv_code = curva_map.get(curva_val, "4")
            codice_final = f"A9F{pdi_code}{curv_code}{pol}{amp}"
            pos_data = [("1-2", "A9"), ("3", "F"), ("4", pdi_code), ("5", curv_code), ("6", pol), ("7-8", amp)]
            url_produttore = f"https://www.se.com/it/it/search/{codice_final}"

        elif brand == "ABB":
            pdi_map = {"4.5 kA":"L", "10 kA":"M", "25 kA":"P"}
            curva_map = {"Curva B":"B", "Curva C":"C", "Curva D":"D"}
            p_code = pdi_map.get(pdi_val, "M")
            c_code = curva_map.get(curva_val, "C")
            codice_final = f"S20{pol}-{c_code}{amp}"
            pos_data = [("1-2", "S2"), ("3", "0"), ("4", p_code), ("5", pol), ("6", c_code), ("7-8", amp)]
            url_produttore = f"https://new.abb.com/products/it/{codice_final}"

        elif brand == "GEWISS":
            pdi_ser = {"4.5 kA":"40", "6 kA":"41", "10 kA":"42"}.get(pdi_val, "41")
            pdi_spec = {"4.5 kA":"1", "6 kA":"2", "10 kA":"3", "15 kA":"4"}.get(pdi_val, "2")
            curv_code = curva_val[-1]
            pol_code = f"0{pol}"
            codice_final = f"GW{pdi_ser}{curv_code}{pdi_spec}{pol_code}{amp}"
            pos_data = [("1-2", "GW"), ("3-4", pdi_ser), ("5", curv_code), ("6", pdi_spec), ("7-8", pol_code), ("9-10", amp)]
            url_produttore = f"https://www.gewiss.com/it/it/products/search?q={codice_final}"

        elif brand == "BTICINO":
            ser_map = {"4.5 kA":"1", "6 kA":"2", "10 kA":"3"}
            pdi_map = {"4.5 kA":"A", "6 kA":"N", "10 kA":"H", "16 kA":"S"}
            curv_code = curva_val[-1]
            codice_final = f"F8{ser_map.get(pdi_val,'2')}{pdi_map.get(pdi_val,'N')}{curv_code}{pol}{amp}"
            pos_data = [("1-2", "F8"), ("3", ser_map.get(pdi_val,'2')), ("4", pdi_map.get(pdi_val,'N')), ("5", curv_code), ("6", pol), ("7-8", amp)]
            url_produttore = f"https://catalogo.bticino.it/search?q={codice_final}"

        elif brand == "HAGER":
            pdi_map = {"6 kA":"N", "10 kA":"H", "15 kA":"L"}
            curv_code = curva_val[-1]
            codice_final = f"M{curv_code}{pol}{amp}{pdi_map.get(pdi_val,'N')}"
            pos_data = [("1", "M"), ("2", curv_code), ("3", pdi_map.get(pdi_val,'N')), ("4", pol), ("5-6", amp), ("7", "A")]
            url_produttore = f"https://hager.com/it/ricerca?q={codice_final}"

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
                <p style='font-size:14px; color:#555;'><b>Caratteristiche selezionate:</b><br>
                {pdi_val} | {poli_val} | {amp_val} | {curva_val}</p>
                <div style='background:#f9f9f9; padding:15px; border-radius:8px; text-align:center;'>
                    <span style='font-size:12px; color:#888;'>CODICE ARTICOLO</span><br>
                    <span style='font-size:24px; font-weight:bold; color:#e63946;'>{codice_final}</span>
                </div>
                <a href="{url_produttore}" target="_blank" class="btn-link">Vai alla Scheda Tecnica ↗</a>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Configura i parametri per visualizzare il risultato.")
