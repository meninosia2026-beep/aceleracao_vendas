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
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --bg:      #ffffff;
  --bg2:     #f7f6f3;
  --bg3:     #eeede9;
  --bdr:     #e2e1dc;
  --bdr2:    #d0cfc9;
  --txt:     #1a1a18;
  --txt2:    #3d3d38;
  --muted:   #8c8c84;
  --muted2:  #b8b8b0;
  --accent:  #f11075;
  --green:   #2d6a4f;
  --green-lt:#d8f3dc;
  --red:     #c0392b;
  --red-lt:  #fde8e8;
  --orange:  #d35400;
  --blue:    #2c3e7a;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"] > div {
  background: var(--bg) !important;
  color: var(--txt) !important;
  font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--bdr) !important;
}
[data-testid="stSidebar"] * { color: var(--txt) !important; font-family: 'Inter', sans-serif !important; }

.block-container { padding: 2.5rem 3rem !important; max-width: 100% !important; }
hr { border: none; border-top: 1px solid var(--bdr) !important; margin: 1rem 0; }

[data-testid="stTextInput"] input {
  background: var(--bg) !important; border: 1px solid var(--bdr2) !important;
  border-radius: 4px !important; color: var(--txt) !important;
  font-family: 'Inter', sans-serif !important; font-size: .83rem !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--accent) !important; outline: none !important; box-shadow: none !important;
}

[data-testid="stButton"] > button {
  background: var(--bg) !important; border: 1px solid var(--bdr2) !important;
  color: var(--txt2) !important; font-family: 'Inter', sans-serif !important;
  font-size: .78rem !important; font-weight: 500 !important; border-radius: 4px !important;
  transition: all .12s !important;
}
[data-testid="stButton"] > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
[data-testid="stButton"] > button[kind="primary"] {
  background: var(--txt) !important; color: var(--bg) !important; border-color: var(--txt) !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 2px; }

/* HEADER */
.pg-header {
  padding-bottom: 1.5rem; margin-bottom: 2rem; border-bottom: 1px solid var(--bdr);
  display: flex; justify-content: space-between; align-items: flex-start;
}
.pg-title {
  font-family: 'Libre Baskerville', serif; font-size: 2.1rem; font-weight: 700;
  letter-spacing: -.5px; color: var(--txt); line-height: 1.1; margin-bottom: 6px;
}
.pg-sub { font-size: .82rem; color: var(--muted); font-weight: 400; }
.upill {
  display: inline-flex; align-items: center; gap: 7px;
  font-size: .72rem; color: var(--muted); white-space: nowrap; margin-top: 6px;
}
.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); display: inline-block; animation: pulse 2.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

/* KPI */
.kpi-strip {
  display: grid; grid-template-columns: repeat(7, 1fr);
  gap: 0; border: 1px solid var(--bdr); border-radius: 6px;
  overflow: hidden; margin-bottom: 2.5rem;
}
.kpi { padding: 16px 20px 14px; border-right: 1px solid var(--bdr); background: var(--bg); }
.kpi:last-child { border-right: none; }
.kpi-lbl {
  font-size: .65rem; font-weight: 600; color: var(--muted);
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;
  display: flex; align-items: center; gap: 5px;
}
.kpi-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.kpi-val { font-family: 'Libre Baskerville', serif; font-size: 2.2rem; font-weight: 700; line-height: 1; color: var(--txt); }
.kpi-val.zero { color: var(--muted2); }

/* CHART */
.chart-section { margin-bottom: 2.5rem; }
.section-title {
  font-family: 'Libre Baskerville', serif; font-size: 1.1rem; font-weight: 700;
  color: var(--txt); margin-bottom: 4px;
}
.section-sub { font-size: .78rem; color: var(--muted); margin-bottom: 1.2rem; }
.chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.chart-col {
  background: var(--bg2); border: 1px solid var(--bdr);
  border-radius: 6px; padding: 20px 22px;
}
.chart-col-title {
  font-size: .72rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 1px; color: var(--muted); margin-bottom: 14px;
  display: flex; align-items: center; gap: 8px;
}
.chart-col-title span { display: inline-block; width: 8px; height: 8px; border-radius: 50%; }
.hbar-row { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.hbar-lbl {
  font-size: .73rem; font-weight: 500; color: var(--txt2);
  width: 90px; text-align: right; flex-shrink: 0;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.hbar-date { font-size: .62rem; color: var(--muted); display: block; font-weight: 400; }
.hbar-track { flex: 1; height: 20px; background: var(--bg3); border-radius: 3px; overflow: hidden; }
.hbar-fill { height: 100%; border-radius: 3px; display: flex; align-items: center; }
.hbar-val { font-size: .7rem; font-weight: 600; padding-left: 8px; color: #fff; white-space: nowrap; }

/* NAV TABS */
.nav-bar {
  display: flex; gap: 0; border-bottom: 1px solid var(--bdr);
  margin-bottom: 0; overflow-x: auto;
}
.nav-item {
  padding: 8px 16px 10px; font-size: .8rem; font-weight: 500; color: var(--muted);
  cursor: pointer; border-bottom: 2px solid transparent; white-space: nowrap;
  transition: all .12s; user-select: none; display: flex; align-items: center;
  gap: 5px; margin-bottom: -1px;
}
.nav-item:hover { color: var(--txt); }
.nav-item.active { color: var(--txt); border-bottom-color: var(--accent); font-weight: 600; }
.nav-count {
  background: var(--bg3); border-radius: 10px; padding: 1px 7px;
  font-size: .68rem; color: var(--muted); font-weight: 600;
}
.nav-item.active .nav-count { background: var(--accent); color: #fff; }

/* ORDENAÇÃO INFO */
.sort-info {
  font-size: .68rem; color: var(--muted); padding: 6px 0 10px;
  display: flex; align-items: center; gap: 6px;
}
.sort-tag {
  display: inline-flex; align-items: center; gap: 4px;
  background: var(--bg3); border: 1px solid var(--bdr2);
  border-radius: 3px; padding: 1px 7px;
  font-size: .65rem; font-weight: 600; color: var(--txt2);
}

/* TABLE */
.tbl-wrap {
  overflow-x: auto; border: 1px solid var(--bdr);
  border-radius: 6px; margin-bottom: 1.5rem;
}
.tbl { width: 100%; border-collapse: collapse; font-size: .8rem; }
.tbl thead tr { background: var(--bg2); }
.tbl th {
  padding: 10px 14px; border-bottom: 1px solid var(--bdr2);
  font-size: .63rem; font-weight: 600; color: var(--muted);
  text-transform: uppercase; letter-spacing: 1px; text-align: left; white-space: nowrap;
}
.tbl th.sort-active { color: var(--txt); }
.tbl th.sort-active::after { content: ' ↓'; color: var(--accent); }
.tbl td { padding: 10px 14px; border-bottom: 1px solid var(--bdr); vertical-align: middle; white-space: nowrap; }
.tbl tbody tr:hover td { background: var(--bg2); }
.tbl tbody tr:last-child td { border-bottom: none; }

/* linha do top 3 dentro do grupo */
.tbl tbody tr.top-row td { background: #fafaf8; }
.tbl tbody tr.top-row:hover td { background: var(--bg2); }

.grp-sep td {
  background: var(--bg2) !important; padding: 7px 14px !important;
  font-size: .65rem !important; font-weight: 600 !important; color: var(--muted) !important;
  letter-spacing: .8px !important; text-transform: uppercase !important;
  border-top: 1px solid var(--bdr2) !important; border-bottom: 1px solid var(--bdr2) !important;
}

.rname { font-weight: 600; font-size: .85rem; color: var(--txt); }
.rsub  { font-size: .63rem; color: var(--muted); }

.badge {
  display: inline-block; padding: 2px 8px; border-radius: 3px;
  font-size: .65rem; font-weight: 600; white-space: nowrap;
  letter-spacing: .3px; text-transform: uppercase;
  background: var(--bg3); color: var(--txt2); border: 1px solid var(--bdr2);
}
.b-urg { background: var(--red-lt);  color: var(--red);   border-color: #f5c6c6; }
.b-atn { background: #fef3e2;        color: var(--orange);border-color: #f5d9b0; }
.b-opp { background: var(--green-lt);color: var(--green); border-color: #95d5b2; }

.spark { display: inline-flex; gap: 2px; align-items: flex-end; height: 22px; vertical-align: middle; }
.sb    { width: 6px; border-radius: 1px 1px 0 0; background: var(--bdr2); }
.su    { background: #74c69d; }
.sd    { background: #f5a0a0; }
.su.sl { background: var(--green); }
.sd.sl { background: var(--red); }

.occ-row   { display: flex; align-items: center; gap: 8px; }
.occ-track { width: 48px; height: 4px; background: var(--bg3); border-radius: 2px; }
.occ-fill  { height: 100%; border-radius: 2px; }
.om { font-size: .78rem; font-weight: 600; }

.ng  { color: var(--green);  font-size: .8rem; font-weight: 600; }
.nr  { color: var(--red);    font-size: .8rem; font-weight: 600; }
.nm  { color: var(--muted);  font-size: .8rem; }
.nt  { color: var(--txt2);   font-size: .8rem; }
.no  { color: var(--orange); font-size: .8rem; font-weight: 600; }

.sinal-tag { display: inline-flex; align-items: center; gap: 5px; font-size: .72rem; font-weight: 500; color: var(--txt2); }
.sinal-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

/* score bar */
.score-wrap { display: flex; align-items: center; gap: 6px; }
.score-track { width: 40px; height: 3px; background: var(--bg3); border-radius: 2px; }
.score-fill  { height: 100%; border-radius: 2px; background: var(--accent); }
.score-val   { font-size: .68rem; color: var(--muted); }

.sb-label {
  font-size: .65rem; font-weight: 600; color: var(--muted);
  text-transform: uppercase; letter-spacing: 1px; margin: 1rem 0 .4rem;
}

.footer {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 1.2rem; border-top: 1px solid var(--bdr); margin-top: .5rem;
}
.ftxt { font-size: .68rem; color: var(--muted); }
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
    "🚨 ABAIXO FORECAST + DESACEL - URGENTE": {"short":"Urgente",      "badge":"b-urg","dot":"#c0392b"},
    "⚠️ ABAIXO FORECAST - PROXIMA VIAGEM":    {"short":"Atenção",      "badge":"b-atn","dot":"#d35400"},
    "🔴 LOTANDO - REVISAR PREÇO":              {"short":"Lotando",      "badge":"",     "dot":"#e74c3c"},
    "🟢 ACELERANDO - OPORTUNIDADE":            {"short":"Oportunidade", "badge":"b-opp","dot":"#2d6a4f"},
    "🟡 ACELERANDO - MONITORAR":               {"short":"Monitorar",    "badge":"",     "dot":"#b7950b"},
    "🔵 DESACELERANDO":                        {"short":"Desacel.",     "badge":"",     "dot":"#2c3e7a"},
    "⚪ NORMAL":                               {"short":"Normal",       "badge":"",     "dot":"#b8b8b0"},
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
                      "tendencia_linear","pct_atingimento_forecast","media_d2_d5","load_factor_atual"]
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

# ── SCORE ─────────────────────────────────────────────────────────────────────
def calcular_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # forecast: quanto já capturou (0–150% normalizado)
    fc   = df["pct_atingimento_forecast"].fillna(0).clip(0, 150) / 150
    # ocupação (0–1)
    occ  = df["occ_atual"].fillna(0).clip(0, 1)
    # aceleração normalizada (0–1)
    acel = df["aceleracao_pct"].fillna(0)
    a_min, a_max = acel.min(), acel.max()
    acel_norm = (acel - a_min) / (a_max - a_min + 1e-9)

    df["_score"] = (0.40 * fc) + (0.35 * occ) + (0.25 * acel_norm)
    return df

# ── HELPERS ───────────────────────────────────────────────────────────────────
def sinal_tag(sinal):
    m = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    if m["badge"]:
        return f'<span class="badge {m["badge"]}">{m["short"]}</span>'
    return (f'<span class="sinal-tag">'
            f'<span class="sinal-dot" style="background:{m["dot"]}"></span>'
            f'{m["short"]}</span>')

def score_bar(score):
    try:
        pct = min(float(score) * 100, 100)
        return (f'<div class="score-wrap">'
                f'<div class="score-track"><div class="score-fill" style="width:{pct:.0f}%"></div></div>'
                f'<span class="score-val">{pct:.0f}</span></div>')
    except: return "—"

def occ_html(v):
    try:
        pct = min(float(v)*100, 100)
        col = "#c0392b" if pct>=90 else ("#d35400" if pct>=70 else "#2d6a4f")
        return (f'<div class="occ-row">'
                f'<div class="occ-track"><div class="occ-fill" style="width:{pct:.0f}%;background:{col}"></div></div>'
                f'<span class="om" style="color:{col}">{pct:.0f}%</span></div>')
    except: return "—"

def spark_html(d5, d4, d3, d2, d1):
    vals = [float(x) if str(x) not in ("nan","") else 0 for x in [d5,d4,d3,d2,d1]]
    mx   = max(vals) if max(vals)>0 else 1
    up   = vals[-1] >= (sum(vals[:-1])/max(len(vals)-1,1))
    bars = ""
    for i,v in enumerate(vals):
        h    = max(int((v/mx)*20), 2)
        last = (i==4)
        cls  = ("su sl" if up else "sd sl") if last else ("su" if up else "sd")
        bars += f'<div class="sb {cls}" style="height:{h}px" title="D{5-i}: {v:.0f}"></div>'
    return f'<div class="spark">{bars}</div>'

def acel_html(pct):
    try:
        v = float(pct)
        if v > 30:  return f'<span class="ng">+{v:.0f}%</span>'
        if v < -30: return f'<span class="nr">{v:.0f}%</span>'
        return f'<span class="nm">{v:.0f}%</span>'
    except: return '<span class="nm">—</span>'

def fc_html(pct, faltam):
    try:
        v   = float(pct)
        cls = "nr" if v<50 else ("no" if v<80 else "ng")
        ft  = (f'<br><span class="nm" style="font-size:.63rem">faltam {int(faltam)}</span>'
               if str(faltam) not in ("nan","") else "")
        return f'<span class="{cls}">{v:.0f}%</span>{ft}'
    except: return "—"

def tend_html(v):
    try:
        f = float(v)
        if f>0.5:  return f'<span class="ng">↑ {f:.1f}</span>'
        if f<-0.5: return f'<span class="nr">↓ {f:.1f}</span>'
        return f'<span class="nm">→ {f:.1f}</span>'
    except: return '<span class="nm">—</span>'

def mono_html(v, prefix="", suffix="", dec=0):
    try:
        if str(v) in ("nan",""): return '<span class="nm">—</span>'
        return f'<span class="nt">{prefix}{float(v):,.{dec}f}{suffix}</span>'
    except: return '<span class="nm">—</span>'

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-label">Fonte de dados</div>', unsafe_allow_html=True)
    github_url = st.text_input("", value=GITHUB_RAW_DEFAULT, label_visibility="collapsed")
    if st.button("↻ Recarregar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.divider()

    df_raw = load_data(github_url)
    if df_raw.empty:
        st.warning("Nenhum dado. Verifique a URL.")
        st.stop()

    st.markdown('<div class="sb-label">Data de viagem</div>', unsafe_allow_html=True)
    datas_disp = sorted(df_raw["data"].dt.date.unique()) if "data" in df_raw.columns else []
    datas_sel  = st.multiselect("", options=datas_disp, default=datas_disp,
                                format_func=lambda d: d.strftime("%d/%m/%Y"),
                                label_visibility="collapsed")

    st.markdown('<div class="sb-label">Antecedência (dias)</div>', unsafe_allow_html=True)
    ant_min, ant_max = int(df_raw["antecedencia"].min()), int(df_raw["antecedencia"].max())
    ant_range = st.slider("", ant_min, ant_max, (ant_min, ant_max), label_visibility="collapsed")

    st.markdown('<div class="sb-label">Buscar rota</div>', unsafe_allow_html=True)
    rota_busca = st.text_input("", placeholder="ex: SAO-RIO", label_visibility="collapsed")

    hide_normal = st.checkbox("Ocultar rotas Normais", value=True)

    st.divider()
    st.markdown(
        '<span style="font-size:.67rem;color:#8c8c84;line-height:1.8">'
        'D1 = ontem completo<br>D5 = 5 dias atrás<br>'
        'Acel = D1 vs média D2–D5<br><br>'
        '<b>Score</b> = 40% forecast + 35% occ + 25% acel</span>',
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
agora = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
<div class="pg-header">
  <div>
    <div class="pg-title">Farol de Aceleração PAX</div>
    <div class="pg-sub">Monitoramento de velocidade de reservas por rota · {len(df_base)} rotas visíveis</div>
  </div>
  <div class="upill"><span class="dot"></span>Atualizado em {agora} · via Databricks</div>
</div>
""", unsafe_allow_html=True)

# ── KPI ───────────────────────────────────────────────────────────────────────
def cnt_kw(kw): return int(df_raw["sinal"].str.contains(kw, na=False).sum())

kpis = [
    ("URGENTE",      cnt_kw("URGENTE"),      "#c0392b"),
    ("ATENÇÃO",      cnt_kw("PROXIMA"),       "#d35400"),
    ("LOTANDO",      cnt_kw("LOTANDO"),       "#e74c3c"),
    ("OPORTUNIDADE", cnt_kw("OPORTUNIDADE"), "#2d6a4f"),
    ("MONITORAR",    cnt_kw("MONITORAR"),     "#b7950b"),
    ("DESACEL.",     cnt_kw("DESACEL"),       "#2c3e7a"),
    ("TOTAL ROTAS",  len(df_raw),             "#b8b8b0"),
]
strip = '<div class="kpi-strip">'
for lbl, val, dot in kpis:
    zero_cls = " zero" if val == 0 else ""
    strip += (f'<div class="kpi">'
              f'<div class="kpi-lbl"><span class="kpi-dot" style="background:{dot}"></span>{lbl}</div>'
              f'<div class="kpi-val{zero_cls}">{val}</div></div>')
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

    def hbar(row, color):
        pct_w = min(abs(float(row["aceleracao_pct"])) / max_abs * 100, 100)
        v     = float(row["aceleracao_pct"])
        sign  = "+" if v > 0 else ""
        dt    = pd.to_datetime(row["data"]).strftime("%d/%m") if pd.notna(row["data"]) else ""
        return (f'<div class="hbar-row">'
                f'<div style="width:90px;text-align:right;flex-shrink:0">'
                f'<span class="hbar-lbl">{row["sentido"]}</span>'
                f'<span class="hbar-date">{dt}</span></div>'
                f'<div class="hbar-track">'
                f'<div class="hbar-fill" style="width:{pct_w:.1f}%;background:{color}">'
                f'<span class="hbar-val">{sign}{v:.0f}%</span></div></div></div>')

    st.markdown(f"""
    <div class="chart-section">
      <div class="section-title">Maiores variações de aceleração</div>
      <div class="section-sub">Variação de D1 vs média D2–D5 · rotas com volume mínimo de 2 reservas/dia</div>
      <div class="chart-grid">
        <div class="chart-col">
          <div class="chart-col-title"><span style="background:#2d6a4f"></span>Acelerando</div>
          {''.join(hbar(r, "#2d6a4f") for _, r in top_up.iterrows())}
        </div>
        <div class="chart-col">
          <div class="chart-col-title"><span style="background:#c0392b"></span>Desacelerando</div>
          {''.join(hbar(r, "#c0392b") for _, r in top_down.iterrows())}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── CHIPS ─────────────────────────────────────────────────────────────────────
sinais_pres = sorted(df_base["sinal"].dropna().unique(), key=lambda s: SINAL_ORDER.get(s, 99))

if "chips" not in st.session_state:
    st.session_state.chips = set(sinais_pres)
st.session_state.chips = st.session_state.chips.intersection(sinais_pres)
if not st.session_state.chips:
    st.session_state.chips = set(sinais_pres)

nav_html = '<div class="nav-bar">'
for sinal in sinais_pres:
    m     = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    ativo = sinal in st.session_state.chips
    cnt_s = int((df_base["sinal"] == sinal).sum())
    act   = " active" if ativo else ""
    nav_html += (f'<div class="nav-item{act}">'
                 f'<span class="sinal-dot" style="background:{m["dot"]}"></span>'
                 f'{m["short"]} <span class="nav-count">{cnt_s}</span></div>')
nav_html += '</div>'
st.markdown(nav_html, unsafe_allow_html=True)

chip_cols = st.columns(len(sinais_pres) + 1)
for i, sinal in enumerate(sinais_pres):
    m     = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    ativo = sinal in st.session_state.chips
    cnt_s = int((df_base["sinal"] == sinal).sum())
    with chip_cols[i]:
        if st.button(
            f"{'●' if ativo else '○'} {m['short']} ({cnt_s})",
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
df_view = calcular_score(df_view)

# ordena: primeiro por grupo de sinal (prioridade), depois por score decrescente
df_view["_sinal_ord"] = df_view["sinal"].map(lambda x: SINAL_ORDER.get(x, 99))
df_view = df_view.sort_values(["_sinal_ord", "_score"], ascending=[True, False])

if df_view.empty:
    st.info("Nenhuma rota com os filtros selecionados.")
    st.stop()

# info de ordenação
st.markdown("""
<div class="sort-info">
  Ordenado por &nbsp;
  <span class="sort-tag">▼ Forecast %</span>
  <span class="sort-tag">▼ Ocupação</span>
  <span class="sort-tag">▼ Aceleração</span>
  &nbsp; dentro de cada grupo · score ponderado 40 / 35 / 25
</div>
""", unsafe_allow_html=True)

has_d5 = "pax_d5" in df_view.columns
rows   = ""
cur    = None
rank   = {}  # rank dentro do grupo

for _, row in df_view.iterrows():
    sinal = row["sinal"]
    if sinal != cur:
        cur      = sinal
        rank[cur] = 0
        m        = SINAL_META.get(cur, SINAL_META["⚪ NORMAL"])
        cnt_g    = int((df_view["sinal"] == cur).sum())
        rows += (f'<tr class="grp-sep"><td colspan="14">'
                 f'<span style="display:inline-flex;align-items:center;gap:6px">'
                 f'<span style="width:6px;height:6px;border-radius:50%;background:{m["dot"]};display:inline-block"></span>'
                 f'{cur} &nbsp;·&nbsp; {cnt_g} rota{"s" if cnt_g>1 else ""}'
                 f'</span></td></tr>')

    rank[cur] += 1
    top_cls = " top-row" if rank[cur] <= 3 else ""
    dt      = row["data"].strftime("%d/%m") if pd.notna(row.get("data")) else "—"
    d5      = row.get("pax_d5", 0) if has_d5 else 0
    sc      = row.get("_score", 0)

    rows += f"""<tr class="{top_cls}">
      <td><span style="font-size:.6rem;color:var(--muted2);font-weight:600;margin-right:6px">#{rank[cur]}</span>
          <span class="rname">{row.get('sentido','—')}</span><br>
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
      <td>{score_bar(sc)}</td>
      <td>{sinal_tag(str(row.get('sinal','⚪ NORMAL')))}</td>
    </tr>"""

st.markdown(f"""
<div class="tbl-wrap">
<table class="tbl">
  <thead><tr>
    <th>Rota</th><th>Data</th><th>Antec.</th>
    <th class="sort-active">Ocupação</th>
    <th>PAX</th><th>Assentos liv.</th>
    <th class="sort-active">Forecast %</th>
    <th>D5→D1</th>
    <th class="sort-active">Acel. %</th>
    <th>Tendência</th><th>Ticket</th><th>Predict</th>
    <th class="sort-active">Score</th>
    <th>Sinal</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <span class="ftxt"><strong style="color:var(--txt)">{len(df_view)}</strong> rotas exibidas · {len(df_raw)} total carregadas</span>
  <span class="ftxt">D1 = ontem completo · Acel = D1 vs média D2–D5 · sem viés de horário</span>
</div>
""", unsafe_allow_html=True)
