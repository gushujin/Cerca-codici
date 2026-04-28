"""
Reverse Engineering Tool per Codici Prodotto Industriali
=========================================================
Adattato al file Master_Data.xlsx con fogli:
  - Ambiti    : Brand | Ambito_Utente | Famiglia_Sistema
  - Mapping   : Brand | Famiglia | Parametro | Valore_Reale | Segmento_Codice | Posizione | URL_Base
  - Blacklist : Brand | Famiglia | Parametro | Valore_da_Escludere
  - Legenda   : Poli | Pdi | Corrente | Curva

LOGICA POSIZIONE: la colonna Posizione indica l'ordine di concatenazione
dei segmenti (1=primo, 2=secondo, …), NON un indice di carattere.
Il codice finale = segmenti ordinati per Posizione e concatenati.

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
DEFAULT_EXCEL_URL = (
    "https://raw.githubusercontent.com/your-user/your-repo/main/Master_Data.xlsx"
)
PLACEHOLDER_CHAR = "?"   # Carattere per parametri non ancora selezionati


# ─────────────────────────────────────────────
#  CARICAMENTO DATI
# ─────────────────────────────────────────────
def _parse_workbook(raw: BytesIO):
    df_ambiti = pd.read_excel(raw, sheet_name="Ambiti", dtype=str).fillna("")

    raw.seek(0)
    df_map = pd.read_excel(raw, sheet_name="Mapping", dtype=str).fillna("")
    df_map["Posizione"] = (
        pd.to_numeric(df_map["Posizione"], errors="coerce").fillna(0).astype(int)
    )

    raw.seek(0)
    try:
        df_bl = pd.read_excel(raw, sheet_name="Blacklist", dtype=str).fillna("")
    except Exception:
        df_bl = pd.DataFrame(
            columns=["Brand", "Famiglia", "Parametro", "Valore_da_Escludere"]
        )

    raw.seek(0)
    try:
        df_leg = pd.read_excel(raw, sheet_name="Legenda", dtype=str).fillna("")
    except Exception:
        df_leg = pd.DataFrame()

    return df_ambiti, df_map, df_bl, df_leg


@st.cache_data(show_spinner="Caricamento dati dal repository…")
def load_from_url(url: str):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        st.error(f"❌ Impossibile scaricare il file: {e}")
        st.stop()
    return _parse_workbook(BytesIO(r.content))


@st.cache_data(show_spinner=False)
def load_from_upload(file_bytes: bytes):
    return _parse_workbook(BytesIO(file_bytes))


# ─────────────────────────────────────────────
#  LOGICA BRAND-AGNOSTIC
# ─────────────────────────────────────────────
def build_code(selections: dict, famiglia_df: pd.DataFrame) -> tuple:
    """
    Ricostruisce il codice concatenando i Segmento_Codice
    nell'ordine indicato dalla colonna Posizione (1, 2, 3, …).

    Se un parametro non è presente in selections (non ancora scelto),
    viene inserito un placeholder.

    Restituisce (codice_finale, url_base, lista_slot).
    """
    # Raccoglie tutti i parametri distinti della famiglia con la loro posizione
    slot_df = (
        famiglia_df[["Parametro", "Posizione"]]
        .drop_duplicates("Parametro")
        .sort_values("Posizione")
    )

    url_base = ""
    segmenti = []       # lista di (posizione, segmento_stringa, parametro, valore)

    for _, slot in slot_df.iterrows():
        parametro = slot["Parametro"]
        posizione = int(slot["Posizione"])
        valore = selections.get(parametro)

        if valore is None:
            segmenti.append((posizione, PLACEHOLDER_CHAR, parametro, "—"))
            continue

        row = famiglia_df[
            (famiglia_df["Parametro"] == parametro) &
            (famiglia_df["Valore_Reale"] == valore)
        ]
        if row.empty:
            segmenti.append((posizione, PLACEHOLDER_CHAR, parametro, valore))
            continue

        r = row.iloc[0]
        seg = str(r["Segmento_Codice"])
        url_base = str(r["URL_Base"]) if r["URL_Base"] else url_base
        segmenti.append((posizione, seg, parametro, valore))

    # Codice finale = concatenazione in ordine di posizione
    final_code = "".join(s[1] for s in segmenti)
    return final_code, url_base, segmenti


def is_blacklisted(brand: str, famiglia: str, parametro: str,
                   valore: str, df_bl: pd.DataFrame) -> bool:
    mask = (
        (df_bl["Brand"] == brand) &
        (df_bl["Famiglia"] == famiglia) &
        (df_bl["Parametro"] == parametro) &
        (df_bl["Valore_da_Escludere"] == valore)
    )
    return bool(mask.any())


# ─────────────────────────────────────────────
#  APP PRINCIPALE
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="RE Tool – Codici Prodotto",
        page_icon="🔩",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
    <style>
        :root {
            --accent: #0066CC;
            --accent-light: #E8F0FE;
            --warning-bg: #FFF4E6;
            --warning-border: #FF8B00;
            --warning-text: #7A5200;
            --border: #DFE1E6;
        }
        .main .block-container { padding-top: 1.5rem; }
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
            letter-spacing: 0.18em;
            word-break: break-all;
        }
        .code-display .seg-placeholder {
            color: #CC3300;
            opacity: 0.7;
        }
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
        .bl-info {
            background: var(--warning-bg);
            border-left: 3px solid var(--warning-border);
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            font-size: 0.82rem;
            color: var(--warning-text);
            margin-bottom: 0.4rem;
        }
        .prefisso-info {
            background: #EEF4FF;
            border-left: 3px solid #0066CC;
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            font-size: 0.82rem;
            color: #003580;
            margin-bottom: 0.4rem;
        }
        @media (max-width: 640px) {
            .code-display { font-size: 1.1rem; letter-spacing: 0.08em; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/48/engineering.png", width=48)
        st.title("⚙️ RE Tool")
        st.caption("Reverse Engineering Codici Prodotto Industriali")
        st.divider()

        st.subheader("📂 Sorgente Dati")
        source = st.radio("Carica da:", ["URL GitHub (Raw)", "File locale"], horizontal=True)

        if source == "URL GitHub (Raw)":
            url = st.text_input("URL Raw GitHub", value=DEFAULT_EXCEL_URL)
            if st.button("🔄 Ricarica dati", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
            df_ambiti, df_map, df_bl, df_leg = load_from_url(url)
        else:
            uploaded = st.file_uploader(
                "Carica Master_Data.xlsx", type=["xlsx"],
                help="Fogli richiesti: Ambiti, Mapping, Blacklist, Legenda"
            )
            if uploaded is None:
                st.info("⬆️ Carica il file Master_Data.xlsx per iniziare.")
                st.stop()
            df_ambiti, df_map, df_bl, df_leg = load_from_upload(uploaded.read())

        st.divider()
        st.caption(
            f"📊 **{len(df_map)}** righe mapping · "
            f"**{len(df_bl)}** blacklist · "
            f"**{len(df_ambiti)}** famiglie"
        )

        if not df_leg.empty:
            with st.expander("📖 Legenda valori"):
                st.dataframe(df_leg, use_container_width=True, hide_index=True)

        with st.expander("🚫 Blacklist attiva"):
            st.dataframe(df_bl, use_container_width=True, height=200, hide_index=True)

    # ── Header ────────────────────────────────
    st.markdown("## 🔩 Reverse Engineering – Codici Prodotto Industriali")
    st.markdown(
        "Seleziona **Brand → Ambito → Famiglia**, poi configura i parametri: "
        "il codice viene ricostruito automaticamente in tempo reale."
    )
    st.divider()

    col_sel, col_out = st.columns([1, 1], gap="large")

    with col_sel:
        st.markdown("### 🎛️ Configuratore")

        # ── 1: Brand ─────────────────────────
        brands = sorted(df_ambiti["Brand"].unique().tolist())
        if not brands:
            st.warning("Nessun Brand trovato nel foglio Ambiti.")
            st.stop()
        brand = st.selectbox("1️⃣ Brand", brands)

        # ── 2: Ambito_Utente ──────────────────
        ambiti = sorted(
            df_ambiti[df_ambiti["Brand"] == brand]["Ambito_Utente"].unique().tolist()
        )
        if not ambiti:
            st.warning("Nessun Ambito per questo Brand.")
            st.stop()
        ambito = st.selectbox("2️⃣ Ambito di utilizzo", ambiti)

        # ── 3: Famiglia_Sistema ───────────────
        famiglie = sorted(
            df_ambiti[
                (df_ambiti["Brand"] == brand) &
                (df_ambiti["Ambito_Utente"] == ambito)
            ]["Famiglia_Sistema"].unique().tolist()
        )
        if not famiglie:
            st.warning("Nessuna Famiglia per questo Ambito.")
            st.stop()
        famiglia = st.selectbox("3️⃣ Famiglia Sistema", famiglie)

        # Sottoinsieme Mapping per brand + famiglia
        fam_df = df_map[
            (df_map["Brand"] == brand) &
            (df_map["Famiglia"] == famiglia)
        ].copy()

        if fam_df.empty:
            st.warning(f"Nessun dato di mapping per **{brand} / {famiglia}**.")
            st.stop()

        # ── Parametri tecnici dinamici ────────
        # Ordine: per Posizione crescente (Prefisso ha Pos=1, viene sempre per primo)
        parametri_order = (
            fam_df[["Parametro", "Posizione"]]
            .drop_duplicates("Parametro")
            .sort_values("Posizione")["Parametro"]
            .tolist()
        )

        st.markdown("---")
        st.markdown("#### 🔧 Parametri Tecnici")

        selections = {}
        blacklisted_count = 0

        for parametro in parametri_order:
            valori_raw = sorted(
                fam_df[fam_df["Parametro"] == parametro]["Valore_Reale"].unique().tolist()
            )

            # Filtra blacklist
            valori_visibili = [
                v for v in valori_raw
                if not is_blacklisted(brand, famiglia, parametro, v, df_bl)
            ]
            bl_hidden = len(valori_raw) - len(valori_visibili)
            blacklisted_count += bl_hidden

            if not valori_visibili:
                st.markdown(
                    f'<div class="bl-info">⚠️ <b>{parametro}</b>: '
                    f'tutti i valori sono in Blacklist</div>',
                    unsafe_allow_html=True,
                )
                continue

            # Prefisso fisso (unico valore) → etichetta, nessun selectbox
            if parametro == "Prefisso" and len(valori_visibili) == 1:
                selections[parametro] = valori_visibili[0]
                seg = fam_df[
                    (fam_df["Parametro"] == "Prefisso") &
                    (fam_df["Valore_Reale"] == valori_visibili[0])
                ].iloc[0]["Segmento_Codice"]
                st.markdown(
                    f'<div class="prefisso-info">'
                    f'🔒 <b>Prefisso</b> (Pos. 1): <code>{seg}</code>'
                    f' — {valori_visibili[0]}</div>',
                    unsafe_allow_html=True,
                )
                continue

            col_lbl, col_info = st.columns([3, 1])
            with col_lbl:
                valore = st.selectbox(
                    f"**{parametro}**",
                    valori_visibili,
                    key=f"sel_{brand}_{famiglia}_{parametro}",
                )
            with col_info:
                if bl_hidden > 0:
                    st.markdown(
                        f'<div class="bl-info" style="margin-top:1.8rem">'
                        f'🚫 {bl_hidden} nascosti</div>',
                        unsafe_allow_html=True,
                    )
            selections[parametro] = valore

        if blacklisted_count > 0:
            st.caption(f"🚫 **{blacklisted_count}** opzioni totali nascoste dalla Blacklist")

    # ── Output ────────────────────────────────
    with col_out:
        st.markdown("### 📦 Codice Generato")

        if not selections:
            st.info("👈 Seleziona i parametri per generare il codice.")
        else:
            final_code, url_base, segmenti = build_code(selections, fam_df)
            has_placeholder = PLACEHOLDER_CHAR in final_code

            st.markdown(f'<span class="brand-badge">{brand}</span>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="code-card">'
                f'<div style="font-size:0.8rem;color:#666;margin-bottom:4px;">'
                f'{ambito} · {famiglia}</div>'
                f'<div class="code-display">{final_code}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if has_placeholder:
                st.warning(
                    f"⚠️ Parametri mancanti (`{PLACEHOLDER_CHAR}`): "
                    "completa tutte le selezioni per ottenere il codice completo."
                )

            if url_base and not has_placeholder:
                search_url = url_base + final_code
                st.markdown(
                    f"🔗 **[Cerca sul portale del fornitore]({search_url})**",
                    unsafe_allow_html=True,
                )
                st.caption(f"`{search_url}`")
            elif url_base and has_placeholder:
                st.caption("🔗 Il link sarà disponibile quando il codice è completo.")
            else:
                st.caption("(URL_Base non definito per questa Famiglia)")

            st.text_input(
                "📋 Copia codice:",
                value=final_code,
                key="code_copy",
                disabled=has_placeholder,
            )
            st.divider()

            # Riepilogo segmenti in ordine di costruzione
            st.markdown("#### 📝 Struttura del Codice")
            riepilogo = []
            for pos, seg, par, val in segmenti:
                riepilogo.append({
                    "Pos.": pos,
                    "Parametro": par,
                    "Valore": val,
                    "Segmento": seg,
                    "Stato": "✅" if seg != PLACEHOLDER_CHAR else "⏳",
                })
            df_riepilogo = pd.DataFrame(riepilogo)
            st.dataframe(
                df_riepilogo,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Pos.":      st.column_config.NumberColumn("Pos.", width=55),
                    "Parametro": st.column_config.TextColumn("Parametro"),
                    "Valore":    st.column_config.TextColumn("Valore"),
                    "Segmento":  st.column_config.TextColumn("Segmento"),
                    "Stato":     st.column_config.TextColumn("Stato", width=60),
                },
            )

            # Visualizzazione composizione codice
            st.markdown("#### 🧬 Composizione")
            parts_html = ""
            colors = [
                "#0066CC", "#007A33", "#8B3A8B", "#CC6600",
                "#006699", "#993300", "#336600", "#660066",
            ]
            for i, (pos, seg, par, _) in enumerate(segmenti):
                color = colors[i % len(colors)]
                is_ph = seg == PLACEHOLDER_CHAR
                style = (
                    f"display:inline-block;padding:4px 6px;margin:2px;"
                    f"border-radius:4px;font-family:monospace;font-size:1.1rem;"
                    f"font-weight:700;letter-spacing:0.1em;"
                )
                if is_ph:
                    style += "background:#FFE4D6;color:#CC3300;border:1px dashed #CC3300;"
                else:
                    style += f"background:{color}18;color:{color};border:1px solid {color}44;"
                label = f'<div style="font-size:0.65rem;color:#888;text-align:center">{par}</div>'
                parts_html += f'<div style="display:inline-block;text-align:center;margin:2px">{label}<span style="{style}">{seg}</span></div>'

            st.markdown(
                f'<div style="background:#F8F9FA;border-radius:8px;padding:12px 10px;'
                f'border:1px solid #DFE1E6;margin-bottom:8px">{parts_html}</div>',
                unsafe_allow_html=True,
            )

    st.divider()
    st.caption(
        "🔩 RE Tool · Reverse Engineering Codici Prodotto · "
        "Brand-Agnostic · Master_Data.xlsx"
    )


if __name__ == "__main__":
    main()
