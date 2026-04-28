# --- LOGICA SCHNEIDER (Basata su schneider_decoder.docx) ---
    elif brand == "SCHNEIDER" and is_mcb:
        c1, c2 = st.columns(2)
        
        with c1:
            # Selezione Famiglia (POS.3)
            famiglia_val = st.selectbox(
                "Famiglia (POS.3)",
                ["F = iC60", "P = iC40", "N = C120 / NG125"]
            )
            famiglia_code = famiglia_val[0]

            # Vincoli dinamici per PDI (POS.4) basati sulla Famiglia
            if famiglia_code == "P": # iC40
                pdi_opts = {"4.5 kA (versione a)": "4", "6 kA (versione N)": "5", "10 kA (versione H)": "6"}
            elif famiglia_code == "N": # NG125
                pdi_opts = {"25 kA (versione a)": "2", "36 kA (versione N)": "3", "70 kA (versione H)": "4", "100 kA (versione L)": "5"}
            else: # iC60
                pdi_opts = {"6 kA (versione a)": "4", "10 kA (versione N)": "7", "15 kA (versione H)": "8", "25 kA (versione L)": "9"}
            
            pdi_val = st.selectbox("Potere di Interruzione (POS.4)", list(pdi_opts.keys()))
            p_code = pdi_opts[pdi_val]

        with c2:
            # Curva di intervento (POS.5)
            curva_val = st.selectbox(
                "Curva di intervento (POS.5)",
                ["Curva B (3–5 In)", "Curva C (5–10 In)", "Curva D (10–14 In)", "Curva Z (3 In)", "Curva MA (solo magnetico)"]
            )
            curv_map = {"Curva B (3–5 In)": "3", "Curva C (5–10 In)": "4", "Curva D (10–14 In)": "5", "Curva Z (3 In)": "2", "Curva MA (solo magnetico)": "0"}
            c_code = curv_map.get(curva_val)

            # Poli (POS.6) - Vincolo iC40
            if famiglia_code == "P":
                pol_opts = {"1P+N": "6", "3P+N": "7"}
            else:
                pol_opts = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
            
            poli_sel = st.selectbox("Poli (POS.6)", list(pol_opts.keys()))
            pol_code = pol_opts[poli_sel]

            # Corrente (POS.7-8) - Vincolo Amperaggio
            if famiglia_code == "N":
                amp_list = ["10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A", "80A", "100A", "125A"]
            else:
                amp_list = ["0.5A", "1A", "2A", "3A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
            
            amp_val = st.selectbox("Corrente nominale In (POS.7-8)", amp_list)
            
            # Formattazione corrente
            amp_raw = amp_val.replace("A", "")
            if amp_raw == "0.5":
                amp_fixed = "70"
            else:
                amp_fixed = amp_raw.zfill(2)

        # Generazione Codice Finale
        codice_final = f"A9{famiglia_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        
        pos_data = [
            ("1-2", "A9"), ("3", famiglia_code), ("4", p_code), 
            ("5", c_code), ("6", pol_code), ("7-8", amp_fixed)
        ]
        url_base = "https://www.se.com/it/it/search/"

    # --- LOGICA HAGER ---
    elif brand == "HAGER" and is_mcb:
        c1, c2 = st.columns(2)
        with c1:
            # ... continua il codice Hager qui ...
            pass
