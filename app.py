import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Configuratore Siemens 5SV", page_icon="⚡")

# --- COSTANTI E MAPPATURE ---
DESCRIZIONI_TIPI = {
    "0": "Tipo AC (Correnti alternate sinusoidali)",
    "6": "Tipo A (Alternate e pulsanti unidirezionali)",
    "3": "Tipo F (Frequenze miste, es. inverter monofase)",
    "4": "Tipo B (Universale, anche correnti continue)"
}

# --- FUNZIONI DI CALCOLO ---
def genera_scheda_tecnica(codice, es, se, po, co, ti, tipo_k):
    es_label = {"3": "Top", "4": "Standard", "5": "Residenziale"}[es]
    se_label = {"1": "10 mA", "3": "30 mA", "6": "300 mA", "8": "1 A"}[se]
    po_label = {"1": "1P+N (2 moduli)", "4": "3P+N (4 moduli)"}[po]
    co_label = {"1": "16 A", "2": "25 A", "4": "40 A", "6": "63 A"}[co]
    ti_label = DESCRIZIONI_TIPI[ti]
    
    scheda = f"""
    **Scheda Tecnica Siemens SENTRON**
    - **Serie:** 5SV (Differenziale Puro)
    - **Esecuzione:** {es_label}
    - **Sensibilità (IΔn):** {se_label}
    - **Poli:** {po_label}
    - **Corrente Nominale (In):** {co_label}
    - **Classe:** {ti_label}
    """
    if tipo_k:
        scheda += "- **Special:** Tipo K (Superimmunizzato)"
    
    return scheda

# --- INTERFACCIA UTENTE ---
st.title("⚡ Configuratore Codici Siemens 5SV")
st.markdown("Generatore di codici d'ordinazione basato su catalogo SENTRON.")

with st.sidebar:
    st.header("Parametri di Configurazione")
    
    # 1. Esecuzione
    esecuzione = st.selectbox(
        "Ambiente di Installazione (Esecuzione):",
        options=["3", "4", "5"],
        format_func=lambda x: {"3": "3 - Top", "4": "4 - Standard", "5": "5 - Residenziale"}[x]
    )

    # 2. Sensibilità
    sensibilita = st.selectbox(
        "Soglia di Intervento (IΔn):",
        options=["1", "3", "6", "8"],
        format_func=lambda x: {"1": "10 mA", "3": "30 mA", "6": "300 mA", "8": "1 A"}[x]
    )

    # 3. Poli
    poli = st.radio(
        "Numero Poli:",
        options=["1", "4"],
        format_func=lambda x: "1P+N (Monofase)" if x == "1" else "3P+N (Trifase)"
    )

    # 4. Corrente Nominale
    corrente = st.selectbox(
        "Corrente Nominale (In):",
        options=["1", "2", "4", "6"],
        format_func=lambda x: {"1": "16 A", "2": "25 A", "4": "40 A", "6": "63 A"}[x]
    )

    # 5. Tipologia (con vincolo per Residenziale)
    opzioni_tipo = ["0", "6", "3", "4"]
    if esecuzione == "5":
        st.warning("Nota: Per la serie Residenziale è disponibile solo il Tipo AC.")
        opzioni_tipo = ["0"]

    tipologia = st.selectbox(
        "Tipologia di Differenziale:",
        options=opzioni_tipo,
        format_func=lambda x: DESCRIZIONI_TIPI[x]
    )

    # 6. Opzioni Speciali
    tipo_k = st.checkbox("Richiedi Tipo K (Superimmunizzato)")

# --- LOGICA DI GENERAZIONE ---
# Costruzione: 5SV + ES + SE + PO + CO + "-" + TI
codice_finale = f"5SV{esecuzione}{sensibilita}{poli}{corrente}-{tipologia}"

if tipo_k:
    codice_finale += "KK01"

# --- OUTPUT ---
st.divider()
st.subheader("Codice d'Ordinazione Generato:")
st.code(codice_finale, language="text")

# Descrizione specifica richiesta dal prompt
if codice_finale.startswith("5SV3314-6"):
    st.info("**Descrizione Catalogo:** Interruttore differenziale puro, Tipo A, 30mA, 1P+N, 40A")

# Visualizzazione Scheda Tecnica
with st.expander("Visualizza Scheda Tecnica Completa", expanded=True):
    scheda_txt = genera_scheda_tecnica(codice_finale, esecuzione, sensibilita, poli, corrente, tipologia, tipo_k)
    st.markdown(scheda_txt)

# Note di validazione aggiuntive
st.caption("I codici generati devono essere verificati sul catalogo ufficiale Siemens prima dell'acquisto.")
