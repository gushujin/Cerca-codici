elif brand == "SCHNEIDER":
        c1, c2 = st.columns(2)
        
        with c1:
            # POS. 1-2: FAMIGLIA
            fam_code = st.selectbox("Famiglia (POS.1-2)", ["A9", "R9"])

            # POS. 3: SERIE
            serie_code = "F"
            st.text_input("Serie (POS.3)", value="F", disabled=True)

            # POS. 4: PDI
            pdi_val = st.selectbox("Potere Interruzione (PDI - POS.4)", ["6 kA", "10 kA", "15 kA"])
            pdi_map = {"6 kA": "7", "10 kA": "8", "15 kA": "9"}
            p_code = pdi_map[pdi_val]

            # SELEZIONE CORRENTE (In)
            amp_options = ["0,5A", "1A", "2A", "3A", "4A", "6A", "10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]
            amp_val = st.selectbox("Corrente (In - POS.7-8)", amp_options)
            current_numeric = float(amp_val.replace('A', '').replace(',', '.'))

        with c2:
            # POS. 6: POLI
            poli_val = st.selectbox("Poli (POS.6)", ["1P", "2P", "3P", "4P"])
            pol_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
            pol_code = pol_map[poli_val]

            # POS. 5: CURVA (Logica Interdipendente basata su In)
            curva_val = st.selectbox("Curva (POS.5)", ["B", "C", "D"])
            
            if curva_val == "B":
                c_code = "3" if current_numeric < 6 else "8"
            elif curva_val == "C":
                c_code = "4" if current_numeric < 6 else "9"
            else: # Curva D
                c_code = "5"

            # DEFINIZIONE POS. 7-8
            if current_numeric == 0.5:
                amp_fixed = "70"
            else:
                amp_fixed = f"{int(current_numeric):02d}"

        # COMPOSIZIONE FINALE E DATI PER LAYOUT COMUNE
        codice_final = f"{fam_code}{serie_code}{p_code}{c_code}{pol_code}{amp_fixed}"
        
        # Popoliamo pos_data per usare il layout grafico Siemens a fondo pagina
        pos_data = [
            ("1-2", fam_code), 
            ("3", serie_code), 
            ("4", p_code), 
            ("5", c_code), 
            ("6", pol_code), 
            ("7-8", amp_fixed)
        ]
        
        url_base = "https://www.se.com/it/it/search/"
