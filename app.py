"""
Reverse Engineering Tool per Codici Prodotto Industriali
=========================================================
Streamlit app brand-agnostic che ricostruisce codici prodotto
leggendo la logica esclusivamente dal file Excel di mappatura.

Requisiti:
    pip install streamlit pandas openpyxl requests

Avvio:
    streamlit run reverse_engineering_tool.py
"""

import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# ─────────────────────────────────────────────
#  CONFIGURAZIONE
# ─────────────────────────────────────────────
# Sostituisci con l'URL Raw del tuo file su GitHub:
# es. https://raw.githubusercontent.com/utente/repo/main/mapping.xlsx
DEFAULT_EXCEL_URL = (
    "https://raw.githubusercontent.com/your-user/your-repo/main/product_code_mapping.xlsx"
)

PLACEHOLDER_CHAR = "_"   # Carattere usato per posizioni non definite


# ─────────────────────────────────────────────
#  CARICAMENTO DATI (con cache)
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="Caricamento dati dal repository…")
def load_excel_from_url(url: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Scarica e carica i fogli 'Mappatura' e 'BlackList' dall'URL fornito."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        raw = BytesIO(response.content)
    except Exception as e:
        st.error(f"❌ Impossibile scaricare il file Excel: {e}")
        st.stop()

    try:
        df_map = pd.read_excel(raw, sheet_name="Mappatura", dtype=str)
        df_map = df_map.fillna("")
        df_map["Posizione"] = pd.to_numeric(df_map["Posizione"], errors="coerce").fillna(0).astype(int)
        df_map["Lunghezza_Totale_Codice"] = pd.to_numeric(
            df_map["Lunghezza_Totale_Codice"], errors="coerce"
        ).fillna(0).astype(int)
    except Exception as e:
        st.error(f"❌ Errore nel foglio 'Mappatura': {e}")
        st.stop()

    raw.seek(0)
    try:
        df_bl = pd.read_excel(raw, sheet_name="BlackList", dtype=str).fillna("")
    except Exception:
        df_bl = pd.DataFrame(columns=["Brand", "Applicazione", "Caratteristica", "Valore", "Motivo"])

    return df_map, df_bl


@st.cache_data(show_spinner=False)
def load_excel_from_upload(file_bytes: bytes) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carica i fogli dal file caricato dall'utente."""
    raw = BytesIO(file_bytes)
    try:
        df_map = pd.read_excel(raw, sheet_name="Mappatura", dtype=str).fillna("")
        df_map["Posizione"] = pd.to_numeric(df_map["Posizione"], errors="coerce").fillna(0).astype(int)
        df_map["Lunghezza_Totale_Codice"] = pd.to_numeric(
            df_map["Lunghezza_Totale_Codice"], errors="coerce"
        ).fillna(0).astype(int)
    except Exception as e:
        st.error(f"❌ Errore nel foglio 'Mappatura': {e}")
        st.stop()

    raw.seek(0)
    try:
        df_bl = pd.read_excel(raw, sheet_name="BlackList", dtype=str).fillna("")
    except Exception:
        df_bl = pd.DataFrame(columns=["Brand", "Applicazione", "Caratteristica", "Valore", "Motivo"])

    return df_map, df_bl


# ─────────────────────────────────────────────
#  LOGICA DI RICOSTRUZIONE CODICE  (brand-agnostic)
# ─────────────────────────────────────────────
def build_code(selections: dict[str, str], brand_df: pd.DataFrame) -> tuple[str, str]:
    """
    Ricostruisce il codice finale inserendo ogni Codice_Parziale
    nella Posizione indicata nel file Excel.

    Restituisce (codice_finale, url_base).
    La logica è completamente guidata dai dati: nessuna regola hard-coded.
    """
    # Determina la lunghezza massima del codice per questo brand/app
    total_len = int(brand_df["Lunghezza_Totale_Codice"].max())
    if total_len <= 0:
        total_len = 32

    # Array di caratteri segnaposto
    code_chars: list[str] = [PLACEHOLDER_CHAR] * total_len

    url_base = ""

    for caratteristica, valore in selections.items():
        subset = brand_df[
            (brand_df["Caratteristica"] == caratteristica) &
            (brand_df["Valore"] == valore)
        ]
        if subset.empty:
            continue

        row = subset.iloc[0]
        partial_code: str = str(row["Codice_Parziale"])
        position: int = int(row["Posizione"])  # 1-based
        url_base = str(row["URL_Ricerca_Base"]) if row["URL_Ricerca_Base"] else url_base

        # Inserisce il codice parziale dalla posizione indicata (1-based → 0-based)
        start = position - 1
        for i, ch in enumerate(partial_code):
            idx = start + i
            if idx < total_len:
                code_chars[idx] = ch
            else:
                # Estendi se il codice parziale supera la lunghezza prevista
                code_chars.append(ch)

    final_code = "".join(code_chars)
    return final_code, url_base


def is_blacklisted(brand: str, applicazione: str, caratteristica: str, valore: str,
                   df_bl: pd.DataFrame) -> bool:
    """Verifica se una combinazione è presente nella BlackList."""
    mask = (
        (df_bl["Brand"] == brand) &
        (df_bl["Applicazione"] == applicazione) &
        (df_bl["Caratteristica"] == caratteristica) &
        (df_bl["Valore"] == valore)
    )
    return bool(mask.any())


# ─────────────────────────────────────────────
#  PAGINA PRINCIPALE
# ─────────────────────────────────────────────
def main():
    # ── Page config ──────────────────────────
    st.set_page_config(
        page_title="RE Tool – Codici Prodotto",
        page_icon="🔩",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ── CSS personalizzato ────────────────────
    st.markdown("""
    <style>
        /* Palette industriale */
        :root {
            --accent: #0066CC;
            --accent-light: #E8F0FE;
            --success: #00875A;
            --warning: #FF8B00;
            --danger: #DE350B;
            --bg-card: #F4F5F7;
            --border: #DFE1E6;
        }
        .main .block-container { padding-top: 1.5rem; }

        /* Card risultato */
        .code-card {
            background: var(--accent-light);
            border-left: 4px solid var(--accent);
            border-radius: 6px;
            padding: 1rem 1.4rem;
            margin: 0.8rem 0;
        }
        .code-display {
            font-family: 'Courier New', Courier, monospace;
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: 0.15em;
            word-break: break-all;
        }
        /* Badge brand */
        .brand-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            background: var(--accent);
            color: white;
            margin-bottom: 0.3rem;
        }
        /* Sezione caratteristiche */
        .char-section {
            background: white;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        /* Info blacklist */
        .bl-info {
            background: #FFF4E6;
            border-left: 3px solid var(--warning);
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            font-size: 0.82rem;
            color: #7A5200;
        }
        /* Responsive: su mobile riduce padding */
        @media (max-width: 640px) {
            .code-display { font-size: 1.1rem; letter-spacing: 0.08em; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ── Sidebar: Sorgente dati ────────────────
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/48/engineering.png", width=48)
        st.title("⚙️ RE Tool")
        st.caption("Reverse Engineering Codici Prodotto Industriali")
        st.divider()

        st.subheader("📂 Sorgente Dati")
        source = st.radio(
            "Carica da:",
            ["URL GitHub (Raw)", "File locale"],
            horizontal=True,
        )

        df_map: pd.DataFrame
        df_bl: pd.DataFrame

        if source == "URL GitHub (Raw)":
            url = st.text_input(
                "URL Raw GitHub",
                value=DEFAULT_EXCEL_URL,
                help="URL diretto al file .xlsx su GitHub (raw.githubusercontent.com)",
            )
            if st.button("🔄 Ricarica dati", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
            df_map, df_bl = load_excel_from_url(url)
        else:
            uploaded = st.file_uploader(
                "Carica file Excel", type=["xlsx"],
                help="Il file deve avere i fogli 'Mappatura' e 'BlackList'"
            )
            if uploaded is None:
                st.info("⬆️ Carica un file Excel per iniziare.")
                st.stop()
            df_map, df_bl = load_excel_from_upload(uploaded.read())

        st.divider()
        st.caption(f"📊 **{len(df_map)}** righe mappatura · **{len(df_bl)}** blacklist")

        with st.expander("📋 Anteprima BlackList"):
            st.dataframe(df_bl, use_container_width=True, height=180)

    # ── Titolo principale ─────────────────────
    st.markdown("## 🔩 Reverse Engineering – Codici Prodotto Industriali")
    st.markdown(
        "Seleziona le caratteristiche in cascata: il sistema ricostruisce "
        "automaticamente il codice ordine e genera il link di ricerca."
    )
    st.divider()

    # ── Layout a 2 colonne ────────────────────
    col_sel, col_out = st.columns([1, 1], gap="large")

    with col_sel:
        st.markdown("### 🎛️ Configuratore")

        # ── Filtro 1: Categoria ───────────────
        categorie = sorted(df_map["Categoria"].unique().tolist())
        if not categorie:
            st.warning("Nessuna categoria trovata nel file Excel.")
            st.stop()

        categoria = st.selectbox("1️⃣ Categoria", categorie)

        # ── Filtro 2: Brand ───────────────────
        brands = sorted(df_map[df_map["Categoria"] == categoria]["Brand"].unique().tolist())
        if not brands:
            st.warning("Nessun Brand per questa Categoria.")
            st.stop()

        brand = st.selectbox("2️⃣ Brand", brands)

        # ── Filtro 3: Applicazione ────────────
        applicazioni = sorted(
            df_map[
                (df_map["Categoria"] == categoria) &
                (df_map["Brand"] == brand)
            ]["Applicazione"].unique().tolist()
        )
        if not applicazioni:
            st.warning("Nessuna Applicazione disponibile.")
            st.stop()

        applicazione = st.selectbox("3️⃣ Applicazione", applicazioni)

        # ── Filtro brand/app: sottoinsieme ────
        app_df = df_map[
            (df_map["Brand"] == brand) &
            (df_map["Applicazione"] == applicazione)
        ].copy()

        # ── Caratteristiche dinamiche ─────────
        caratteristiche = sorted(app_df["Caratteristica"].unique().tolist())

        st.markdown("---")
        st.markdown("#### 🔧 Caratteristiche Tecniche")

        selections: dict[str, str] = {}
        blacklisted_count = 0

        for caratteristica in caratteristiche:
            valori_raw = sorted(
                app_df[app_df["Caratteristica"] == caratteristica]["Valore"].unique().tolist()
            )

            # Filtra blacklist
            valori_visibili = [
                v for v in valori_raw
                if not is_blacklisted(brand, applicazione, caratteristica, v, df_bl)
            ]
            bl_hidden = len(valori_raw) - len(valori_visibili)
            blacklisted_count += bl_hidden

            if not valori_visibili:
                st.markdown(
                    f'<div class="bl-info">⚠️ <b>{caratteristica}</b>: '
                    f'tutti i valori sono in BlackList</div>',
                    unsafe_allow_html=True,
                )
                continue

            with st.container():
                col_lbl, col_info = st.columns([3, 1])
                with col_lbl:
                    valore = st.selectbox(
                        f"**{caratteristica}**",
                        valori_visibili,
                        key=f"sel_{brand}_{applicazione}_{caratteristica}",
                    )
                with col_info:
                    if bl_hidden > 0:
                        st.markdown(
                            f'<div class="bl-info" style="margin-top:1.8rem">'
                            f'🚫 {bl_hidden} nascosti</div>',
                            unsafe_allow_html=True,
                        )
                selections[caratteristica] = valore

        if blacklisted_count > 0:
            st.caption(f"🚫 {blacklisted_count} opzioni totali nascoste dalla BlackList")

    # ── Output: codice generato ───────────────
    with col_out:
        st.markdown("### 📦 Codice Generato")

        if not selections:
            st.info("👈 Seleziona almeno una caratteristica per generare il codice.")
        else:
            final_code, url_base = build_code(selections, app_df)
            has_placeholder = PLACEHOLDER_CHAR in final_code

            st.markdown(
                f'<span class="brand-badge">{brand}</span>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="code-card">'
                f'<div style="font-size:0.8rem;color:#666;margin-bottom:4px;">'
                f'{categoria} · {applicazione}</div>'
                f'<div class="code-display">{final_code}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if has_placeholder:
                st.warning(
                    f"⚠️ Il codice contiene caratteri segnaposto `{PLACEHOLDER_CHAR}` "
                    "nelle posizioni non ancora definite. Completa la selezione."
                )

            # ── Link di ricerca ───────────────
            if url_base:
                search_url = url_base + final_code
                st.markdown(
                    f"🔗 **[Cerca su portale del fornitore]({search_url})**",
                    unsafe_allow_html=True,
                )
                st.caption(f"`{search_url}`")
            else:
                st.caption("(Nessun URL_Ricerca_Base definito per questo Brand/Applicazione)")

            # ── Copy box ─────────────────────
            st.text_input("📋 Copia codice:", value=final_code, key="code_copy")

            st.divider()

            # ── Riepilogo selezioni ───────────
            st.markdown("#### 📝 Riepilogo Selezioni")
            riepilogo = []
            for car, val in selections.items():
                subset = app_df[
                    (app_df["Caratteristica"] == car) & (app_df["Valore"] == val)
                ]
                codice_p = subset.iloc[0]["Codice_Parziale"] if not subset.empty else "—"
                posizione = subset.iloc[0]["Posizione"] if not subset.empty else "—"
                riepilogo.append({
                    "Caratteristica": car,
                    "Valore Selezionato": val,
                    "Codice Parziale": codice_p,
                    "Posizione": posizione,
                })

            df_riepilogo = pd.DataFrame(riepilogo)
            st.dataframe(df_riepilogo, use_container_width=True, hide_index=True)

            # ── Visualizzazione struttura codice ──
            st.markdown("#### 🧬 Struttura Codice")
            total_len = int(app_df["Lunghezza_Totale_Codice"].max())
            if total_len > 0:
                rows_struct = []
                for i, ch in enumerate(final_code[:total_len], 1):
                    is_ph = ch == PLACEHOLDER_CHAR
                    rows_struct.append({
                        "Pos": i,
                        "Char": ch,
                        "Tipo": "⬜ Libero" if is_ph else "🔷 Definito",
                    })
                df_struct = pd.DataFrame(rows_struct)
                st.dataframe(
                    df_struct,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Pos": st.column_config.NumberColumn("Pos", width=60),
                        "Char": st.column_config.TextColumn("Char", width=60),
                        "Tipo": st.column_config.TextColumn("Tipo"),
                    },
                    height=min(35 * total_len + 38, 400),
                )

    # ── Footer ────────────────────────────────
    st.divider()
    st.caption(
        "🔩 RE Tool · Reverse Engineering Codici Prodotto Industriali · "
        "Brand-Agnostic · Logica completamente guidata dal file Excel"
    )


if __name__ == "__main__":
    main()
