import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Multibrand MCB Selector Pro", layout="wide", page_icon="⚡")

# --- STILE CSS ---
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

st.title("🔌 Portale Tecnico Multibrand")
st.sidebar.title("⚙️ Configurazione")

categoria = st.sidebar.selectbox("Seleziona Categoria", ["Magnetotermici (MCB)"])
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS", "SCHNEIDER", "HAGER"])

st.divider()
col_params, col_res = st.columns([1.8, 1.2])

with col_params:
    st.subheader(f"🛠️ Specifiche {brand}")
    codice_final = ""
    pos_data = []
    url_base = ""

    if brand == "SIEMENS":
        c1, c2 = st.columns(2)
        with c1:
            serie_opt = {"L=Standard": "L", "Y=Industriale": "Y", "P=Di Potenza": "P"}
            serie_sel = st.selectbox("Serie (POS.3)", list(serie_opt.keys()))
            serie_code = serie_opt[serie_sel]
            
            pdi_opt = {"4.5 kA": "3", "6 kA": "6", "10 kA": "4", "15 kA": "7", "25 kA": "8"}
            pdi_sel = st.selectbox("PDI (POS.4)", list(pdi_opt.keys()))
            p_code = pdi_opt[pdi_sel]
        with c2:
            pol_opt = {"1P": "1", "2P": "2", "3P": "3", "4P": "4", "1P+N": "5", "3P+N": "6"}
            pol_sel = st.selectbox("Poli (POS.5)", list(pol_opt.keys()))
            pol_code = pol_opt[pol_sel]
            
            amp_opt = ["06", "10", "16", "20", "25", "32", "40", "50", "63"]
            amp_fixed = st.selectbox("Corrente (POS.6-7)", amp_opt)
            
            curv_opt = {"Curva B": "6", "Curva C": "7", "Curva D": "8"}
            curv_sel = st.selectbox("Curva (POS.8)", list(curv_opt.keys()))
            c_code = curv_opt[curv_sel]

        codice_final = f"5S{serie_code}{p_code}{pol_code}{amp_fixed}{c_code}"
        pos_data = [("1-2", "5S"), ("3", serie_code), ("4", p_code), ("5", pol_code), ("6-7", amp_fixed), ("8", c_code)]
        url_base = "https://support.industry.siemens.com/cs/products?search="

    elif brand == "SCHNEIDER":
        c1, c2 = st.columns(2)
        with c1:
            fam_opt = {"A9 = Terziario/comm.": "A9", "R9 = Residenziale": "R9"}
            fam_sel = st.selectbox("Famiglia (POS.1-2)", list(fam_opt.keys()))
            fam_code = fam_opt[fam_sel]
            
            serie_code = "F" # iC60N
            st.text_input("Serie (POS.3)", value="F (iC60N)", disabled=True)
            
            pdi_opt = {"7=6kA": "7", "8=10kA": "8", "9=15kA": "9"}
            pdi_sel = st.selectbox("PDI (POS.4)", list(pdi_opt.keys()))
            p_code = pdi_opt[pdi_sel]
        with c2:
            curv_opt = {"3=Curva B": "3", "4=Curva C": "4", "2=Curva D": "2"}
            curv_sel = st.selectbox("Curva (POS.5)", list(curv_opt.keys()))
            c_code = curv_opt[curv_sel]
            
            pol_opt = {"1=1P": "1", "2=2P": "2", "3=3P": "3", "4=4P": "4", "5=1P+N": "5"}
            pol_sel = st.selectbox("Poli (POS.6)", list(pol_opt.keys()))
            pol_code = pol_opt[pol_sel]
            
            amp_opt = ["06", "10", "16", "20", "25", "32", "40", "50", "63"]
            amp_fixed = st.selectbox("Corrente (POS.7)", amp_opt)

        codice_final = f"{fam_code}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        pos_data = [("1-2", fam_code), ("3", serie_code), ("4", p_code), ("5", c_code), ("6", pol_code), ("7", amp_fixed)]
        url_base = "https://www.se.com/it/it/search/"

    elif brand == "HAGER":
        pdi_map = {"6 kA": "B", "10 kA": "C", "15 kA": "D"}
        curv_map = {"Curva B": "A", "Curva C": "B", "Curva D": "C"}
        pdi_val = st.selectbox("PDI", list(pdi_map.keys()))
        curva_val = st.selectbox("Curva", list(curv_map.keys()))
        poli_val = st.selectbox("Poli", ["1", "2", "3", "4"])
        amp_val = st.selectbox("Corrente", ["06", "10", "16", "20", "25", "32", "40", "50", "63"])
        
        p_let = pdi_map[pdi_val]
        c_let = curv_map[curva_val]
        codice_final = f"M{p_let}{c_let}{poli_val}{amp_val}"
        pos_data = [("1", "M"), ("2", p_let), ("3", c_let), ("4", poli_val), ("5-6", amp_val)]
        url_base = "https://hager.com/it/ricerca?q="

    # --- VISUALIZZAZIONE ANALISI ---
    if pos_data:
        st.markdown("---")
        st.write(f"🔍 **Analisi Struttura Codice {brand}**")
        p_cols = st.columns(len(pos_data))
        for i, (label, val) in enumerate(pos_data):
            with p_cols[i]:
                st.markdown(f'<div class="pos-box"><div class="pos-label">POS.{label}</div><div class="pos-val">{val}</div></div>', unsafe_allow_html=True)

with col_res:
    st.subheader("📌 Risultato")
    if codice_final:
        st.markdown(f"""
            <div class="result-box">
                <h2 style='color:#015F73; margin-top:0;'>{brand}</h2>
                <div style='background:#f9f9f9; padding:15px; border-radius:8px; text-align:center;'>
                    <span style='font-size:12px; color:#888;'>CODICE ARTICOLO GENERATO</span><br>
                    <span style='font-size:26px; font-weight:bold; color:#e63946;'>{codice_final}</span>
                </div>
                <a href="{url_base}{codice_final}" target="_blank" class="btn-link">Catalogo Ufficiale ↗</a>
            </div>
        """, unsafe_allow_html=True)
