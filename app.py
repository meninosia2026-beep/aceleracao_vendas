import streamlit as st
import pandas as pd
import requests
import io
import base64
import json
from datetime import datetime

GITHUB_RAW_CURVA   = "https://raw.githubusercontent.com/meninosia2026-beep/aceleracao_vendas/main/data/curva_feriado.csv"
GITHUB_RAW_CURVA2  = "https://raw.githubusercontent.com/meninosia2026-beep/aceleracao_vendas/main/data/curva_feriado2.csv"

st.set_page_config(page_title="Pricing · Curva de Feriados", page_icon=None, layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

:root {
  --bg:       #f9f8f6;
  --bg2:      #f2f1ee;
  --bg3:      #eae9e5;
  --bdr:      #e0deda;
  --bdr2:     #cccac5;
  --txt:      #171614;
  --txt2:     #3a3935;
  --muted:    #7a7870;
  --muted2:   #b0aea8;
  --ink:      #1a1a1a;
  --accent:   #1a1a1a;
  --green:    #1e5c3a;
  --green-lt: #e8f5ee;
  --red:      #8b1a1a;
  --red-lt:   #fdf0f0;
  --amber:    #7a4a0a;
  --amber-lt: #fdf5e8;
  --blue:     #1a2e5c;
}

*,*::before,*::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"] > div {
  background: var(--bg) !important;
  color: var(--txt) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--bdr) !important;
}
[data-testid="stSidebar"] * { color: var(--txt) !important; font-family: 'DM Sans', sans-serif !important; }

.block-container { padding: 2.5rem 3rem !important; max-width: 100% !important; }
hr { border: none; border-top: 1px solid var(--bdr) !important; margin: 1.2rem 0; }

::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 2px; }

/* ── INPUTS ───────────────────────────────────── */
[data-testid="stTextInput"] input {
  background: var(--bg) !important;
  border: 1px solid var(--bdr2) !important;
  border-radius: 3px !important;
  color: var(--txt) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: .83rem !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--ink) !important;
  outline: none !important;
  box-shadow: none !important;
}

/* ── BUTTONS ──────────────────────────────────── */
[data-testid="stButton"] > button {
  background: transparent !important;
  border: 1px solid var(--bdr2) !important;
  color: var(--muted) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: .75rem !important;
  font-weight: 500 !important;
  border-radius: 3px !important;
  padding: 5px 14px !important;
  letter-spacing: .2px !important;
  transition: all .1s !important;
  white-space: nowrap !important;
}
[data-testid="stButton"] > button:hover {
  border-color: var(--ink) !important;
  color: var(--ink) !important;
  background: var(--bg3) !important;
}
[data-testid="stButton"] > button[kind="primary"] {
  background: var(--ink) !important;
  color: var(--bg) !important;
  border-color: var(--ink) !important;
  font-weight: 600 !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
  background: #333 !important;
  color: #fff !important;
}

/* ── MULTISELECT ──────────────────────────────── */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
  background: var(--bg) !important;
  border: 1px solid var(--bdr2) !important;
  border-radius: 3px !important;
  min-height: 34px !important;
  box-shadow: none !important;
}
[data-testid="stMultiSelect"] [data-baseweb="select"] > div:focus-within {
  border-color: var(--ink) !important;
  box-shadow: none !important;
}
[data-baseweb="tag"] {
  background: var(--bg3) !important;
  border: 1px solid var(--bdr2) !important;
  border-radius: 2px !important;
  padding: 1px 6px !important;
  height: 20px !important;
}
[data-baseweb="tag"] span:first-child {
  color: var(--txt2) !important;
  font-size: .71rem !important;
  font-weight: 500 !important;
}
[data-baseweb="popover"] [data-baseweb="menu"] {
  background: var(--bg) !important;
  border: 1px solid var(--bdr2) !important;
  border-radius: 3px !important;
  box-shadow: 0 4px 20px rgba(0,0,0,.1) !important;
}
[data-baseweb="option"] {
  background: var(--bg) !important;
  font-size: .78rem !important;
  color: var(--txt2) !important;
  padding: 7px 12px !important;
}
[data-baseweb="option"]:hover,
[aria-selected="true"][data-baseweb="option"] { background: var(--bg2) !important; }

/* ── SLIDER ───────────────────────────────────── */
[data-testid="stSlider"] [role="slider"] {
  background: var(--ink) !important;
  border: 2px solid var(--bg) !important;
  box-shadow: 0 1px 4px rgba(0,0,0,.2) !important;
  width: 13px !important;
  height: 13px !important;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
  font-size: .68rem !important;
  color: var(--muted) !important;
}

/* ── CHECKBOX ─────────────────────────────────── */
[data-testid="stCheckbox"] label {
  font-size: .8rem !important;
  color: var(--txt2) !important;
  font-weight: 400 !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 8px !important;
  white-space: nowrap !important;
}
[data-testid="stCheckbox"] [data-baseweb="checkbox"] div {
  border-color: var(--bdr2) !important;
  border-radius: 2px !important;
  background: var(--bg) !important;
  width: 15px !important;
  height: 15px !important;
  flex-shrink: 0 !important;
}
[data-testid="stCheckbox"] [aria-checked="true"] div {
  background: var(--ink) !important;
  border-color: var(--ink) !important;
}

/* ── TABS ─────────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--bdr) !important;
  gap: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: .82rem !important;
  font-weight: 400 !important;
  border: none !important;
  border-bottom: 1.5px solid transparent !important;
  padding: 8px 20px 10px !important;
  margin-bottom: -1px !important;
  letter-spacing: .1px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover { color: var(--txt) !important; }
[data-testid="stTabs"] [aria-selected="true"][data-baseweb="tab"] {
  color: var(--ink) !important;
  border-bottom-color: var(--ink) !important;
  font-weight: 600 !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none !important; }
[data-testid="stTabs"] [data-baseweb="tab-border"]    { display: none !important; }

/* ── PAGE HEADER ──────────────────────────────── */
.pg-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding-bottom: 1.6rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--bdr);
}
.pg-eyebrow {
  font-family: 'DM Sans', sans-serif;
  font-size: .65rem;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}
.pg-title {
  font-family: 'DM Serif Display', serif;
  font-size: 2.2rem;
  font-weight: 400;
  letter-spacing: -.5px;
  color: var(--ink);
  line-height: 1;
}
.pg-sub { font-size: .8rem; color: var(--muted); margin-top: 6px; font-weight: 300; }
.upill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: .68rem;
  color: var(--muted);
  white-space: nowrap;
  letter-spacing: .2px;
}
.live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green); display: inline-block;
  animation: pulse 3s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

/* ── KPI STRIP ────────────────────────────────── */
.kpi-strip {
  display: grid;
  gap: 0;
  border: 1px solid var(--bdr);
  border-top: 2px solid var(--ink);
  border-radius: 0 0 4px 4px;
  overflow: hidden;
  margin-bottom: 2.5rem;
}
.kpi {
  padding: 16px 20px 14px;
  border-right: 1px solid var(--bdr);
  background: var(--bg);
}
.kpi:last-child { border-right: none; }
.kpi-lbl {
  font-size: .6rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin-bottom: 8px;
}
.kpi-val {
  font-family: 'DM Serif Display', serif;
  font-size: 2.1rem;
  font-weight: 400;
  line-height: 1;
  color: var(--ink);
}
.kpi-val.zero { color: var(--muted2); }
.kpi-val.positive { color: var(--green); }
.kpi-val.negative { color: var(--red); }

/* ── CHART ────────────────────────────────────── */
.chart-section { margin-bottom: 2.5rem; }
.section-label {
  font-size: .6rem;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 4px;
}
.section-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.15rem;
  font-weight: 400;
  color: var(--ink);
  margin-bottom: 4px;
}
.section-sub { font-size: .75rem; color: var(--muted); margin-bottom: 1.2rem; font-weight: 300; }
.chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: var(--bdr); border: 1px solid var(--bdr); border-radius: 4px; overflow: hidden; }
.chart-col { background: var(--bg2); padding: 20px 22px; }
.chart-col-title {
  font-size: .6rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--muted);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.chart-col-title span { display: inline-block; width: 12px; height: 2px; border-radius: 1px; }
.hbar-row { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.hbar-lbl {
  font-size: .71rem;
  font-weight: 500;
  color: var(--txt2);
  width: 80px;
  text-align: right;
  flex-shrink: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.hbar-track { flex: 1; height: 18px; background: var(--bg3); border-radius: 2px; overflow: hidden; }
.hbar-fill { height: 100%; border-radius: 2px; display: flex; align-items: center; }
.hbar-val { font-size: .67rem; font-weight: 600; padding-left: 8px; color: #fff; white-space: nowrap; }

/* ── SORT INFO ────────────────────────────────── */
.sort-info {
  font-size: .67rem;
  color: var(--muted);
  padding: 8px 0 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  letter-spacing: .1px;
}
.sort-tag {
  display: inline-flex;
  align-items: center;
  background: var(--bg3);
  border: 1px solid var(--bdr2);
  border-radius: 2px;
  padding: 1px 7px;
  font-size: .63rem;
  font-weight: 600;
  color: var(--txt2);
  letter-spacing: .3px;
}

/* ── TABLE ────────────────────────────────────── */
.tbl-wrap { overflow-x: auto; border: 1px solid var(--bdr); border-top: 2px solid var(--ink); border-radius: 0 0 4px 4px; margin-bottom: 1.5rem; }
.tbl { width: 100%; border-collapse: collapse; font-size: .78rem; }
.tbl thead tr { background: var(--bg2); }
.tbl th {
  padding: 11px 14px;
  border-bottom: 1px solid var(--bdr2);
  font-size: .59rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 1.1px;
  text-align: left;
  white-space: nowrap;
}
.tbl th.col-active { color: var(--ink); }
.tbl th.col-active::after { content: ' ↓'; }
.tbl td { padding: 9px 14px; border-bottom: 1px solid var(--bdr); vertical-align: middle; white-space: nowrap; }
.tbl tbody tr:hover td { background: var(--bg2); }
.tbl tbody tr:last-child td { border-bottom: none; }

.rname { font-weight: 600; font-size: .83rem; color: var(--ink); letter-spacing: -.2px; }
.rsub  { font-size: .62rem; color: var(--muted); font-weight: 300; }

.occ-row   { display: flex; align-items: center; gap: 8px; }
.occ-track { width: 46px; height: 3px; background: var(--bg3); border-radius: 2px; }
.occ-fill  { height: 100%; border-radius: 2px; }
.om { font-size: .76rem; font-weight: 600; }

.ng  { color: var(--green); font-size: .78rem; font-weight: 600; }
.nr  { color: var(--red);   font-size: .78rem; font-weight: 600; }
.nm  { color: var(--muted); font-size: .78rem; font-weight: 300; }
.nt  { color: var(--txt2);  font-size: .78rem; }
.no  { color: var(--amber); font-size: .78rem; font-weight: 600; }

/* ── EDITOR HEADER ────────────────────────────── */
.editor-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin: 1.8rem 0 .6rem;
  padding-bottom: .8rem;
  border-bottom: 1px solid var(--bdr);
}
.editor-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--ink);
  margin-bottom: 2px;
}
.editor-sub { font-size: .75rem; color: var(--muted); font-weight: 300; }

/* ── BANNER ───────────────────────────────────── */
.acion-banner {
  display: flex;
  align-items: center;
  background: var(--green-lt);
  border: 1px solid #b6dfc9;
  border-left: 3px solid var(--green);
  border-radius: 3px;
  padding: 10px 16px;
  margin: 1rem 0 .6rem;
}
.acion-txt { font-size: .8rem; color: var(--green); font-weight: 500; }

.warn-banner {
  background: var(--amber-lt);
  border: 1px solid #e8d0a0;
  border-left: 3px solid var(--amber);
  border-radius: 3px;
  padding: 8px 14px;
  margin-bottom: .8rem;
  font-size: .78rem;
  color: var(--amber);
  font-weight: 400;
}

/* ── SIDEBAR ──────────────────────────────────── */
.sb-section {
  font-size: .58rem;
  font-weight: 700;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--muted2);
  margin: 1.2rem 0 .5rem;
  padding-bottom: .4rem;
  border-bottom: 1px solid var(--bdr);
}
.sb-label {
  font-size: .63rem;
  font-weight: 500;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .8px;
  margin: .7rem 0 .25rem;
}

/* ── FOOTER ───────────────────────────────────── */
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  margin-top: .5rem;
  border-top: 1px solid var(--bdr);
}
.ftxt { font-size: .65rem; color: var(--muted2); letter-spacing: .1px; }
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
        return df
    except:
        return pd.DataFrame()

def prep_acel(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    df = df.copy()
    int_cols   = ["pax","capacidade_atual","assentos_disponiveis","pax_d1","pax_d2","pax_d3","pax_d4","pax_d5",
                  "pax_hoje_parcial","predict_consenso","pax_faltam_forecast","predict_time_series","predict_eixo_sentido"]
    float_cols = ["occ_atual","tkm_comp","aceleracao_pct","aceleracao_abs","tendencia_linear",
                  "pct_atingimento_forecast","media_d2_d5","load_factor_atual"]
    for c in int_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    for c in float_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    if "data" in df.columns: df["data"] = pd.to_datetime(df["data"])
    return df

def prep_curva(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    df = df.copy()
    float_cols = ["occ_atual","lf_pascoa_2026","lf_atual","ratio","tkm_comp",
                  "preco_base","preco_est_draft","preco_com_sazonalidade","mult_final","price_cc",
                  "tkm_atual","mult_flutuacao","preco_com_flutuacao","preco_staff","preco_mult_flutuacao"]
    for c in float_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c].replace("null", None), errors="coerce")
    for c in ["pax","capacidade_atual","vagas_restantes","antecedencia"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    if "data" in df.columns: df["data"] = pd.to_datetime(df["data"])
    return df

# ── SCORE ─────────────────────────────────────────────────────────────────────
def calcular_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    fc        = df["pct_atingimento_forecast"].fillna(0).clip(0, 150) / 150
    occ       = df["occ_atual"].fillna(0).clip(0, 1)
    acel      = df["aceleracao_pct"].fillna(0).clip(-100, 200)
    a_min, a_max = acel.min(), acel.max()
    acel_norm = (acel - a_min) / (a_max - a_min + 1e-9)
    df["_score"] = (0.45 * occ) + (0.35 * fc) + (0.20 * acel_norm)
    return df

# ── HELPERS HTML ──────────────────────────────────────────────────────────────
def sinal_tag(sinal):
    m = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    if m["badge"]: return f'<span class="badge {m["badge"]}">{m["short"]}</span>'
    return f'<span class="sinal-tag"><span class="sinal-dot" style="background:{m["dot"]}"></span>{m["short"]}</span>'

def occ_html(v):
    try:
        pct = min(float(v)*100, 100)
        col = "#c0392b" if pct>=90 else ("#d35400" if pct>=70 else "#2d6a4f")
        return (f'<div class="occ-row"><div class="occ-track">'
                f'<div class="occ-fill" style="width:{pct:.0f}%;background:{col}"></div></div>'
                f'<span class="om" style="color:{col}">{pct:.0f}%</span></div>')
    except: return "—"

def spark_html(d5, d4, d3, d2, d1):
    vals = [float(x) if str(x) not in ("nan","") else 0 for x in [d5,d4,d3,d2,d1]]
    mx   = max(vals) if max(vals)>0 else 1
    up   = vals[-1] >= (sum(vals[:-1])/max(len(vals)-1,1))
    bars = ""
    for i,v in enumerate(vals):
        h = max(int((v/mx)*20), 2)
        last = (i==4)
        cls  = ("su sl" if up else "sd sl") if last else ("su" if up else "sd")
        bars += f'<div class="sb {cls}" style="height:{h}px" title="D{5-i}: {v:.0f}"></div>'
    return f'<div class="spark">{bars}</div>'

def acel_html(pct):
    try:
        v = float(pct)
        if v>30:  return f'<span class="ng">+{v:.0f}%</span>'
        if v<-30: return f'<span class="nr">{v:.0f}%</span>'
        return f'<span class="nm">{v:.0f}%</span>'
    except: return '<span class="nm">—</span>'

def fc_html(pct, faltam):
    try:
        v   = float(pct)
        cls = "nr" if v<50 else ("no" if v<80 else "ng")
        ft  = (f'<br><span class="nm" style="font-size:.62rem">faltam {int(faltam)}</span>'
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

def score_bar(score):
    try:
        pct = min(float(score)*100, 100)
        return (f'<div class="score-wrap"><div class="score-track">'
                f'<div class="score-fill" style="width:{pct:.0f}%"></div></div>'
                f'<span class="score-val">{pct:.0f}</span></div>')
    except: return "—"

def lf_bar(v, ref=None):
    try:
        pct   = min(float(v)*100, 100)
        ref_f = float(ref) if ref is not None and str(ref) not in ("nan","") else None
        col   = "#2d6a4f" if (ref_f is None or float(v) >= ref_f) else "#c0392b"
        return (f'<div class="occ-row"><div class="occ-track" style="width:52px">'
                f'<div class="occ-fill" style="width:{pct:.0f}%;background:{col}"></div></div>'
                f'<span class="om" style="color:{col}">{float(v):.0%}</span></div>')
    except: return "—"

def ratio_html(v):
    try:
        f = float(v)
        if f>=1.2: return f'<span class="ng" style="font-weight:700">{f:.2f}x</span>'
        if f>=1.0: return f'<span class="ng">{f:.2f}x</span>'
        if f>=0.8: return f'<span class="no">{f:.2f}x</span>'
        return f'<span class="nr">{f:.2f}x</span>'
    except: return "—"

def turno_badge(t):
    cores = {"MANHA":"#f97316","TARDE":"#2563eb","NOITE":"#7c3aed","MADRUGADA":"#374151"}
    cor   = cores.get(str(t).upper(), "#8c8c84")
    return (f'<span style="display:inline-block;padding:1px 7px;border-radius:3px;'
            f'font-size:.61rem;font-weight:600;background:{cor}18;color:{cor};'
            f'border:1px solid {cor}33">{t}</span>')

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-section">Fontes de dados</div><div class="sb-label">Tiradentes · URL</div>',
                unsafe_allow_html=True)
    url_curva = st.text_input("", value=GITHUB_RAW_CURVA, label_visibility="collapsed", key="url_curva")

    st.markdown('<div class="sb-label" style="margin-top:10px">Feriado Maio · URL</div>', unsafe_allow_html=True)
    url_curva2 = st.text_input("", value=GITHUB_RAW_CURVA2, label_visibility="collapsed", key="url_curva2")

    if st.button("Recarregar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    df_curva_raw  = prep_curva(load_data(url_curva))
    df_curva2_raw = prep_curva(load_data(url_curva2))


# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Tiradentes", "Feriado Maio"])

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO REUTILIZÁVEL — CURVA DE FERIADO + EDITOR DE PRICING
# Parâmetros:
#   df_raw      — DataFrame já preparado com prep_curva()
#   tab_key     — prefixo único para todas as chaves de session_state (ex: "t2","t3")
#   titulo      — título exibido no header
# ══════════════════════════════════════════════════════════════════════════════
def render_curva(df_raw: pd.DataFrame, tab_key: str, titulo: str, extra_cols: list = None):
    agora_t = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(f"""
    <div class="pg-header">
      <div>
        <div class="pg-eyebrow">Curva de Feriado</div>
        <div class="pg-title">{titulo}</div>
        <div class="pg-sub">Comparativo de load factor — edite o preço desejado diretamente na tabela</div>
      </div>
      <div class="upill"><span class="live-dot"></span>Atualizado {agora_t} · via Databricks</div>
    </div>
    """, unsafe_allow_html=True)

    if df_raw.empty:
        st.info("Nenhum dado de curva. Verifique a URL na sidebar.")
        return

    df_c = df_raw.copy()

    # ── KPIs ──────────────────────────────────────────────────────────────────
    lf_med  = df_c["lf_atual"].mean()
    lf_ref  = df_c["lf_pascoa_2026"].mean()
    rat_med = df_c["ratio"].mean()
    acima   = int((df_c["ratio"] >= 1).sum())
    abaixo  = int((df_c["ratio"] < 1).sum())
    rat_cls = "c-grn" if rat_med >= 1 else "c-red"
    rat_dot = "#2d6a4f" if rat_med >= 1 else "#c0392b"

    ratio_cls_val = "positive" if rat_med >= 1 else "negative"
    st.markdown(f"""
    <div class="kpi-strip" style="grid-template-columns:repeat(5,1fr)">
      <div class="kpi"><div class="kpi-lbl">LF Atual médio</div>
        <div class="kpi-val">{lf_med:.0%}</div></div>
      <div class="kpi"><div class="kpi-lbl">LF Referência</div>
        <div class="kpi-val">{lf_ref:.0%}</div></div>
      <div class="kpi"><div class="kpi-lbl">Ratio médio</div>
        <div class="kpi-val {ratio_cls_val}">{rat_med:.2f}</div></div>
      <div class="kpi"><div class="kpi-lbl">Acima da ref.</div>
        <div class="kpi-val positive">{acima}</div></div>
      <div class="kpi"><div class="kpi-lbl">Abaixo da ref.</div>
        <div class="kpi-val negative">{abaixo}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Gráfico ────────────────────────────────────────────────────────────────
    df_chart = (df_c.groupby("sentido")
                .agg(lf_atual=("lf_atual","mean"), lf_ref=("lf_pascoa_2026","mean"),
                     ratio=("ratio","mean"), occ=("occ_atual","mean"))
                .reset_index().sort_values("occ", ascending=False).head(12))
    max_lf = max(df_chart["lf_atual"].max(), df_chart["lf_ref"].max(), 0.01)
    chart_rows = ""
    for _, r in df_chart.iterrows():
        lf_a  = float(r["lf_atual"]) if pd.notna(r["lf_atual"]) else 0
        lf_r  = float(r["lf_ref"])   if pd.notna(r["lf_ref"])   else 0
        rat   = float(r["ratio"])    if pd.notna(r["ratio"])    else 0
        w_a   = min(lf_a / max_lf * 100, 100)
        w_r   = min(lf_r / max_lf * 100, 100)
        col_a = "#2d6a4f" if lf_a >= lf_r else "#c0392b"
        rat_c = "ng" if rat >= 1 else "nr"
        chart_rows += (
            f'<div class="hbar-row">'
            f'<div style="width:80px;text-align:right;flex-shrink:0"><span class="hbar-lbl">{r["sentido"]}</span></div>'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:3px">'
            f'<div class="hbar-track" style="height:13px">'
            f'<div class="hbar-fill" style="width:{w_a:.1f}%;background:{col_a}">'
            f'<span class="hbar-val" style="font-size:.6rem">{lf_a:.0%}</span></div></div>'
            f'<div class="hbar-track" style="height:13px;background:#e8e8ed">'
            f'<div class="hbar-fill" style="width:{w_r:.1f}%;background:#9ab8d4">'
            f'<span class="hbar-val" style="font-size:.6rem;color:#1a1a18">{lf_r:.0%}</span></div></div>'
            f'</div>'
            f'<div style="width:44px;text-align:right;flex-shrink:0">'
            f'<span class="{rat_c}" style="font-size:.76rem">{rat:.2f}x</span></div></div>'
        )
    st.markdown(f"""
    <div class="chart-section">
      <div class="section-label">Análise comparativa</div>
      <div class="section-title">LF Atual vs Referência</div>
      <div class="section-sub">Top rotas por ocupação &mdash;
        <span style="display:inline-inline;margin-right:12px">
          <span style="display:inline-block;width:10px;height:2px;background:#1e5c3a;vertical-align:middle;margin-right:4px"></span>LF Atual
        </span>
        <span style="display:inline-inline">
          <span style="display:inline-block;width:10px;height:2px;background:#9ab8d4;vertical-align:middle;margin-right:4px"></span>LF Referência
        </span>
      </div>
      <div class="chart-col" style="margin-top:12px;max-width:700px">{chart_rows}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filtros ────────────────────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        datas_c     = sorted(df_c["data"].dt.date.unique())
        datas_c_sel = st.multiselect("Data", options=datas_c, default=datas_c,
                                     format_func=lambda d: d.strftime("%d/%m"),
                                     key=f"{tab_key}_datas")
    with col_f2:
        turnos_c   = sorted(df_c["turno"].dropna().unique())
        turnos_sel = st.multiselect("Turno", options=turnos_c, default=turnos_c,
                                    key=f"{tab_key}_turnos")
    with col_f3:
        rota_c = st.text_input("Buscar rota", placeholder="ex: BHZ-RIO", key=f"{tab_key}_rota")

    df_cv = df_c.copy()
    if datas_c_sel: df_cv = df_cv[df_cv["data"].dt.date.isin(datas_c_sel)]
    if turnos_sel:  df_cv = df_cv[df_cv["turno"].isin(turnos_sel)]
    if rota_c:      df_cv = df_cv[df_cv["sentido"].str.upper().str.contains(rota_c.upper(), na=False)]
    df_cv = df_cv.sort_values(["occ_atual","ratio"], ascending=[False, False]).reset_index(drop=True)

    # ── Filtro de já enviados ──────────────────────────────────────────────────
    key_enviadas = f"{tab_key}_linhas_enviadas"
    if key_enviadas not in st.session_state:
        st.session_state[key_enviadas] = set()

    def chave_linha(row):
        data_str = pd.to_datetime(row["data"]).strftime("%Y-%m-%d") if pd.notna(row["data"]) else ""
        return f"{data_str}|{row.get('turno','')}|{row.get('sentido','')}"

    mask_enviadas = df_cv.apply(chave_linha, axis=1).isin(st.session_state[key_enviadas])
    n_ocultas     = int(mask_enviadas.sum())
    df_cv_editor  = df_cv[~mask_enviadas].reset_index(drop=True)

    if n_ocultas > 0:
        col_oc1, col_oc2 = st.columns([5, 1])
        with col_oc1:
            st.markdown(f"""
            <div class="warn-banner">
              <strong>{n_ocultas}</strong> linha{"s" if n_ocultas>1 else ""} já enviada{"s" if n_ocultas>1 else ""} oculta{"s" if n_ocultas>1 else ""}.
              Clique em 'Mostrar todas' para reexibi-las.
            </div>
            """, unsafe_allow_html=True)
        with col_oc2:
            if st.button("Mostrar todas", key=f"{tab_key}_mostrar"):
                st.session_state[key_enviadas] = set()
                st.rerun()

    # ── Editor de Pricing ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="editor-header">
      <div>
        <div class="editor-title">Editor de Pricing</div>
        <div class="editor-sub">Preencha <strong>Preço novo</strong> nas linhas que deseja alterar — o mult é calculado automaticamente sobre o preço com flutuação. Desmarque <strong>Incluir</strong> para ignorar uma linha.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    key_version = f"{tab_key}_editor_version"
    if key_version not in st.session_state:
        st.session_state[key_version] = 0

    cols_editor    = ["data","turno","rota_principal","sentido","antecedencia",
                      "occ_atual","pax","vagas_restantes","lf_atual","lf_pascoa_2026","ratio",
                      "tkm_atual","tkm_comp","price_cc","preco_com_sazonalidade","preco_staff","preco_com_flutuacao",
                      "mult_final","mult_flutuacao"]
    if extra_cols:
        cols_editor += [c for c in extra_cols if c not in cols_editor]
    cols_presentes = [c for c in cols_editor if c in df_cv_editor.columns]
    df_editor      = df_cv_editor[cols_presentes].copy()

    df_editor["data_fmt"] = pd.to_datetime(df_editor["data"]).dt.strftime("%d/%m/%Y")
    if "occ_atual"      in df_editor.columns: df_editor["occ_pct"]  = (df_editor["occ_atual"]      * 100).round(1).astype(str) + "%"
    if "lf_atual"       in df_editor.columns: df_editor["lf_a_fmt"] = (df_editor["lf_atual"]       * 100).round(1).astype(str) + "%"
    if "lf_pascoa_2026" in df_editor.columns: df_editor["lf_r_fmt"] = (df_editor["lf_pascoa_2026"] * 100).round(1).astype(str) + "%"
    if "ratio"          in df_editor.columns: df_editor["ratio_fmt"]= df_editor["ratio"].round(3).astype(str) + "x"

    df_editor["incluir"]       = True
    df_editor["✏️ Preço novo"] = None

    show_cols = ["incluir","data_fmt","turno","rota_principal","sentido","antecedencia",
                 "occ_pct","pax","vagas_restantes","lf_a_fmt","lf_r_fmt","ratio_fmt",
                 "tkm_atual","tkm_comp","price_cc","preco_com_sazonalidade","preco_staff","preco_com_flutuacao",
                 "mult_final","mult_flutuacao"]
    if extra_cols:
        show_cols += [c for c in extra_cols if c not in show_cols]
    show_cols += ["✏️ Preço novo"]
    show_cols  = [c for c in show_cols if c in df_editor.columns]
    df_show    = df_editor[show_cols].copy()

    col_config = {
        "incluir":             st.column_config.CheckboxColumn("Incluir", default=True),
        "data_fmt":            st.column_config.TextColumn("Data",             disabled=True),
        "turno":               st.column_config.TextColumn("Turno",            disabled=True),
        "rota_principal":      st.column_config.TextColumn("Rota principal",   disabled=True),
        "sentido":             st.column_config.TextColumn("Sentido",          disabled=True),
        "antecedencia":        st.column_config.NumberColumn("Antec.",         disabled=True),
        "occ_pct":             st.column_config.TextColumn("Occ",              disabled=True),
        "pax":                 st.column_config.NumberColumn("PAX",            disabled=True),
        "vagas_restantes":     st.column_config.NumberColumn("Vagas rest.",    disabled=True),
        "lf_a_fmt":            st.column_config.TextColumn("LF Atual",         disabled=True),
        "lf_r_fmt":            st.column_config.TextColumn("LF Ref",           disabled=True),
        "ratio_fmt":           st.column_config.TextColumn("Ratio",            disabled=True),
        "tkm_atual":           st.column_config.NumberColumn("TKM Atual",      disabled=True, format="R$ %.0f"),
        "tkm_comp":            st.column_config.NumberColumn("TKM Comp",       disabled=True, format="R$ %.0f"),
        "price_cc":            st.column_config.NumberColumn("Price CC",       disabled=True, format="R$ %.0f"),
        "preco_com_sazonalidade": st.column_config.NumberColumn("Preço c/ sazon.", disabled=True, format="R$ %.2f"),
        "preco_staff":         st.column_config.NumberColumn("Preço Staff",    disabled=True, format="R$ %.2f"),
        "preco_com_flutuacao": st.column_config.NumberColumn("Preço c/ flut.", disabled=True, format="R$ %.2f"),
        "mult_final":          st.column_config.NumberColumn("Mult Final",     disabled=True, format="%.3fx"),
        "mult_flutuacao":      st.column_config.NumberColumn("Mult Flut.",     disabled=True, format="%.3fx"),
        "preco_mult_flutuacao":st.column_config.NumberColumn("Preço mult. flut.", disabled=True, format="R$ %.2f"),
        "✏️ Preço novo": st.column_config.NumberColumn(
            "Preco novo", min_value=0.0, format="R$ %.2f",
            help="Digite o preço desejado — mult = preco_novo / preco_com_flutuacao",
        ),
    }

    edited = st.data_editor(
        df_show, use_container_width=True, hide_index=True,
        column_config=col_config, num_rows="fixed",
        key=f"{tab_key}_editor_{st.session_state[key_version]}",
    )

    # ── Preview do acionamento ─────────────────────────────────────────────────
    df_editado  = edited[edited["✏️ Preço novo"].notna() & edited["incluir"].fillna(True)].copy()
    n_excluidas = int((~edited["incluir"].fillna(True)).sum())

    if not df_editado.empty:
        df_editado["_preco_prat"]     = df_cv_editor.loc[df_editado.index, "preco_com_sazonalidade"].values
        df_editado["_preco_com_flut"] = df_cv_editor.loc[df_editado.index, "preco_com_flutuacao"].values \
                                        if "preco_com_flutuacao" in df_cv_editor.columns else None
        base_vals = pd.Series(df_editado["_preco_com_flut"]).fillna(
                    pd.Series(df_editado["_preco_prat"])).values
        df_editado["_base_calc"] = base_vals
        df_editado["mult_novo"]  = (df_editado["✏️ Preço novo"] / df_editado["_base_calc"]).round(6)

        df_acionamento = pd.DataFrame({
            "data":                pd.to_datetime(df_editado["data_fmt"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d"),
            "turno":               df_editado["turno"].values,
            "rota_principal":      df_editado["rota_principal"].values,
            "sentido":             df_editado["sentido"].values,
            "preco_com_sazonalidade": df_editado["_preco_prat"].values,
            "preco_com_flutuacao": df_editado["_base_calc"].values,
            "preco_novo":          df_editado["✏️ Preço novo"].values,
            "mult":                df_editado["mult_novo"].values,
        })

        n_edit   = len(df_acionamento)
        excl_txt = f" · {n_excluidas} ignorada{'s' if n_excluidas>1 else ''}" if n_excluidas > 0 else ""
        st.markdown(f"""
        <div class="acion-banner">
          <span class="acion-txt">{n_edit} linha{"s" if n_edit>1 else ""} no acionamento{excl_txt} — pronto para enviar</span>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_acionamento, use_container_width=True, hide_index=True)

        col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 3])
        csv_bytes = df_acionamento.to_csv(index=False).encode("utf-8")

        with col_b1:
            if st.download_button(
                label="Baixar CSV",
                data=csv_bytes,
                file_name=f"pricing_{tab_key}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"{tab_key}_download",
            ):
                for _, r in df_acionamento.iterrows():
                    st.session_state[key_enviadas].add(f"{r['data']}|{r['turno']}|{r['sentido']}")
                st.session_state[key_version] += 1
                st.rerun()

        with col_b2:
            if st.button("Enviar pro GitHub", use_container_width=True,
                         type="primary", key=f"{tab_key}_push"):
                gh_token = st.session_state.get(f"{tab_key}_gh_token", "")
                if not gh_token:
                    st.warning("Cole seu token no campo abaixo.")
                else:
                    repo   = "meninosia2026-beep/aceleracao_vendas"
                    branch = "main"
                    path   = f"data/pricing_{tab_key}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
                    url_gh = f"https://api.github.com/repos/{repo}/contents/{path}"
                    hdrs   = {"Authorization": f"token {gh_token}", "Accept": "application/vnd.github.v3+json"}
                    enc    = base64.b64encode(csv_bytes).decode("utf-8")
                    r_gh   = requests.put(url_gh, headers=hdrs,
                                          data=json.dumps({"message": f"pricing: {path}",
                                                           "content": enc, "branch": branch}))
                    if r_gh.status_code in (200, 201):
                        for _, r in df_acionamento.iterrows():
                            st.session_state[key_enviadas].add(f"{r['data']}|{r['turno']}|{r['sentido']}")
                        st.session_state[key_version] += 1
                        st.success(f"✅ Enviado: {path}")
                        st.rerun()
                    else:
                        st.error(f"Erro {r_gh.status_code}: {r_gh.json().get('message')}")

        with col_b3:
            if st.button("Limpar edições", use_container_width=True, key=f"{tab_key}_reset"):
                st.session_state[key_version] += 1
                st.session_state[key_enviadas] = set()
                st.rerun()

        with st.expander("Token GitHub"):
            st.text_input("Token", type="password", key=f"{tab_key}_gh_token",
                          help="Necessário só para 'Enviar pro GitHub'. Fica apenas na sessão.")
    else:
        st.markdown("""
        <div style="padding:10px 16px;background:var(--bg2);border:1px solid var(--bdr);border-radius:3px;margin-top:.8rem">
          <span style="font-size:.78rem;color:var(--muted);font-weight:300">
            Preencha a coluna <strong style="font-weight:600;color:var(--txt2)">Preco novo</strong> nas linhas que deseja alterar para gerar o acionamento.
          </span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Limpar edições", key=f"{tab_key}_reset_empty"):
            st.session_state[key_version] += 1
            st.session_state[key_enviadas] = set()
            st.rerun()

    st.markdown(f"""
    <div class="footer">
      <span class="ftxt"><strong style="color:var(--txt)">{len(df_cv_editor)}</strong> linhas no editor · {len(df_cv)} total · {n_ocultas} já enviadas ocultas</span>
      <span class="ftxt">mult = preço novo / preço c/ flut. · &gt; 1 aumento · &lt; 1 redução</span>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CURVA DE FERIADO
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    render_curva(df_curva_raw, tab_key="t1", titulo="Tiradentes")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CURVA DE FERIADO 2
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    render_curva(df_curva2_raw, tab_key="t2", titulo="Feriado Maio",
                 extra_cols=["preco_mult_flutuacao"])
