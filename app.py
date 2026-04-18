# --- 1. MAGNETOTERMICI STANDARD (Correzione IF) ---
if categoria.startswith("Magnetotermici (5SL"):  # <--- CORRETTO
    c1, c2 = st.columns(2)
    with c1:
        pdi = st.selectbox("Potere Interruzione", ["4.5 kA", "6 kA", "10 kA", "15 kA", "25 kA"])
        poli = st.selectbox("Poli", ["1P", "2P", "3P", "4P"]) # Semplificato per logica multibrand
    with c2:
        amp = st.selectbox("Corrente (In)", ["06", "10", "16", "20", "25", "32", "40", "50", "63"])
        curva = st.radio("Curva", ["B", "C", "D"], horizontal=True)

    # --- LOGICA SCHNEIDER (Basata su catalogo Acti9) ---
    if "Schneider" in brand:
        # Mappatura Codici Parlanti Schneider
        pdi_map = {"4.5 kA": "64", "6 kA": "74", "10 kA": "74", "15 kA": "84", "25 kA": "94"}
        poli_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
        
        # Prefisso: A9F per magnetotermici
        # Esempio: A9F + 74 (PDI) + 1 (Poli) + 16 (Amp)
        codice_final = f"A9F{pdi_map[pdi]}{poli_map[poli]}{amp}"

    # --- LOGICA SIEMENS ---
    elif "SIEMENS" in brand:
        pref = "5SL3" if "4.5" in pdi else "5SL6" if "6" in pdi else "5SL4" if "10" in pdi else "5SY7" if "15" in pdi else "5SY8"
        p_map = {"1P": "1", "2P": "2", "3P": "3", "4P": "4"}
        codice_final = f"{pref}{p_map[poli]}{amp}-{curva[0]}{amp}"

    # --- LOGICA ABB ---
    elif "ABB" in brand:
        pref_abb = "S200L" if "4.5" in pdi else "S200" if "6" in pdi else "S200M" if "10" in pdi else "S200P"
        p_val = poli[0] # Prende il primo carattere (1, 2, 3, 4)
        codice_final = f"{pref_abb}-{curva[0]}{int(amp)}"
