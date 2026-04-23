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
categoria = st.sidebar.selectbox("Seleziona Categoria", ["Magnetotermici (MCB)"])
brand = st.sidebar.selectbox("Brand Selezionato", ["SIEMENS", "SCHNEIDER", "HAGER", "ABB", "GEWISS", "BTICINO"])

st.title("🔌 Portale Tecnico Multibrand")
st.divider()

col_params, col_res = st.columns([1.8, 1.2])

with col_params:
    st.subheader(f"🛠️ Specifiche Tecniche {brand}")
    codice_final = "N/D"
    pos_data = [] 
    url_base = ""

    # --- LOGICHE BRAND CON VINCOLI INTERNI ---
    
    if brand == "SIEMENS":
        c1, c2 = st.columns(2)
        with c1:
            # Vincoli POS.3
            serie_val = st.selectbox("Serie (POS.3)", ["L=Standard", "Y=Industriale", "P=Di Potenza"])
            serie_code = serie_val[0]
            # Vincoli POS.4
            pdi_val = st.selectbox("Potere Interruzione (PDI - POS.4)", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
            pdi_map = {"4.5 kA":"3", "6 kA":"6", "10 kA":"4", "15 kA":"7", "25 kA":"8"}
            p_code = pdi_map.get(pdi_val)
        with c2:
            # Vincoli POS.5
            poli_val = st.selectbox("Poli (POS.5)", ["1P", "2P", "3P", "4P", "1P+N", "3P+N"])
            pol_map = {"1P":"1", "2P":"2", "3P":"3", "4P":"4", "1P+N":"5", "3P+N":"6"}
            pol_code = pol_map.get(poli_val)
            # Vincoli POS.6-7
            amp_val = st.selectbox("Corrente (In - POS.6-7)", ["6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"])
            amp_fixed = amp_val.replace("A", "").zfill(2)
            # Vincoli POS.8
            curva_val = st.selectbox("Curva (POS.8)", ["Curva B", "Curva C", "Curva D"])
            curv_map = {"Curva B":"6", "Curva C":"7", "Curva D":"8"}
            c_code = curv_map.get(curva_val)

        codice_final = f"5S{serie_code}{p_code}{pol_code}{amp_fixed}{c_code}"
        pos_data = [("1-2", "5S"), ("3", serie_code), ("4", p_code), ("5", pol_code), ("6-7", amp_fixed), ("8", c_code)]
        url_base = "https://support.industry.siemens.com/cs/products?search="

    elif brand == "SCHNEIDER":
        c1, c2 = st.columns(2)
        
        #with c2:
        #    st.subheader("Configuratore Acti9 iC60N") 

        with c1:
            # POS. 1-2: FAMIGLIA
            fam_code = st.selectbox("Famiglia (POS.1-2)", ["A9", "R9"])

            # POS. 3: SERIE
            serie_code = "F"
            st.text_input("Serie (POS.3)", value="F", disabled=True)

            # POS. 4: PDI
            pdi_val = st.selectbox("PDI (POS.4)", ["6 kA", "10 kA", "15 kA"])
            pdi_map = {"6 kA": "7", "10 kA": "8", "15 kA": "9"}
            p_code = pdi_map[pdi_val]

            # SELEZIONE CORRENTE (POS. 7-8)
            amp_options = ["0,5A", "1A", "2A", "3A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
            amp_val = st.selectbox("Corrente Nominale (POS.7-8)", amp_options)
            current_numeric = float(amp_val.replace('A', '').replace(',', '.'))

        with c2:
            # POS. 6: POLI
            poli_val = st.selectbox("Poli (POS.6)", ["1P", "2P", "3P", "4P"])
            pol_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
            pol_code = pol_map[poli_val]

            # POS. 5: CURVA (LOGICA INTERDIPENDENTE)
            curva_val = st.selectbox("Curva di Intervento", ["B", "C", "D"])
            
            if curva_val == "B":
                c_code = "3" if current_numeric < 6 else "8"
            elif curva_val == "C":
                c_code = "4" if current_numeric < 6 else "9"
            else: # Curva D
                c_code = "5"

            # DEFINIZIONE amp_fixed (POS. 7-8)
            if current_numeric == 0.5:
                amp_fixed = "70"
            else:
                amp_fixed = f"{int(current_numeric):02d}"

        # COMPOSIZIONE FINALE
        codice_final = f"{fam_code}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        url_base = "https://www.se.com/it/it//products?search="
        
        # RISULTATO FINALE
        #st.divider()
        #st.success(f"**Codice Schneider Generato: {codice_final}**")

        # --- NUOVA PARTE GRAFICA: ANALISI STRUTTURA CODICE ---
        #st.write("### 🔍 Analisi Struttura Codice SCHNEIDER")
        
        # Creiamo 6 colonne per i 6 blocchi del codice
        #cols = st.columns(6)
        
        # Definiamo i dati dei box (Etichetta, Valore)
        struttura = [
            ("POS.1-2", fam_code),
            ("POS.3", serie_code),
            ("POS.4", p_code),
            ("POS.5", c_code),
            ("POS.6", pol_code),
            ("POS.7-8", amp_fixed)
        ]
        
        #for i, (label, value) in enumerate(struttura):
        #    with cols[i]:
                # HTML/CSS per creare il box colorato
        #        st.markdown(
        #            f"""
                    <div style="
                        border: 2px solid #00778b;
                        border-radius: 10px;
                        padding: 10px;
                        text-align: center;
                        background-color: #f0f8f9;
                        min-height: 80px;">
                        <p style="margin: 0; font-size: 12px; color: #555; font-weight: bold;">{label}</p>
                        <p style="margin: 0; font-size: 24px; color: #e63946; font-weight: bold;">{value}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    elif brand == "HAGER":
        c1, c2 = st.columns(2)
        with c1:
            pdi_val = st.selectbox("Potere Interruzione (PDI)", ["6 kA", "10 kA", "15 kA"])
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

    # --- BOX ANALISI (Comune) ---
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
                <p style='font-size:14px; color:#555;'><b>Parametri Generati:</b><br>
                {pdi_val} | {poli_val} | {amp_val} | {curva_val}</p>
                <div style='background:#f9f9f9; padding:15px; border-radius:8px; text-align:center;'>
                    <span style='font-size:12px; color:#888;'>CODICE ARTICOLO COMPLETO</span><br>
                    <span style='font-size:26px; font-weight:bold; color:#e63946;'>{codice_final}</span>
                </div>
                <a href="{url_base}{codice_final}" target="_blank" class="btn-link">Vai al Catalogo Ufficiale ↗</a>
            </div>
        """, unsafe_allow_html=True)
