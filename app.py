import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime

GITHUB_RAW_DEFAULT = "https://raw.githubusercontent.com/meninosia2026-beep/aceleracao_vendas/main/data/alerta_aceleracao.csv"

st.set_page_config(
    page_title="Farol · Aceleração PAX",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;900&family=Archivo+Narrow:wght@400;500;600;700&display=swap');

:root {
  --pink:    #f11075;
  --pink-lt: #fff0f5;
  --pink-md: #ffd6e7;
  --bg:      #ffffff;
  --bg2:     #fafafa;
  --bg3:     #f4f4f6;
  --bdr:     #e8e8ed;
  --bdr2:    #d4d4db;
  --txt:     #0f0f14;
  --txt2:    #3a3a4a;
  --muted:   #8a8a9a;
  --green:   #00b96b;
  --red:     #f11075;
  --orange:  #f97316;
  --yellow:  #eab308;
  --blue:    #2563eb;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"] > div {
  background: var(--bg) !important;
  color: var(--txt) !important;
  font-family: 'Archivo', sans-serif !important;
}

[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--bdr) !important;
}
[data-testid="stSidebar"] * { color: var(--txt) !important; }
[data-testid="stSidebar"] h3 {
  font-family: 'Archivo', sans-serif !important;
  font-weight: 700 !important;
  font-size: .85rem !important;
  letter-spacing: .5px !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
}

.block-container { padding: 2rem 2.5rem !important; max-width: 100% !important; }
hr { border-color: var(--bdr) !important; }

[data-testid="stTextInput"] input {
  background: var(--bg) !important;
  border: 1px solid var(--bdr2) !important;
  border-radius: 6px !important;
  color: var(--txt) !important;
  font-family: 'Archivo Narrow', sans-serif !important;
  font-size: .85rem !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--pink) !important;
  box-shadow: 0 0 0 3px rgba(241,16,117,.1) !important;
}

[data-testid="stButton"] > button {
  background: var(--bg) !important;
  border: 1.5px solid var(--bdr2) !important;
  color: var(--txt2) !important;
  font-family: 'Archivo Narrow', sans-serif !important;
  font-size: .8rem !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  transition: all .15s !important;
}
[data-testid="stButton"] > button:hover {
  border-color: var(--pink) !important;
  color: var(--pink) !important;
  background: var(--pink-lt) !important;
}
[data-testid="stButton"] > button[kind="primary"] {
  background: var(--pink-lt) !important;
  border-color: var(--pink) !important;
  color: var(--pink) !important;
  font-weight: 700 !important;
}

/* multiselect */
[data-baseweb="tag"] {
  background: var(--pink-lt) !important;
  border: 1px solid var(--pink-md) !important;
}
[data-baseweb="tag"] span { color: var(--pink) !important; }

/* slider */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--pink) !important;
  border-color: var(--pink) !important;
}

/* ── HEADER ─────────────────────────── */
.farol-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding-bottom: 1.4rem;
  margin-bottom: 1.6rem;
  border-bottom: 2px solid var(--txt);
}
.header-left { display: flex; flex-direction: column; gap: 4px; }
.farol-eyebrow {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--pink);
}
.farol-title {
  font-family: 'Archivo', sans-serif;
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: -1px;
  color: var(--txt);
  line-height: 1;
}
.farol-sub {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .8rem;
  color: var(--muted);
  margin-top: 2px;
}
.upill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: var(--bg3);
  border: 1px solid var(--bdr2);
  border-radius: 20px;
  padding: 5px 14px;
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .72rem;
  font-weight: 600;
  color: var(--muted);
  white-space: nowrap;
}
.dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--green); display: inline-block;
  animation: pulse 2.5s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.25} }

/* ── KPI STRIP ──────────────────────── */
.kpi-strip {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
  margin-bottom: 2rem;
}
.kpi {
  background: var(--bg2);
  border: 1px solid var(--bdr);
  border-radius: 10px;
  padding: 14px 16px 12px;
  border-left: 4px solid var(--bdr2);
  transition: transform .15s, box-shadow .15s;
}
.kpi:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,.06);
}
.kpi-lbl {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .65rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 6px;
}
.kpi-val {
  font-family: 'Archivo', sans-serif;
  font-size: 2rem;
  font-weight: 900;
  line-height: 1;
  color: var(--txt);
}
.kpi.c-red    { border-left-color: var(--red);    }
.kpi.c-ora    { border-left-color: var(--orange);  }
.kpi.c-red2   { border-left-color: #ef4444;        }
.kpi.c-grn    { border-left-color: var(--green);   }
.kpi.c-yel    { border-left-color: var(--yellow);  }
.kpi.c-blu    { border-left-color: var(--blue);    }
.kpi.c-mut    { border-left-color: var(--bdr2);    }

/* ── CHART ──────────────────────────── */
.chart-wrap {
  background: var(--bg2);
  border: 1px solid var(--bdr);
  border-radius: 12px;
  padding: 22px 26px;
  margin-bottom: 1.8rem;
}
.chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.chart-col-title {
  font-family: 'Archivo', sans-serif;
  font-size: .85rem;
  font-weight: 700;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.chart-col-title::before {
  content: '';
  display: inline-block;
  width: 10px; height: 10px;
  border-radius: 2px;
}
.chart-col-title.up::before   { background: var(--green); }
.chart-col-title.down::before { background: var(--red);   }

.hbar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 7px; }
.hbar-lbl {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .72rem;
  font-weight: 600;
  color: var(--txt2);
  width: 76px;
  text-align: right;
  flex-shrink: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.hbar-date {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .6rem;
  color: var(--muted);
  display: block;
}
.hbar-track {
  flex: 1;
  height: 24px;
  background: var(--bg3);
  border-radius: 4px;
  overflow: hidden;
}
.hbar-fill {
  height: 100%;
  border-radius: 4px;
  display: flex;
  align-items: center;
}
.hbar-val {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .7rem;
  font-weight: 700;
  padding-left: 8px;
  color: #fff;
  white-space: nowrap;
}

/* ── TABLE ──────────────────────────── */
.tbl-wrap {
  overflow-x: auto;
  border: 1px solid var(--bdr);
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,.04);
}
.tbl { width: 100%; border-collapse: collapse; font-size: .81rem; }
.tbl thead tr { background: var(--bg3); }
.tbl th {
  padding: 11px 14px;
  border-bottom: 1px solid var(--bdr2);
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .63rem;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: left;
  white-space: nowrap;
}
.tbl td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--bdr);
  vertical-align: middle;
  white-space: nowrap;
  color: var(--txt);
}
.tbl tbody tr:hover td { background: var(--pink-lt); }
.tbl tbody tr:last-child td { border-bottom: none; }

.grp-sep td {
  background: var(--bg3) !important;
  padding: 6px 14px !important;
  font-family: 'Archivo Narrow', sans-serif !important;
  font-size: .65rem !important;
  font-weight: 700 !important;
  color: var(--txt2) !important;
  letter-spacing: .5px !important;
  text-transform: uppercase !important;
  border-bottom: 1px solid var(--bdr2) !important;
  border-top: 2px solid var(--bdr2) !important;
}

/* cells */
.rname {
  font-family: 'Archivo', sans-serif;
  font-weight: 700;
  font-size: .9rem;
  color: var(--txt);
  letter-spacing: -.3px;
}
.rsub {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .63rem;
  color: var(--muted);
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 4px;
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .67rem;
  font-weight: 700;
  white-space: nowrap;
  letter-spacing: .3px;
  text-transform: uppercase;
}
.b-urg { background: #fff0f5; color: var(--red);    border: 1px solid #ffd6e7; }
.b-atn { background: #fff7ed; color: var(--orange); border: 1px solid #fed7aa; }
.b-lot { background: #fef2f2; color: #ef4444;       border: 1px solid #fecaca; }
.b-opp { background: #f0fdf4; color: var(--green);  border: 1px solid #bbf7d0; }
.b-mon { background: #fefce8; color: #a16207;       border: 1px solid #fde68a; }
.b-des { background: #eff6ff; color: var(--blue);   border: 1px solid #bfdbfe; }
.b-nor { background: var(--bg3); color: var(--muted); border: 1px solid var(--bdr2); }

.spark { display: inline-flex; gap: 3px; align-items: flex-end; height: 24px; vertical-align: middle; }
.sb  { width: 7px; border-radius: 2px 2px 0 0; background: var(--bdr2); }
.su  { background: #86efac; }
.sd  { background: #fca5a5; }
.sl  { opacity: 1 !important; }
.su.sl { background: var(--green); }
.sd.sl { background: var(--red); }

.occ-row  { display: flex; align-items: center; gap: 8px; }
.occ-track{ width: 52px; height: 5px; background: var(--bg3); border-radius: 3px; }
.occ-fill { height: 100%; border-radius: 3px; }
.om { font-family: 'Archivo Narrow', sans-serif; font-size: .78rem; font-weight: 600; }

.ng { font-family: 'Archivo Narrow', sans-serif; color: var(--green);  font-size: .8rem; font-weight: 700; }
.nr { font-family: 'Archivo Narrow', sans-serif; color: var(--red);    font-size: .8rem; font-weight: 700; }
.nm { font-family: 'Archivo Narrow', sans-serif; color: var(--muted);  font-size: .8rem; }
.nt { font-family: 'Archivo Narrow', sans-serif; color: var(--txt2);   font-size: .8rem; font-weight: 500; }
.no { font-family: 'Archivo Narrow', sans-serif; color: var(--orange); font-size: .8rem; font-weight: 700; }

/* FOOTER */
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  margin-top: .5rem;
  border-top: 1px solid var(--bdr);
}
.ftxt {
  font-family: 'Archivo Narrow', sans-serif;
  font-size: .68rem;
  color: var(--muted);
}
.ftxt strong { color: var(--pink); }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
SINAL_ORDER = {
    "🚨 ABAIXO FORECAST + DESACEL - URGENTE": 1,
    "⚠️ ABAIXO FORECAST - PROXIMA VIAGEM":    2,
    "🔴 LOTANDO - REVISAR PREÇO":              3,
    "🟢 ACELERANDO - OPORTUNIDADE":            4,
    "🟡 ACELERANDO - MONITORAR":               5,
    "🔵 DESACELERANDO":                        6,
    "⚪ NORMAL":                               7,
}
SINAL_META = {
    "🚨 ABAIXO FORECAST + DESACEL - URGENTE": {"short":"URGENTE",      "badge":"b-urg","color":"#f11075","kpi":"c-red"},
    "⚠️ ABAIXO FORECAST - PROXIMA VIAGEM":    {"short":"ATENÇÃO",      "badge":"b-atn","color":"#f97316","kpi":"c-ora"},
    "🔴 LOTANDO - REVISAR PREÇO":              {"short":"LOTANDO",      "badge":"b-lot","color":"#ef4444","kpi":"c-red2"},
    "🟢 ACELERANDO - OPORTUNIDADE":            {"short":"OPORTUNIDADE", "badge":"b-opp","color":"#00b96b","kpi":"c-grn"},
    "🟡 ACELERANDO - MONITORAR":               {"short":"MONITORAR",    "badge":"b-mon","color":"#a16207","kpi":"c-yel"},
    "🔵 DESACELERANDO":                        {"short":"DESACEL.",     "badge":"b-des","color":"#2563eb","kpi":"c-blu"},
    "⚪ NORMAL":                               {"short":"NORMAL",       "badge":"b-nor","color":"#8a8a9a","kpi":"c-mut"},
}

# ── LOAD ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(url: str) -> pd.DataFrame:
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text))
        df.columns = df.columns.str.strip()
        int_cols   = ["pax","capacidade_atual","assentos_disponiveis",
                      "pax_d1","pax_d2","pax_d3","pax_d4","pax_d5",
                      "pax_hoje_parcial","predict_consenso","pax_faltam_forecast",
                      "predict_time_series","predict_eixo_sentido"]
        float_cols = ["occ_atual","tkm_comp","aceleracao_pct","aceleracao_abs",
                      "tendencia_linear","pct_atingimento_forecast","media_d2_d5",
                      "load_factor_atual"]
        for c in int_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
        for c in float_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def badge_html(sinal):
    m = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    return f'<span class="badge {m["badge"]}">{m["short"]}</span>'

def occ_html(v):
    try:
        pct = min(float(v)*100, 100)
        col = "#f11075" if pct>=90 else ("#f97316" if pct>=70 else "#00b96b")
        return (f'<div class="occ-row">'
                f'<div class="occ-track"><div class="occ-fill" style="width:{pct:.0f}%;background:{col}"></div></div>'
                f'<span class="om" style="color:{col}">{pct:.0f}%</span></div>')
    except:
        return "—"

def spark_html(d5, d4, d3, d2, d1):
    vals = [float(x) if str(x) not in ("nan","") else 0 for x in [d5,d4,d3,d2,d1]]
    mx   = max(vals) if max(vals)>0 else 1
    up   = vals[-1] >= (sum(vals[:-1])/max(len(vals)-1,1))
    bars = ""
    for i,v in enumerate(vals):
        h    = max(int((v/mx)*22), 2)
        last = (i==4)
        cls  = ("su sl" if up else "sd sl") if last else ("su" if up else "sd")
        bars += f'<div class="sb {cls}" style="height:{h}px" title="{v:.0f}"></div>'
    return f'<div class="spark">{bars}</div>'

def acel_html(pct):
    try:
        v = float(pct)
        if v > 30:  return f'<span class="ng">+{v:.0f}%</span>'
        if v < -30: return f'<span class="nr">{v:.0f}%</span>'
        return f'<span class="nm">{v:.0f}%</span>'
    except:
        return '<span class="nm">—</span>'

def fc_html(pct, faltam):
    try:
        v   = float(pct)
        cls = "nr" if v<50 else ("no" if v<80 else "ng")
        ft  = (f'<br><span class="nm" style="font-size:.63rem">faltam {int(faltam)}</span>'
               if str(faltam) not in ("nan","") else "")
        return f'<span class="{cls}">{v:.0f}%</span>{ft}'
    except:
        return "—"

def tend_html(v):
    try:
        f = float(v)
        if f>0.5:  return f'<span class="ng">↑ {f:.1f}</span>'
        if f<-0.5: return f'<span class="nr">↓ {f:.1f}</span>'
        return f'<span class="nm">→ {f:.1f}</span>'
    except:
        return '<span class="nm">—</span>'

def mono_html(v, prefix="", suffix="", dec=0):
    try:
        if str(v) in ("nan",""): return '<span class="nm">—</span>'
        return f'<span class="nt">{prefix}{float(v):,.{dec}f}{suffix}</span>'
    except:
        return '<span class="nm">—</span>'

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Configuração")
    github_url = st.text_input("URL do CSV (GitHub Raw)", value=GITHUB_RAW_DEFAULT)
    if st.button("↻ Recarregar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.markdown("### Filtros")

    df_raw = load_data(github_url)
    if df_raw.empty:
        st.warning("Nenhum dado. Verifique a URL.")
        st.stop()

    datas_disp = sorted(df_raw["data"].dt.date.unique()) if "data" in df_raw.columns else []
    datas_sel  = st.multiselect(
        "Data de viagem", options=datas_disp, default=datas_disp,
        format_func=lambda d: d.strftime("%d/%m/%Y"),
    )
    ant_min, ant_max = int(df_raw["antecedencia"].min()), int(df_raw["antecedencia"].max())
    ant_range  = st.slider("Antecedência (dias)", ant_min, ant_max, (ant_min, ant_max))
    rota_busca = st.text_input("Buscar rota", placeholder="ex: SAO-RIO")
    hide_normal= st.checkbox("Ocultar ⚪ NORMAL", value=True)

    st.divider()
    st.markdown(
        '<span style="font-family:\'Archivo Narrow\',sans-serif;font-size:.68rem;color:#8a8a9a">'
        'D1 = ontem · D5 = 5 dias atrás<br>Acel = D1 vs média D2–D5</span>',
        unsafe_allow_html=True,
    )

# ── FILTROS ───────────────────────────────────────────────────────────────────
df_base = df_raw.copy()
if datas_sel:
    df_base = df_base[df_base["data"].dt.date.isin(datas_sel)]
df_base = df_base[df_base["antecedencia"].between(ant_range[0], ant_range[1])]
if rota_busca:
    df_base = df_base[df_base["sentido"].str.upper().str.contains(rota_busca.upper(), na=False)]
if hide_normal:
    df_base = df_base[df_base["sinal"] != "⚪ NORMAL"]

# ── HEADER ────────────────────────────────────────────────────────────────────
agora = datetime.now().strftime("%d/%m %H:%M")
st.markdown(f"""
<div class="farol-header">
  <div class="header-left">
    <span class="farol-eyebrow">Monitoramento de reservas</span>
    <span class="farol-title">Farol de Aceleração PAX</span>
    <span class="farol-sub">{len(df_base)} rotas visíveis com os filtros aplicados</span>
  </div>
  <div class="upill"><span class="dot"></span>atualizado {agora}</div>
</div>
""", unsafe_allow_html=True)

# ── KPI STRIP ─────────────────────────────────────────────────────────────────
def cnt_kw(kw): return int(df_raw["sinal"].str.contains(kw, na=False).sum())

kpis = [
    ("c-red",  "🚨 Urgente",      cnt_kw("URGENTE")),
    ("c-ora",  "⚠️ Atenção",      cnt_kw("PROXIMA")),
    ("c-red2", "🔴 Lotando",      cnt_kw("LOTANDO")),
    ("c-grn",  "🟢 Oportunidade", cnt_kw("OPORTUNIDADE")),
    ("c-yel",  "🟡 Monitorar",    cnt_kw("MONITORAR")),
    ("c-blu",  "🔵 Desacel.",     cnt_kw("DESACEL")),
    ("c-mut",  "Total rotas",     len(df_raw)),
]
strip = '<div class="kpi-strip">'
for cls, lbl, val in kpis:
    strip += f'<div class="kpi {cls}"><div class="kpi-lbl">{lbl}</div><div class="kpi-val">{val}</div></div>'
strip += '</div>'
st.markdown(strip, unsafe_allow_html=True)

# ── GRÁFICO ───────────────────────────────────────────────────────────────────
if "aceleracao_pct" in df_base.columns and not df_base.empty:
    df_ch = df_base.dropna(subset=["aceleracao_pct"]).copy()
    if "media_d2_d5" in df_ch.columns:
        df_ch = df_ch[df_ch["media_d2_d5"] >= 2]

    top_up   = df_ch.nlargest(8,  "aceleracao_pct")
    top_down = df_ch.nsmallest(8, "aceleracao_pct")
    max_abs  = max(
        top_up["aceleracao_pct"].abs().max()   if not top_up.empty   else 1,
        top_down["aceleracao_pct"].abs().max() if not top_down.empty else 1,
    )

    def hbar(row, color, bg):
        pct_w = min(abs(float(row["aceleracao_pct"])) / max_abs * 100, 100)
        v     = float(row["aceleracao_pct"])
        sign  = "+" if v > 0 else ""
        dt    = pd.to_datetime(row["data"]).strftime("%d/%m") if pd.notna(row["data"]) else ""
        return (f'<div class="hbar-row">'
                f'<div style="width:76px;text-align:right;flex-shrink:0">'
                f'<span class="hbar-lbl">{row["sentido"]}</span><br>'
                f'<span class="hbar-date">{dt}</span></div>'
                f'<div class="hbar-track" style="background:{bg}">'
                f'<div class="hbar-fill" style="width:{pct_w:.1f}%;background:{color}">'
                f'<span class="hbar-val">{sign}{v:.0f}%</span></div></div></div>')

    chart = '<div class="chart-wrap"><div class="chart-grid">'
    chart += '<div><div class="chart-col-title up">Maiores Acelerações</div>'
    for _, r in top_up.iterrows():
        chart += hbar(r, "#00b96b", "#f0fdf4")
    chart += '</div>'
    chart += '<div><div class="chart-col-title down">Maiores Desacelerações</div>'
    for _, r in top_down.iterrows():
        chart += hbar(r, "#f11075", "#fff0f5")
    chart += '</div></div></div>'
    st.markdown(chart, unsafe_allow_html=True)

# ── CHIPS ─────────────────────────────────────────────────────────────────────
sinais_pres = sorted(df_base["sinal"].dropna().unique(), key=lambda s: SINAL_ORDER.get(s, 99))

if "chips" not in st.session_state:
    st.session_state.chips = set(sinais_pres)
st.session_state.chips = st.session_state.chips.intersection(sinais_pres)
if not st.session_state.chips:
    st.session_state.chips = set(sinais_pres)

chip_cols = st.columns(len(sinais_pres) + 1)
for i, sinal in enumerate(sinais_pres):
    m     = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    ativo = sinal in st.session_state.chips
    cnt_s = int((df_base["sinal"] == sinal).sum())
    with chip_cols[i]:
        if st.button(
            f"{m['short']} ({cnt_s})",
            key=f"chip_{i}",
            use_container_width=True,
            type="primary" if ativo else "secondary",
        ):
            if ativo and len(st.session_state.chips) > 1:
                st.session_state.chips.discard(sinal)
            else:
                st.session_state.chips.add(sinal)
            st.rerun()

# ── TABELA ────────────────────────────────────────────────────────────────────
df_view = df_base[df_base["sinal"].isin(st.session_state.chips)].copy()
df_view = df_view.sort_values("sinal", key=lambda s: s.map(lambda x: SINAL_ORDER.get(x, 99)))

if df_view.empty:
    st.info("Nenhuma rota com os filtros selecionados.")
    st.stop()

has_d5 = "pax_d5" in df_view.columns
rows   = ""
cur    = None

for _, row in df_view.iterrows():
    if row["sinal"] != cur:
        cur   = row["sinal"]
        m     = SINAL_META.get(cur, SINAL_META["⚪ NORMAL"])
        cnt_g = int((df_view["sinal"] == cur).sum())
        rows += (f'<tr class="grp-sep"><td colspan="13" style="color:{m["color"]}!important">'
                 f'{cur} &nbsp;·&nbsp; {cnt_g} rota{"s" if cnt_g>1 else ""}</td></tr>')

    dt  = row["data"].strftime("%d/%m") if pd.notna(row.get("data")) else "—"
    d5  = row.get("pax_d5", 0) if has_d5 else 0

    rows += f"""<tr>
      <td><span class="rname">{row.get('sentido','—')}</span><br>
          <span class="rsub">{row.get('rota_principal','')}</span></td>
      <td><span class="nt">{dt}</span></td>
      <td>{mono_html(row.get('antecedencia'), suffix='d')}</td>
      <td>{occ_html(row.get('occ_atual', 0))}</td>
      <td>{mono_html(row.get('pax'))}</td>
      <td>{mono_html(row.get('assentos_disponiveis'))}</td>
      <td>{fc_html(row.get('pct_atingimento_forecast'), row.get('pax_faltam_forecast'))}</td>
      <td>{spark_html(d5, row.get('pax_d4',0), row.get('pax_d3',0), row.get('pax_d2',0), row.get('pax_d1',0))}</td>
      <td>{acel_html(row.get('aceleracao_pct'))}</td>
      <td>{tend_html(row.get('tendencia_linear'))}</td>
      <td>{mono_html(row.get('tkm_comp'), prefix='R$', dec=0)}</td>
      <td>{mono_html(row.get('predict_consenso'))}</td>
      <td>{badge_html(str(row.get('sinal','⚪ NORMAL')))}</td>
    </tr>"""

st.markdown(f"""
<div class="tbl-wrap">
<table class="tbl">
  <thead><tr>
    <th>Rota</th><th>Data</th><th>Antec.</th><th>Ocupação</th>
    <th>PAX</th><th>Assentos liv.</th><th>Forecast %</th>
    <th>D5→D1</th><th>Acel. %</th><th>Tendência</th>
    <th>Ticket</th><th>Predict</th><th>Sinal</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <span class="ftxt"><strong>{len(df_view)}</strong> rotas exibidas · {len(df_raw)} total carregadas</span>
  <span class="ftxt">D1 = ontem completo · Acel = D1 vs média D2–D5 · sem viés de horário</span>
</div>
""", unsafe_allow_html=True)
